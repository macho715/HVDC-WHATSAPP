#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini HVDC 물류팀 WhatsApp 추출 스크립트 (키워드 토큰화 + 부분 일치 검색)
------------------------------------------------
Samsung C&T Logistics · HVDC Project

기능:
- HVDC 물류팀 채팅방 자동 추출
- 실시간 메시지 분석
- 업무 관련 내용 필터링
- 자동 요약 생성
- 키워드 토큰화로 이모지/특수문자 채팅방 안정적 검색
- 부분 일치 XPath로 높은 매칭 성공률
- 세션 저장으로 QR 재스캔 방지
"""

import asyncio
import logging
import sys
import json
import re
import unicodedata
from pathlib import Path
from datetime import datetime

# MACHO-GPT 모듈 import
try:
    from macho_gpt.rpa.logi_rpa_whatsapp_241219 import WhatsAppRPAExtractor
    from macho_gpt.core.role_config import RoleConfigManager
except ImportError as e:
    print(f"❌ MACHO-GPT 모듈 import 오류: {e}")
    sys.exit(1)

# 세션 매니저 import
from session_manager import get_shared_session, close_shared_session

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/hvdc_whatsapp_extract.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HVDCWhatsAppExtractor:
    """HVDC 프로젝트 전용 WhatsApp 추출기 (이모지 제거 + 텍스트 정규화)"""
    
    def __init__(self):
        self.role_config = RoleConfigManager()
        self.extractor = WhatsAppRPAExtractor(mode="LATTICE")
        
        # HVDC 프로젝트 관련 채팅방 목록
        self.hvdc_chats = [
            "HVDC 물류팀",
            "[HVDC] ⚡ Project lightning ⚡",
            "Abu Dhabi Logistics",
            "Jopetwil 71 Group",
            "AGI- Wall panel-GCC Storage"
        ]
        
        # 개선된 셀렉터 (ARIA 표준 기반)
        self.BTN_SEARCH = 'button[aria-label="Search or start new chat"]'  # 돋보기 버튼
        self.SEARCH_BOX_SELECTORS = [
            'div[role="searchbox"]',  # ARIA 표준
            'div[contenteditable="true"]',
            'div[data-testid="search"]',
            'input[type="text"]'
        ]
        
        # 공유 세션 디렉토리
        self.user_data_dir = "browser_data/shared_session"
        
        print("✅ HVDC WhatsApp 추출기 초기화 완료 (키워드 토큰화 + 부분 일치 검색)")
    
    def sanitize_text(self, text: str) -> str:
        """텍스트 정규화 (이모지 제거, ZWSP 제거, 공백 정규화)"""
        # 이모지 제거 (유니코드 이모지 범위)
        text = re.sub(r'[\U0001F600-\U0001F64F]', '', text)  # 감정 이모지
        text = re.sub(r'[\U0001F300-\U0001F5FF]', '', text)  # 기호 및 픽토그램
        text = re.sub(r'[\U0001F680-\U0001F6FF]', '', text)  # 교통 및 지도
        text = re.sub(r'[\U0001F1E0-\U0001F1FF]', '', text)  # 국기
        text = re.sub(r'[\U00002600-\U000027BF]', '', text)  # 기타 기호
        text = re.sub(r'[\U0001F900-\U0001F9FF]', '', text)  # 보충 기호 및 픽토그램
        text = re.sub(r'[\U0001F018-\U0001F270]', '', text)  # 기타 기호
        text = re.sub(r'[\U0001F004]', '', text)  # 마하종
        text = re.sub(r'[\U0001F0CF]', '', text)  # 플레잉 카드 블랙 조커
        text = re.sub(r'[\U0001F170-\U0001F251]', '', text)  # 기타 기호
        
        # 제로폭 공백(ZWSP) 및 제어문자 제거
        text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')
        
        # 대괄호 제거 (채팅방 제목에서 일반적)
        text = text.replace('[', '').replace(']', '')
        
        # 연속 공백을 단일 공백으로 정규화
        text = ' '.join(text.split())
        
        return text.strip()
    
    def generate_search_tokens(self, title: str) -> list:
        """채팅방 제목에서 검색용 키워드 토큰 생성"""
        # 이모지·제어문자 제거
        cleaned = ''.join(c for c in title if unicodedata.category(c)[0] != 'C' and c.isprintable())
        
        # 대괄호·특수문자 제거 (이모지 포함)
        cleaned = re.sub(r'[\[\]⚡☆★○●□■▶►▪️•]|[^0-9A-Za-z가-힣 ]', '', cleaned)
        
        # 공백 기준 토큰 분리
        tokens = [t for t in cleaned.split() if len(t) >= 3]
        
        # 길이 기준 내림차순 정렬 (가장 구체적인 토큰 우선)
        tokens = sorted(tokens, key=len, reverse=True)
        
        # 토큰이 없으면 정규화된 전체 텍스트 반환
        if not tokens:
            normalized = self.sanitize_text(title)
            return [normalized] if normalized else [title]
        
        return tokens
    
    async def setup_browser_context(self, playwright):
        """브라우저 컨텍스트 설정 (공유 세션 사용)"""
        # 공유 세션 사용
        return await get_shared_session()
    
    async def find_and_activate_search_box(self, page):
        """돋보기 버튼 클릭 후 검색창 찾기 및 활성화 (개선된 버전)"""
        try:
            # 1단계: 돋보기 버튼 클릭 (넓은 뷰포트로 가려짐 방지)
            print("🔍 돋보기 버튼 클릭 중...")
            try:
                await page.locator('button[aria-label="Search or start new chat"]').click(timeout=5000)
            except Error:
                # UI 업데이트 대응 – title 또는 data-icon 속성 fallback
                await page.locator('button[title*="Search"]').first.click(timeout=5000)
            print("✅ 돋보기 버튼 클릭 성공")
            
        except Exception as e:
            print(f"⚠️ 돋보기 버튼 클릭 실패: {str(e)}")
            print("🔄 키보드 단축키 백업 시도...")
            
            # 백업: WhatsApp 공식 검색 단축키 사용
            try:
                await page.keyboard.press('Control+Alt+Shift+F')
                print("✅ 키보드 단축키 성공")
            except Exception as e2:
                print(f"❌ 키보드 단축키도 실패: {str(e2)}")
                raise Exception("검색창을 활성화할 수 없습니다.")
        
        # 2단계: contenteditable 검색창 찾기 (ARIA 표준 우선)
        search_box = None
        for selector in self.SEARCH_BOX_SELECTORS:
            try:
                print(f"🔍 검색창 찾기 시도: {selector}")
                await page.wait_for_selector(selector, timeout=5000)
                search_box = page.locator(selector).first
                await search_box.wait_for(state="visible", timeout=10000)
                print(f"✅ 검색창 발견: {selector}")
                break
            except Exception as e:
                print(f"⚠️ 셀렉터 실패: {selector}")
                continue
        
        if not search_box:
            raise Exception("검색창을 찾을 수 없습니다.")
        
        return search_box
    
    async def input_search_text(self, page, search_box, text):
        """검색어 입력 (type() 메서드 사용)"""
        try:
            # 방법 1: click() + type() 조합 (contenteditable 대응)
            print("🔄 type() 메서드로 검색어 입력...")
            await search_box.click()
            await page.wait_for_timeout(500)
            await search_box.type(text)
            print("✅ type() 메서드 입력 성공")
            
        except Exception as e:
            print(f"⚠️ type() 메서드 실패: {str(e)}")
            print("🔄 키보드 직접 입력 시도...")
            
            try:
                # 방법 2: 키보드 직접 입력
                await search_box.click()
                await page.wait_for_timeout(500)
                await page.keyboard.type(text)
                print("✅ 키보드 직접 입력 성공")
                
            except Exception as e2:
                print(f"❌ 모든 입력 방법 실패: {str(e2)}")
                raise Exception("검색어를 입력할 수 없습니다.")
    
    async def find_chat_by_normalized_text(self, page, chat_title):
        """키워드 토큰화 기반 채팅방 찾기 (이모지/특수문자 대응)"""
        print(f"🔍 채팅방 검색: '{chat_title}'")
        
        # 키워드 토큰 생성
        search_tokens = self.generate_search_tokens(chat_title)
        print(f"🔑 검색 토큰: {search_tokens}")
        
        # 검색 결과 로드 대기
        await page.wait_for_timeout(3000)
        
        # 각 토큰으로 순차 검색 시도
        for i, token in enumerate(search_tokens):
            print(f"🔄 토큰 {i+1}/{len(search_tokens)} 시도: '{token}'")
            
            # 방법 1: Playwright 텍스트 로케이터 (가장 안정적)
            try:
                print(f"  📍 Playwright 텍스트 로케이터 시도...")
                chat_element = page.get_by_text(token, exact=False).first
                await chat_element.wait_for(state="visible", timeout=8000)
                print(f"  ✅ Playwright 텍스트 로케이터 성공: '{token}'")
                return chat_element
            except Exception as e:
                print(f"  ⚠️ Playwright 텍스트 로케이터 실패: {str(e)}")
            
            # 방법 2: XPath with translate() (공백 제거 후 비교)
            try:
                print(f"  📍 XPath translate() 시도...")
                safe_token = token.replace("'", "\\'").replace('"', '\\"')
                xpath = f"//span[contains(translate(@title,' ',''), '{safe_token}')] | //div[contains(translate(@title,' ',''), '{safe_token}')]"
                
                chat_element = page.locator(xpath).first
                await chat_element.wait_for(state="visible", timeout=8000)
                print(f"  ✅ XPath translate() 성공: '{safe_token}'")
                return chat_element
            except Exception as e:
                print(f"  ⚠️ XPath translate() 실패: {str(e)}")
            
            # 방법 3: XPath with normalize-space()
            try:
                print(f"  📍 XPath normalize-space() 시도...")
                safe_token = token.replace("'", "\\'").replace('"', '\\"')
                xpath = f"//span[contains(normalize-space(@title), '{safe_token}')] | //div[contains(normalize-space(@title), '{safe_token}')]"
                
                chat_element = page.locator(xpath).first
                await chat_element.wait_for(state="visible", timeout=8000)
                print(f"  ✅ XPath normalize-space() 성공: '{safe_token}'")
                return chat_element
            except Exception as e:
                print(f"  ⚠️ XPath normalize-space() 실패: {str(e)}")
            
            # 방법 4: CSS 셀렉터 백업
            try:
                print(f"  📍 CSS 셀렉터 백업 시도...")
                css_patterns = [
                    f'span[title*="{token}"]',
                    f'div[title*="{token}"]',
                    f'[aria-label*="{token}"]'
                ]
                
                for css in css_patterns:
                    try:
                        chat_element = page.locator(css).first
                        await chat_element.wait_for(state="visible", timeout=5000)
                        print(f"  ✅ CSS 셀렉터 성공: {css}")
                        return chat_element
                    except Exception:
                        continue
            except Exception as e:
                print(f"  ⚠️ CSS 셀렉터 백업 실패: {str(e)}")
        
        # 모든 토큰 실패 시 원본 텍스트로 최종 시도
        print("🔄 원본 텍스트 최종 시도...")
        try:
            safe_original = chat_title.replace("'", "\\'").replace('"', '\\"')
            xpath = f"//span[contains(@title, '{safe_original}')] | //div[contains(@title, '{safe_original}')]"
            
            chat_element = page.locator(xpath).first
            await chat_element.wait_for(state="visible", timeout=5000)
            print(f"✅ 원본 텍스트 최종 성공: '{safe_original}'")
            return chat_element
        except Exception as e:
            print(f"⚠️ 원본 텍스트 최종 실패: {str(e)}")
        
        return None
    
    async def extract_hvdc_chats(self):
        """HVDC 관련 채팅방들 추출 (키워드 토큰화 + 부분 일치 검색)"""
        print(f"\n🔄 HVDC 프로젝트 채팅방 추출 시작")
        print(f"📱 대상 채팅방: {len(self.hvdc_chats)}개")
        print("=" * 60)
        
        results = []
        from playwright.async_api import TimeoutError, Error   # S‑08

        # 공유 세션 사용
        context = await get_shared_session()
        page = await context.new_page()
        
        try:
            # WhatsApp Web 접속 및 로그인
            await page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded")
            
            # 로그인 상태 확인
            try:
                await page.wait_for_selector("#side", timeout=10000)
                print("✅ 이미 로그인된 상태")
            except:
                print("⚠️ WhatsApp 웹에 접속합니다. QR 코드를 스캔하여 로그인해주세요 (2분 제한).")
                await page.wait_for_selector("#side", timeout=120000)
                print("✅ 로그인 성공!")

            for chat_title in self.hvdc_chats:
                print(f"\n📱 채팅방 처리 중: {chat_title}")
                try:
                    result = await self.extract_single_chat(page, chat_title)
                    results.append(result)
                    
                    if result['status'] == 'SUCCESS':
                        print(f"✅ 추출 성공: {result['message_count']}개 메시지")
                    else:
                        print(f"❌ 추출 실패: {result.get('error', 'Unknown error')}")
                    
                    await asyncio.sleep(2) # 채팅방 간 짧은 대기
                    
                except Exception as e:
                    error_message = f"처리 중 예외 발생: {str(e)}"
                    print(f"❌ {error_message}")
                    results.append({
                        'status': 'ERROR', 'chat_title': chat_title, 'error': error_message,
                        'timestamp': datetime.now().isoformat()
                    })

        except TimeoutError:
            print("❌ 로그인 시간(2분)이 초과되었습니다. QR 코드 스캔을 다시 시도해주세요.")
            logger.error("Login timeout exceeded.")
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            logger.error(f"Browser automation error: {str(e)}")
        # 세션 유지 - 종료 호출 제거
        
        return results
    
    async def extract_single_chat(self, page, chat_title: str):
        """단일 채팅방 추출 (이모지 제거 + 텍스트 정규화)"""
        try:
            # 검색창 찾기 및 활성화
            search_box = await self.find_and_activate_search_box(page)
            
            # 검색어 입력
            await self.input_search_text(page, search_box, chat_title)
            await page.wait_for_timeout(2000)
            
            # Enter 키로 검색 실행
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            
            # 정규화된 텍스트로 채팅방 찾기
            chat_element = await self.find_chat_by_normalized_text(page, chat_title)
            
            if not chat_element:
                print(f"❌ 채팅방을 찾을 수 없음: {chat_title}")
                return {
                    'status': 'ERROR',
                    'chat_title': chat_title,
                    'error': 'Chat room not found',
                    'timestamp': datetime.now().isoformat()
                }
            
            # 채팅방 클릭
            await chat_element.click()
            print(f"✅ 채팅방 선택: {chat_title}")
            
            # 메시지 로딩 대기
            await page.wait_for_timeout(3000)
            
            # 메시지 추출 (다중 셀렉터 사용)
            message_selectors = [
                '[data-testid="conversation-panel-messages"] .message-in, [data-testid="conversation-panel-messages"] .message-out',
                '[data-testid="msg-meta"]',
                'div[role="row"]:has([data-testid="msg-meta"])',
                '.message-in, .message-out',
                '[data-testid*="message"]',  # 최신 메시지 셀렉터
                'div[role="row"]'  # 대안 메시지 셀렉터
            ]
            
            messages = []
            for selector in message_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        for element in elements:
                            text = await element.text_content()
                            if text and text.strip():
                                messages.append(text.strip())
                        print(f"✅ 메시지 추출 성공: {len(messages)}개")
                        break
                except Exception as e:
                    print(f"⚠️ 메시지 셀렉터 실패: {selector}")
                    continue
            
            # 빈 메시지 필터링
            filtered_messages = [msg for msg in messages if msg.strip()]
            
            # HVDC 관련 키워드 필터링
            hvdc_keywords = ['HVDC', '물류', 'logistics', 'project', 'abudhabi', 'storage', 'panel', 'AGI']
            relevant_messages = []
            
            for msg in filtered_messages:
                if any(keyword.lower() in msg.lower() for keyword in hvdc_keywords):
                    relevant_messages.append(msg)
            
            result = {
                'status': 'SUCCESS',
                'chat_title': chat_title,
                'normalized_title': self.sanitize_text(chat_title),
                'messages': filtered_messages,
                'relevant_messages': relevant_messages,
                'message_count': len(filtered_messages),
                'relevant_count': len(relevant_messages),
                'extraction_time': datetime.now().isoformat(),
                'confidence': len(filtered_messages) / 100.0
            }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 추출 중 오류: {str(e)}")
            return {
                'status': 'ERROR',
                'chat_title': chat_title,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def save_results(self, results: list):
        """결과 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"data/hvdc_whatsapp_extraction_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 결과 저장: {output_file}")
        return output_file

