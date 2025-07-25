#!/usr/bin/env python3
"""
WhatsApp Media OCR Extractor
MACHO-GPT v3.4-mini for HVDC Project
성공적인 whatsapp_rpa_hvdc_extract.py 접근법 적용
"""

import asyncio
import json
import os
import re
import hashlib
import unicodedata
import warnings
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import sys

# Google Cloud Vision import
try:
    from google.cloud import vision
    GCV_AVAILABLE = True
except ImportError:
    GCV_AVAILABLE = False
    print("⚠️ Google Cloud Vision not available")

# EasyOCR UserWarning 해결
warnings.filterwarnings(
    "ignore",
    message=".*pin_memory.*no accelerator.*",
    category=UserWarning,
    module="torch.utils.data"
)

# Playwright imports
from playwright.async_api import async_playwright, Page, Browser

# OCR imports
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_unique_user_data_dir(chat_name: str) -> str:
    """
    채팅방별 고유한 user_data_dir 경로 생성
    
    Args:
        chat_name: 채팅방 이름
        
    Returns:
        str: 고유한 user_data_dir 경로
    """
    # 채팅방 이름을 해시하여 고유한 디렉토리 생성
    hashed_name = hashlib.sha256(chat_name.encode('utf-8')).hexdigest()[:16]
    user_data_dir = os.path.join("browser_data", f"chat_{hashed_name}")
    
    # 디렉토리 생성
    os.makedirs(user_data_dir, exist_ok=True)
    
    return user_data_dir

