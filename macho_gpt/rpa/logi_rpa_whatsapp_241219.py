"""
MACHO-GPT RPA WhatsApp 자동화 모듈  
------------------------------------------
Samsung C&T Logistics · HVDC Project
파일명: logi_rpa_whatsapp_241219.py

기능:
- Playwright 기반 WhatsApp Web 자동화
- 대화 내용 자동 추출 및 텍스트 변환
- 기존 WhatsApp 처리 모듈과 통합
- 스케줄링 지원 및 에러 복구
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import yaml

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError

# 기존 모듈 import
from macho_gpt.core.logi_whatsapp_241219 import WhatsAppProcessor, WhatsAppMessage


class WhatsAppRPAExtractor:
    """
    MACHO-GPT WhatsApp Web RPA 자동화 클래스
    
    Mode: PRIME (기본 모드) + LATTICE (고급 텍스트 처리)
    Confidence: ≥0.90 필요
    """
    
    def __init__(self, config_path: str = "configs/config_prime_dev.yaml"):
        self.config = self._load_config(config_path)
        self.mode = self.config.get('system', {}).get('mode', 'PRIME')
        self.confidence_threshold = 0.90
        
        # WhatsApp 설정
        self.web_url = self.config.get('whatsapp', {}).get('web_url', 'https://web.whatsapp.com/')
        self.chat_title = self.config.get('whatsapp', {}).get('chat_title', 'MR.CHA 전용')
        self.auth_file = Path(self.config.get('whatsapp', {}).get('auth_file', 'auth.json'))
        self.extraction_hours = self.config.get('whatsapp', {}).get('extraction_hours', 24)
        
        # RPA 설정
        self.browser_type = self.config.get('rpa', {}).get('browser', 'chromium')
        self.headless = self.config.get('rpa', {}).get('headless', False)
        self.timeout = self.config.get('rpa', {}).get('timeout', 30000)
        self.retry_attempts = self.config.get('rpa', {}).get('retry_attempts', 3)
        self.scroll_delay = self.config.get('rpa', {}).get('scroll_delay', 1000)
        
        # 프로세서 초기화
        self.processor = WhatsAppProcessor(mode=self.mode)
        
        # 로깅 설정
        self._setup_logging()
    
    def _load_config(self, config_path: str) -> Dict:
        """YAML 설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return {}
    
    def _setup_logging(self):
        """로깅 설정"""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/whatsapp_rpa.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def setup_browser_session(self) -> Tuple[Browser, BrowserContext]:
        """
        브라우저 세션 설정 및 인증
        
        Returns:
            tuple: (browser, context) 객체
            
        Triggers:
            - 인증 실패 시 ZERO 모드 전환
            - 브라우저 실행 실패 시 재시도
        """
        playwright = await async_playwright().start()
        
        try:
            # 브라우저 실행
            browser = await getattr(playwright, self.browser_type).launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-setuid-sandbox'] if self.headless else None
            )
            
            # 인증 파일 확인
            storage_state = None
            if self.auth_file.exists():
                try:
                    with open(self.auth_file, 'r', encoding='utf-8') as f:
                        storage_state = json.load(f)
                    self.logger.info(f"Loaded auth from {self.auth_file}")
                except Exception as e:
                    self.logger.warning(f"Failed to load auth file: {e}")
            
            # 브라우저 컨텍스트 생성
            context = await browser.new_context(
                storage_state=storage_state,
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            return browser, context
            
        except Exception as e:
            self.logger.error(f"Browser setup failed: {e}")
            raise
    
    async def authenticate_whatsapp(self, page: Page) -> bool:
        """
        WhatsApp Web 인증 처리
        
        Args:
            page: Playwright 페이지 객체
            
        Returns:
            bool: 인증 성공 여부
        """
        try:
            await page.goto(self.web_url, timeout=self.timeout)
            
            # 로그인 상태 확인
            await page.wait_for_timeout(3000)  # 페이지 로드 대기
            
            # QR 코드가 있는지 확인 (로그인 필요)
            qr_code = await page.locator('canvas[aria-label="Scan me!"]').count()
            
            if qr_code > 0:
                self.logger.warning("QR code detected. Manual login required.")
                self.logger.info("Please scan QR code and press Enter to continue...")
                
                # 개발 모드에서는 수동 로그인 대기
                if not self.headless:
                    input("Press Enter after scanning QR code...")
                    
                    # 인증 정보 저장
                    await self._save_auth_state(page)
                    
                return True
            
            # 이미 로그인된 상태인지 확인
            chat_area = await page.locator('[data-testid="conversation-panel-wrapper"]').count()
            if chat_area > 0:
                self.logger.info("Already authenticated")
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return False
    
    async def _save_auth_state(self, page: Page):
        """인증 상태 저장"""
        try:
            storage_state = await page.context.storage_state()
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(storage_state, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Auth state saved to {self.auth_file}")
        except Exception as e:
            self.logger.error(f"Failed to save auth state: {e}")
    
    async def extract_chat_messages(self, page: Page) -> str:
        """
        지정된 채팅방에서 메시지 추출
        
        Args:
            page: Playwright 페이지 객체
            
        Returns:
            str: 추출된 채팅 텍스트
            
        Triggers:
            - 채팅방 찾기 실패 시 ZERO 모드 전환
            - 메시지 추출 실패 시 재시도
        """
        try:
            # 채팅방 검색 및 선택
            await self._select_chat(page)
            
            # 메시지 스크롤 및 로드
            await self._scroll_to_load_messages(page)
            
            # 메시지 추출
            messages = await self._extract_message_elements(page)
            
            self.logger.info(f"Extracted {len(messages)} messages")
            return "\n".join(messages)
            
        except Exception as e:
            self.logger.error(f"Message extraction failed: {e}")
            raise
    
    async def _select_chat(self, page: Page):
        """채팅방 선택"""
        try:
            # 채팅방 검색
            search_box = page.locator('[data-testid="chat-list-search"]')
            await search_box.fill(self.chat_title)
            await page.wait_for_timeout(2000)
            
            # 채팅방 클릭
            chat_selector = f'span[title="{self.chat_title}"]'
            await page.locator(chat_selector).first.click()
            await page.wait_for_timeout(2000)
            
            self.logger.info(f"Selected chat: {self.chat_title}")
            
        except Exception as e:
            self.logger.error(f"Failed to select chat: {e}")
            raise
    
    async def _scroll_to_load_messages(self, page: Page):
        """메시지 로드를 위한 스크롤"""
        try:
            # 메시지 컨테이너 찾기
            message_container = page.locator('[data-testid="conversation-panel-wrapper"]')
            
            # 최근 24시간 메시지 로드를 위해 스크롤
            scroll_attempts = 10
            for i in range(scroll_attempts):
                await page.keyboard.press('PageUp')
                await page.wait_for_timeout(self.scroll_delay)
                
                # 날짜 확인 로직 (선택적)
                # 24시간 이전 메시지에 도달했는지 확인
                
            self.logger.info(f"Scrolled {scroll_attempts} times to load messages")
            
        except Exception as e:
            self.logger.error(f"Scrolling failed: {e}")
            raise
    
    async def _extract_message_elements(self, page: Page) -> List[str]:
        """메시지 요소 추출"""
        try:
            # 메시지 선택자 (일반적인 WhatsApp Web 구조)
            message_selectors = [
                '[data-testid="msg-container"]',
                '.message-in, .message-out',
                '[data-testid="conversation-panel-wrapper"] div[data-testid]'
            ]
            
            messages = []
            
            for selector in message_selectors:
                elements = await page.locator(selector).all()
                if elements:
                    for element in elements:
                        try:
                            # 메시지 텍스트 추출
                            text = await element.text_content()
                            if text and text.strip():
                                messages.append(text.strip())
                        except Exception as e:
                            continue
                    
                    if messages:
                        break
            
            # 중복 제거 및 정렬
            unique_messages = list(dict.fromkeys(messages))
            
            return unique_messages
            
        except Exception as e:
            self.logger.error(f"Message element extraction failed: {e}")
            return []
    
    async def process_extracted_data(self, raw_text: str) -> Dict:
        """
        추출된 데이터 처리 및 요약
        
        Args:
            raw_text: 추출된 원시 텍스트
            
        Returns:
            dict: 처리된 데이터 및 요약 결과
        """
        try:
            # 메시지 파싱
            messages = self.processor.parse_whatsapp_text(raw_text)
            
            # 요약 데이터 추출
            summary_data = self.processor.extract_summary_data(messages)
            
            # KPI 생성
            kpi_data = self.processor.generate_kpi_summary(messages)
            
            # 결과 통합
            result = {
                'timestamp': datetime.now().isoformat(),
                'extraction_status': 'SUCCESS',
                'confidence': summary_data.get('confidence', 0.0),
                'mode': self.mode,
                'raw_text': raw_text,
                'parsed_messages': len(messages),
                'summary_data': summary_data,
                'kpi_data': kpi_data,
                'triggers': summary_data.get('triggers', []),
                'next_cmds': summary_data.get('next_cmds', [])
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Data processing failed: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'extraction_status': 'FAIL',
                'confidence': 0.0,
                'mode': 'ZERO',
                'error': str(e),
                'triggers': ['/switch_mode ZERO'],
                'next_cmds': ['/logi-master --fallback']
            }
    
    async def run_extraction(self) -> Dict:
        """
        전체 추출 프로세스 실행
        
        Returns:
            dict: 추출 및 처리 결과
            
        Triggers:
            - 추출 실패 시 재시도
            - 3회 실패 시 ZERO 모드 전환
        """
        for attempt in range(self.retry_attempts):
            try:
                self.logger.info(f"Starting extraction attempt {attempt + 1}")
                
                # 브라우저 설정
                browser, context = await self.setup_browser_session()
                
                try:
                    # 페이지 생성
                    page = await context.new_page()
                    
                    # 인증
                    if not await self.authenticate_whatsapp(page):
                        raise Exception("Authentication failed")
                    
                    # 메시지 추출
                    raw_text = await self.extract_chat_messages(page)
                    
                    # 데이터 처리
                    result = await self.process_extracted_data(raw_text)
                    
                    self.logger.info(f"Extraction completed successfully")
                    return result
                    
                finally:
                    # 브라우저 정리
                    await browser.close()
                    
            except Exception as e:
                self.logger.error(f"Extraction attempt {attempt + 1} failed: {e}")
                if attempt == self.retry_attempts - 1:
                    return {
                        'timestamp': datetime.now().isoformat(),
                        'extraction_status': 'FAIL',
                        'confidence': 0.0,
                        'mode': 'ZERO',
                        'error': str(e),
                        'attempts': self.retry_attempts,
                        'triggers': ['/switch_mode ZERO'],
                        'next_cmds': ['/logi-master --manual-mode']
                    }
                
                # 재시도 전 대기
                await asyncio.sleep(5)
        
        return {}


# 스케줄러 실행 함수
async def scheduled_extraction(config_path: str = "configs/config_prime_dev.yaml"):
    """
    스케줄된 추출 실행
    
    Args:
        config_path: 설정 파일 경로
        
    Returns:
        dict: 추출 결과
    """
    extractor = WhatsAppRPAExtractor(config_path)
    result = await extractor.run_extraction()
    
    # 결과 로깅
    status = result.get('extraction_status', 'UNKNOWN')
    confidence = result.get('confidence', 0.0)
    
    extractor.logger.info(f"Scheduled extraction completed - Status: {status}, Confidence: {confidence}")
    
    return result


# CLI 실행
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp RPA Extractor")
    parser.add_argument("--config", default="configs/config_prime_dev.yaml", help="Config file path")
    parser.add_argument("--mode", default="PRIME", help="Operating mode")
    
    args = parser.parse_args()
    
    # 비동기 실행
    result = asyncio.run(scheduled_extraction(args.config))
    
    print(f"Extraction completed with status: {result.get('extraction_status', 'UNKNOWN')}")
    print(f"Confidence: {result.get('confidence', 0.0)}")
    
    # 추천 명령어 출력
    if result.get('next_cmds'):
        print("\n🔧 **추천 명령어:**")
        for cmd in result.get('next_cmds', [])[:3]:
            print(f"  {cmd}")

# 호환성을 위한 별칭
WhatsAppRPAProcessor = WhatsAppRPAExtractor 