async def main():
    """메인 실행 함수"""
    print("🤖 MACHO-GPT v3.4-mini HVDC WhatsApp 추출 (이모지 제거 + 텍스트 정규화)")
    print("=" * 60)
    print(f"📅 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 모드: LATTICE (OCR 및 자동화)")
    print(f"🏢 프로젝트: Samsung C&T Logistics · HVDC")
    print("=" * 60)
    
    extractor = HVDCWhatsAppExtractor()
    
    try:
        # HVDC 채팅방들 추출
        results = await extractor.extract_hvdc_chats()
        
        # 결과 요약
        print("\n📊 추출 결과 요약:")
        success_count = 0
        total_messages = 0
        total_relevant = 0
        
        for result in results:
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            print(f"  {status_icon} {result['chat_title']}: {result['status']}")
            
            if result['status'] == 'SUCCESS':
                success_count += 1
                total_messages += result['message_count']
                total_relevant += result['relevant_count']
                print(f"     📊 전체: {result['message_count']}개, 관련: {result['relevant_count']}개")
        
        print(f"\n📈 전체 통계:")
        print(f"   - 성공한 채팅방: {success_count}/{len(results)}개")
        print(f"   - 총 메시지: {total_messages}개")
        print(f"   - 관련 메시지: {total_relevant}개")
        
        # 결과 저장
        if results:
            output_file = extractor.save_results(results)
            print(f"✅ HVDC WhatsApp 추출 완료!")
            print(f"📁 결과 파일: {output_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"❌ 실행 중 오류: {str(e)}")
        print(f"❌ 오류 발생: {str(e)}")
    
    print("\n🎉 HVDC WhatsApp 추출 완료")

if __name__ == "__main__":
    asyncio.run(main()) 