class MediaOCRProcessor:
    """미디어 파일 OCR 처리 클래스"""
    
    def __init__(self, max_file_size_mb: int = 5):
        self.max_file_size_mb = max_file_size_mb
        self.processed_files = set()
        
        # EasyOCR 초기화 (CPU 최적화)
        if EASYOCR_AVAILABLE:
            # CPU 전용 설정으로 UserWarning 방지
            self.easyocr_reader = easyocr.Reader(
                ['ko', 'en'],
                gpu=False,  # CPU 전용 모드
                verbose=False  # 불필요한 로그 제거
            )
        else:
            self.easyocr_reader = None
            logger.warning("EasyOCR not available")
    
    def get_file_hash(self, file_path: str) -> str:
        """파일 해시 생성"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def sanitize_ocr_text(self, text: str) -> str:
        """OCR 텍스트 정제"""
        if not text:
            return ""
        
        # 개인정보 마스킹
        patterns = {
            r'\b\d{3}-\d{4}-\d{4}\b': '[PHONE]',
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': '[EMAIL]',
            r'\b\d{6}-\d{7}\b': '[ID_NUMBER]',
            r'\b\d{4}-\d{4}-\d{4}-\d{4}\b': '[CARD_NUMBER]'
        }
        
        for pattern, replacement in patterns.items():
            text = re.sub(pattern, replacement, text)
        
        return text.strip()
    
    async def process_image(self, file_path: str, engine: str = "easyocr") -> Dict[str, Any]:
        """이미지 OCR 처리"""
        try:
            if engine == "gcv":
                # Google Cloud Vision API 사용
                try:
                    from google_vision_ocr_patch import create_gcv_client
                    client = create_gcv_client()
                    
                    with open(file_path, 'rb') as image_file:
                        content = image_file.read()
                    
                    image = vision.Image(content=content)
                    response = client.text_detection(image=image)
                    
                    if response.error.message:
                        return {
                            'error': response.error.message,
                            'text': '',
                            'confidence': 0.0,
                            'engine': 'gcv'
                        }
                    
                    texts = response.text_annotations
                    if texts:
                        text = texts[0].description
                        confidence = 0.95  # GCV는 높은 신뢰도
                        return {
                            'text': text,
                            'confidence': confidence,
                            'engine': 'gcv'
                        }
                    else:
                        return {
                            'error': 'No text detected',
                            'text': '',
                            'confidence': 0.0,
                            'engine': 'gcv'
                        }
                        
                except Exception as e:
                    return {
                        'error': f'Google Cloud Vision API error: {str(e)}',
                        'text': '',
                        'confidence': 0.0,
                        'engine': 'gcv'
                    }
            else:
                # EasyOCR 사용
                if not self.easyocr_reader:
                    return {
                        'error': 'EasyOCR not available',
                        'text': '',
                        'confidence': 0.0,
                        'engine': 'easyocr'
                    }
                
                result = self.easyocr_reader.readtext(file_path)
                if result:
                    text = ' '.join([item[1] for item in result])
                    confidence = sum([item[2] for item in result]) / len(result)
                    return {
                        'text': text,
                        'confidence': confidence,
                        'engine': 'easyocr'
                    }
                else:
                    return {
                        'error': 'No text detected',
                        'text': '',
                        'confidence': 0.0,
                        'engine': 'easyocr'
                    }
                    
        except Exception as e:
            return {
                'error': str(e),
                'text': '',
                'confidence': 0.0,
                'engine': engine
            }
    
    async def _process_with_easyocr(self, image_path: str) -> Dict[str, Any]:
        """EasyOCR로 이미지 처리"""
        try:
            results = self.easyocr_reader.readtext(image_path)
            text_parts = []
            total_confidence = 0.0
            
            for (bbox, text, confidence) in results:
                text_parts.append(text)
                total_confidence += confidence
            
            full_text = ' '.join(text_parts)
            avg_confidence = total_confidence / len(results) if results else 0.0
            
            sanitized_text = self.sanitize_ocr_text(full_text)
            
            return {
                'text': sanitized_text,
                'confidence': avg_confidence,
                'engine': 'easyocr',
                'raw_results': results
            }
        except Exception as e:
            logger.error(f"EasyOCR processing error: {e}")
            return {
                'error': str(e),
                'text': '',
                'confidence': 0.0,
                'engine': 'easyocr'
            }
    
    async def _process_with_gcv(self, image_path: str) -> Dict[str, Any]:
        """Google Cloud Vision으로 이미지 처리"""
        try:
            # Google Cloud Vision API 클라이언트 생성
            client = vision.ImageAnnotatorClient()
            
            # 이미지 읽기
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # OCR 요청
            response = client.text_detection(image=image)
            
            if response.error.message:
                return {
                    'error': response.error.message,
                    'text': '',
                    'confidence': 0.0,
                    'engine': 'gcv'
                }
            
            # 결과 추출
            texts = response.text_annotations
            if texts:
                extracted_text = texts[0].description
                sanitized_text = self.sanitize_ocr_text(extracted_text)
                
                return {
                    'text': sanitized_text,
                    'confidence': 0.9,  # GCV 기본 신뢰도
                    'engine': 'gcv'
                }
            else:
                return {
                    'text': '',
                    'confidence': 0.0,
                    'engine': 'gcv'
                }
        except Exception as e:
            logger.error(f"Google Cloud Vision processing error: {e}")
            return {
                'error': str(e),
                'text': '',
                'confidence': 0.0,
                'engine': 'gcv'
            }

class WhatsAppMediaOCRExtractor:
    """WhatsApp 미디어 OCR 추출기 (성공적인 접근법 적용)"""
    
    def __init__(self, chat_name: str = "HVDC 물류팀"):
        self.chat_name = chat_name
        self.auth_file = "auth_backups/whatsapp_auth.json"
        self.ocr_processor = MediaOCRProcessor()
        
        # 채팅방별 고유한 user_data_dir 설정
        self.user_data_dir = get_unique_user_data_dir(chat_name)
        
        # 미디어 셀렉터들
        self.media_selectors = [
            'img[src*="blob:"]',
            'video[src*="blob:"]',
            'audio[src*="blob:"]',
            'div[data-testid="media-container"]'
        ]
        
        # 성공적인 접근법에서 가져온 셀렉터들
        self.BTN_SEARCH = 'button[aria-label="Search or start new chat"]'
        self.SEARCH_BOX_SELECTORS = [
            'div[role="searchbox"]',
            'div[contenteditable="true"]',
            'div[data-testid="search"]',
            'input[type="text"]'
        ]
        
        print(f"✅ WhatsApp Media OCR Extractor 초기화 완료 (채팅방: {chat_name})")
        print(f"📁 고유 세션 디렉토리: {self.user_data_dir}")
    
    def _deduplicate_browser_arguments(self, args: List[str]) -> List[str]:
        """
        브라우저 인수 중복 제거
        
        Args:
            args: 브라우저 인수 리스트
            
        Returns:
            List[str]: 중복이 제거된 인수 리스트
        """
        # Set을 사용하여 중복 제거 후 리스트로 변환
        unique_args = list(dict.fromkeys(args))  # 순서 보존
        return unique_args
    
    def _combine_browser_arguments(self, args_list_1: List[str], args_list_2: List[str]) -> List[str]:
        """
        두 개의 브라우저 인수 리스트를 결합하고 중복 제거
        
        Args:
            args_list_1: 첫 번째 인수 리스트
            args_list_2: 두 번째 인수 리스트
            
        Returns:
            List[str]: 결합되고 중복이 제거된 인수 리스트
        """
        # Set을 사용하여 중복 제거
        combined_set = set(args_list_1) | set(args_list_2)
        return list(combined_set)
    
    def _log_browser_arguments(self, args: List[str], context: str):
        """
        브라우저 인수 로깅
        
        Args:
            args: 브라우저 인수 리스트
            context: 컨텍스트 정보
        """
        print(f"🔧 Browser Arguments ({context}): {args}")
    
    def _get_browser_launch_config(self, headless: bool = False, ignore_default_args: List[str] = None) -> Dict[str, Any]:
        """
        브라우저 실행 설정 생성
        
        Args:
            headless: 헤드리스 모드 여부
            ignore_default_args: 무시할 기본 인수 리스트
            
        Returns:
            Dict[str, Any]: 브라우저 실행 설정
        """
        config = {
            "headless": headless,
            "user_data_dir": self.user_data_dir,
            "timeout": 300000,
            "args": ["--no-sandbox", "--disable-dev-shm-usage"],
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "viewport": {"width": 1280, "height": 900},
            "ignore_https_errors": True
        }
        
        if ignore_default_args:
            config["ignore_default_args"] = ignore_default_args
            
        return config
    
    def _validate_browser_arguments(self, args: List[str]) -> List[str]:
        """
        브라우저 인수 형식 검증
        
        Args:
            args: 검증할 인수 리스트
            
        Returns:
            List[str]: 유효한 인수만 포함된 리스트
        """
        valid_args = []
        for arg in args:
            # --로 시작하고 값이 있는지 확인
            if arg.startswith("--") and len(arg) > 2:
                # =이 포함된 경우 값이 있는지 확인
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    # 값이 비어있지 않고 'invalid'가 아닌 경우만 유효
                    if value and value.strip() and value.strip() != "invalid":
                        valid_args.append(arg)
                else:
                    # =이 없는 경우 단순히 --로 시작하고 길이가 충분하면 유효
                    valid_args.append(arg)
        return valid_args
    
    def _cleanup_session_directory(self):
        """세션 디렉토리 정리"""
        import shutil
        try:
            shutil.rmtree(self.user_data_dir, ignore_errors=True)
            print(f"🧹 세션 디렉토리 정리 완료: {self.user_data_dir}")
        except Exception as e:
            print(f"⚠️ 세션 디렉토리 정리 실패: {str(e)}")
    
    async def _safe_close_context(self, context):
        """안전한 컨텍스트 종료"""
        try:
            if context and not context.is_closed():
                await context.close()
                print("✅ 브라우저 컨텍스트 안전 종료 완료")
        except Exception as e:
            print(f"⚠️ 브라우저 컨텍스트 종료 중 오류: {str(e)}")
    
    async def _monitor_browser_status(self, page, timeout: int = 30) -> bool:
        """브라우저 상태 모니터링"""
        import asyncio
        start_time = asyncio.get_event_loop().time()
        
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            if page.is_closed():
                return False
            await asyncio.sleep(1)
        
        return True
    
    def _handle_critical_error(self, error: Exception):
        """치명적 오류 처리"""
        print(f"❌ 치명적 오류 발생: {str(error)}")
        self._cleanup_session_directory()
    
    def _log_system_info(self):
        """시스템 정보 로깅"""
        try:
            import playwright
            print(f"🔧 Playwright Version: {playwright.__version__}")
            print(f"🔧 Python Version: {sys.version}")
            print(f"🔧 User Data Directory: {self.user_data_dir}")
        except Exception as e:
            print(f"⚠️ 시스템 정보 로깅 실패: {str(e)}")
    
    async def _poll_browser_status(self, page, interval: float = 1.0, max_attempts: int = 10) -> bool:
        """브라우저 상태 폴링"""
        import asyncio
        for attempt in range(max_attempts):
            if page.is_closed():
                return False
            if attempt < max_attempts - 1:  # 마지막 시도에서는 대기하지 않음
                await asyncio.sleep(interval)
        return True
    
    def _log_debug_info(self, debug_info: Dict[str, Any]):
        """디버그 정보 로깅"""
        print("🔍 Debug Information:")
        for key, value in debug_info.items():
            print(f"  {key}: {value}")
    
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
    
    def sanitize_filename(self, filename: str) -> str:
        """파일명 정제"""
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    async def setup_browser_context(self, playwright):
        """브라우저 컨텍스트 설정 (완전히 새로운 안정 설정)"""
        import shutil
        
        try:
            print(f"🔄 완전히 새로운 브라우저 컨텍스트 설정 중...")
            print(f"📁 사용 디렉토리: {self.user_data_dir}")
            
            # Playwright 기본 설정 사용 (인수 최소화)
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=False,
                timeout=300000,  # 5분
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 900},
                ignore_https_errors=True
            )
            
            # 전역 타임아웃 설정
            context.set_default_timeout(300000)  # 5분
            context.set_default_navigation_timeout(300000)  # 5분
            
            print("✅ 완전히 새로운 브라우저 컨텍스트 설정 완료")
            return context
            
        except Exception as e:
            print(f"❌ 브라우저 컨텍스트 설정 실패: {str(e)}")
            # 디렉토리 정리
            try:
                shutil.rmtree(self.user_data_dir, ignore_errors=True)
            except:
                pass
            raise RuntimeError(f"브라우저 컨텍스트 설정 실패: {str(e)}")
    
    async def _setup_non_persistent_context(self, playwright):
        """비-Persistent Context 설정 (Fallback) - 더 이상 사용하지 않음"""
        # 이 메서드는 더 이상 사용하지 않음
        raise RuntimeError("Fallback 메서드는 더 이상 사용하지 않습니다.")
    
    async def find_and_activate_search_box(self, page):
        """돋보기 버튼 클릭 후 검색창 찾기 및 활성화"""
        try:
            # 1단계: 돋보기 버튼 클릭
            print("🔍 돋보기 버튼 클릭 중...")
            await page.click(self.BTN_SEARCH, timeout=5000)
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
        
        # 2단계: contenteditable 검색창 찾기
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
        """검색어 입력"""
        try:
            # 방법 1: click() + type() 조합
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
        """키워드 토큰화 기반 채팅방 찾기"""
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
            
            # 방법 2: XPath with translate()
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
            
            # 방법 3: CSS 셀렉터 백업
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
        
        return None
    
    async def find_media_messages(self, page: Page, chat_name: str) -> List[Any]:
        """미디어 메시지 찾기 (성공적인 접근법 적용)"""
        try:
            print(f"🔍 채팅방 검색: {chat_name}")
            
            # 검색창 찾기 및 활성화
            search_box = await self.find_and_activate_search_box(page)
            
            # 검색어 입력
            await self.input_search_text(page, search_box, chat_name)
            await page.wait_for_timeout(2000)
            
            # Enter 키로 검색 실행
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            
            # 정규화된 텍스트로 채팅방 찾기
            chat_element = await self.find_chat_by_normalized_text(page, chat_name)
            
            if not chat_element:
                print(f"❌ 채팅방을 찾을 수 없음: {chat_name}")
                return []
            
            # 채팅방 클릭
            await chat_element.click()
            print(f"✅ 채팅방 선택: {chat_name}")
            
            # 메시지 로딩 대기
            await page.wait_for_timeout(3000)
            
            # 미디어 메시지 찾기
            media_elements = []
            for selector in self.media_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"✅ 미디어 요소 발견: {len(elements)}개 ({selector})")
                        media_elements.extend(elements)
                except Exception as e:
                    print(f"⚠️ 셀렉터 실패: {selector}")
                    continue
            
            print(f"📊 총 미디어 요소: {len(media_elements)}개")
            return media_elements
            
        except Exception as e:
            logger.error(f"Error finding media messages: {e}")
            return []
    
    async def download_media(self, element: Any, download_dir: str) -> Optional[str]:
        """미디어 파일 다운로드"""
        try:
            # 다운로드 디렉토리 생성
            os.makedirs(download_dir, exist_ok=True)
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_media_{timestamp}.jpg"
            filepath = os.path.join(download_dir, filename)
            
            # 파일 다운로드
            await element.screenshot(path=filepath)
            
            return filepath
        except Exception as e:
            logger.error(f"Error downloading media: {e}")
            return None
    
    async def process_media_file(self, file_path: str, engine: str = "easyocr") -> Dict[str, Any]:
        """미디어 파일 처리"""
        try:
            # 파일 해시 확인
            file_hash = self.ocr_processor.get_file_hash(file_path)
            if file_hash in self.ocr_processor.processed_files:
                return {'error': 'File already processed', 'text': '', 'confidence': 0.0}
            
            # OCR 처리
            result = await self.ocr_processor.process_image(file_path, engine)
            
            # 처리된 파일 기록
            self.ocr_processor.processed_files.add(file_hash)
            
            return result
        except Exception as e:
            logger.error(f"Error processing media file: {e}")
            return {'error': str(e), 'text': '', 'confidence': 0.0}
    
    async def save_results(self, results: List[Dict[str, Any]], output_file: str):
        """결과 저장"""
        try:
            output_data = {
                'timestamp': datetime.now().isoformat(),
                'total_processed': len(results),
                'successful': len([r for r in results if 'error' not in r]),
                'results': results
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")

async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp Media OCR Extractor")
    parser.add_argument("--chat", default="HVDC 물류팀", help="Chat name to extract media from")
    parser.add_argument("--media-only", action="store_true", help="Extract media only")
    parser.add_argument("--ocr-engine", default="easyocr", choices=["easyocr", "gcv"], help="OCR engine to use")
    parser.add_argument("--max-media", type=int, default=10, help="Maximum number of media files to process")
    parser.add_argument("--output", default="data/whatsapp_media_ocr_results.json", help="Output file path")
    
    args = parser.parse_args()
    
    # 출력 디렉토리 생성
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    extractor = WhatsAppMediaOCRExtractor(args.chat)
    context = None
    
    try:
        async with async_playwright() as p:
            print("🔄 Playwright 초기화 중...")
            context = await extractor.setup_browser_context(p)
            
            # launch_persistent_context는 이미 페이지를 포함하므로 새로 생성하지 않음
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("🌐 WhatsApp Web 접속 중...")
            # WhatsApp Web 접속
            await page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded", timeout=300000)
            print("✅ WhatsApp Web 접속 완료")
            
            # 로그인 상태 확인 (완전히 새로운 방식)
            print("🔍 로그인 상태 확인 중...")
            login_success = False
            
            try:
                # 브라우저가 닫혔는지 먼저 확인
                if page.is_closed():
                    raise RuntimeError("브라우저가 닫혔습니다.")
                
                # 먼저 짧은 시간으로 확인
                await page.wait_for_selector("#side", timeout=15000)
                print("✅ 이미 로그인된 상태")
                login_success = True
            except Exception as initial_check_error:
                print(f"⚠️ 초기 로그인 확인 실패: {str(initial_check_error)}")
                print("⚠️ 로그인이 필요합니다. QR 코드를 스캔해주세요 (3분 제한).")
                
                # 브라우저가 닫히지 않았는지 확인하면서 대기
                try:
                    # 더 짧은 시간으로 대기 (3분)
                    await page.wait_for_selector("#side", timeout=180000)  # 3분
                    print("✅ 로그인 성공!")
                    login_success = True
                except Exception as login_error:
                    print(f"❌ 로그인 타임아웃: {str(login_error)}")
                    raise RuntimeError("로그인에 실패했습니다. QR 코드를 스캔해주세요.")
            
            if not login_success:
                raise RuntimeError("로그인 상태를 확인할 수 없습니다.")
            
            # 페이지가 완전히 로드될 때까지 대기
            await page.wait_for_timeout(3000)  # 3초 대기
            
            # 미디어 메시지 찾기
            print(f"🔍 채팅방 '{args.chat}'에서 미디어 검색 중...")
            media_elements = await extractor.find_media_messages(page, args.chat)
            
            if not media_elements:
                print("⚠️ 미디어 메시지를 찾을 수 없습니다.")
                return
            
            print(f"📱 발견된 미디어: {len(media_elements)}개")
            
            # 미디어 처리
            results = []
            download_dir = "downloads"
            
            for i, element in enumerate(media_elements[:args.max_media]):
                print(f"📱 미디어 처리 중... ({i+1}/{min(len(media_elements), args.max_media)})")
                
                try:
                    # 미디어 다운로드
                    file_path = await extractor.download_media(element, download_dir)
                    if not file_path:
                        continue
                    
                    # OCR 처리
                    result = await extractor.process_media_file(file_path, args.ocr_engine)
                    result['file_path'] = file_path
                    results.append(result)
                    
                    print(f"✅ 미디어 {i+1} 처리 완료")
                    
                except Exception as e:
                    print(f"❌ 미디어 {i+1} 처리 실패: {str(e)}")
                    results.append({
                        'error': str(e),
                        'file_path': 'unknown',
                        'confidence': 0.0
                    })
            
            # 결과 저장
            await extractor.save_results(results, args.output)
            
            print(f"✅ 미디어 OCR 처리 완료! 결과 저장: {args.output}")
            print(f"📊 처리 결과: {len(results)}개 중 {len([r for r in results if 'error' not in r])}개 성공")
            
    except Exception as e:
        logger.error(f"❌ 실행 중 오류 발생: {str(e)}")
        print(f"❌ 오류 발생: {str(e)}")
        
        # 오류 발생 시에도 결과 저장 시도
        try:
            error_result = {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'total_processed': 0,
                'successful': 0,
                'results': []
            }
            
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(error_result, f, ensure_ascii=False, indent=2)
            
            print(f"⚠️ 오류 정보 저장: {args.output}")
        except:
            pass
    
    finally:
        # 브라우저 정리
        try:
            if context:
                await context.close()
                print("✅ 브라우저 컨텍스트 정리 완료")
        except Exception as e:
            print(f"⚠️ 브라우저 정리 중 오류: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 