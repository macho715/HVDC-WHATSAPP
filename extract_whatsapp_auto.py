#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp 자동 추출 스크립트
Samsung C&T Logistics · HVDC Project Integration

Features:
- 강화된 봇 탐지 회피 (Bot Detection Avoidance)
- 인간적 행동 패턴 모방 (Human-like Behavior)
- 오류 복구 및 재시도 메커니즘 (Error Recovery)
- 멀티 UA 로테이션 (User-Agent Rotation)
- 세션 관리 (Session Management)
"""

import asyncio
import random
import sys
from pathlib import Path
from datetime import datetime
import json
import traceback
import time
from whatsapp_summary_app import llm_summarise, load_db, save_db

# 설정 상수
CHAT_TITLE = "MR.CHA 전용"
AUTH_FILE = Path("auth.json")
MAX_RETRIES = 3
CONFIDENCE_THRESHOLD = 0.90

# 다양한 User Agent 문자열 (실제 브라우저 통계 기반)
UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0"
]

# 기본 함수들 (whatsapp_summary_app.py에서 import할 수 없는 경우 대비)
def safe_import():
    """안전한 모듈 import"""
    try:
        from whatsapp_summary_app import llm_summarise, load_db, save_db
        return llm_summarise, load_db, save_db
    except ImportError as e:
        print(f"⚠️  모듈 import 오류: {e}")
        return None, None, None

def fallback_llm_summarise(text: str) -> dict:
    """대체 요약 함수"""
    lines = text.split('\\n')
    total_messages = len(lines)
    
    # 간단한 키워드 추출
    keywords = []
    for line in lines:
        if any(word in line.lower() for word in ['긴급', '중요', '완료', '확인', '검토', '승인']):
            keywords.append(line.strip())
    
    return {
        'summary': f"WhatsApp 대화 요약 (총 {total_messages}개 메시지)\\n주요 키워드: {', '.join(keywords[:5])}",
        'tasks': keywords[:3] if keywords else ["대화 내용 검토 필요"],
        'confidence': 0.75
    }

def fallback_load_db() -> dict:
    """대체 DB 로딩"""
    try:
        with open('summaries.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def fallback_save_db(db: dict):
    """대체 DB 저장"""
    try:
        with open('summaries.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"DB 저장 오류: {e}")

async def init_browser():
    """브라우저 초기화 with 스텔스 모드"""
    try:
        # 동적 import로 오류 방지
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print("❌ Playwright가 설치되지 않았습니다. 설치 명령:")
            print("pip install playwright")
            print("python -m playwright install")
            return None, None, None
        
        try:
            from playwright_stealth import stealth_async
        except ImportError:
            print("⚠️  playwright-stealth 없음. 기본 스텔스 모드로 실행")
            stealth_async = None
        
        # Playwright 초기화
        playwright = await async_playwright().start()
        
        # 브라우저 실행 (스텔스 모드)
        browser = await playwright.chromium.launch(
            headless=True,  # 헤드리스 모드 (봇 탐지 회피)
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor"
            ]
        )
        
        # 컨텍스트 생성 (인간적 설정)
        context = await browser.new_context(
            storage_state=str(AUTH_FILE) if AUTH_FILE.exists() else None,
            user_agent=random.choice(UA_LIST),
            viewport={"width": 1366, "height": 768},  # 일반적인 화면 크기
            locale="ko-KR",
            timezone_id="Asia/Seoul"
        )
        
        # 페이지 생성
        page = await context.new_page()
        
        # 스텔스 모드 적용
        if stealth_async:
            await stealth_async(page)
        
        # JavaScript 실행 (봇 탐지 회피)
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ko-KR', 'ko', 'en-US', 'en'],
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)
        
        return playwright, browser, page
        
    except Exception as e:
        print(f"❌ 브라우저 초기화 오류: {e}")
        return None, None, None

async def human_like_delay(min_ms: int = 1000, max_ms: int = 3000):
    """인간적 지연 시간"""
    delay = random.randint(min_ms, max_ms) / 1000.0
    await asyncio.sleep(delay)

async def extract_messages(page, chat_title: str, max_retries: int = 3):
    """메시지 추출 (재시도 메커니즘 포함)"""
    for attempt in range(max_retries):
        try:
            print(f"🔍 메시지 추출 시도 {attempt + 1}/{max_retries}")
            
            # WhatsApp Web 접속
            await page.goto("https://web.whatsapp.com/", wait_until="networkidle")
            await human_like_delay(3000, 5000)
            
            # 로그인 상태 확인
            if "post_logout=1" in page.url:
                print("❌ 세션 만료됨. 다시 로그인 필요")
                return None
            
            # 채팅방 찾기
            chat_selector = f'[title="{chat_title}"]'
            print(f"📱 채팅방 검색: {chat_title}")
            
            try:
                await page.wait_for_selector(chat_selector, timeout=30000)
            except Exception:
                print(f"❌ 채팅방 '{chat_title}' 찾을 수 없음")
                continue
            
            # 채팅방 클릭
            await page.click(chat_selector)
            await human_like_delay(2000, 4000)
            
            # 인간적 스크롤 행동
            print("📜 메시지 로딩 중...")
            for _ in range(3):
                await page.keyboard.press('PageUp')
                await human_like_delay(800, 1500)
            
            # 메시지 선택자 (더 포괄적)
            message_selectors = [
                ".message-in .copyable-text",
                ".message-out .copyable-text",
                "[data-testid='conversation-panel-messages'] .copyable-text",
                "div[data-testid='msg-container'] .copyable-text"
            ]
            
            messages = []
            for selector in message_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements:
                        text = await element.text_content()
                        if text and text.strip():
                            messages.append(text.strip())
                except Exception as e:
                    print(f"⚠️  선택자 {selector} 오류: {e}")
                    continue
            
            # 중복 제거
            messages = list(dict.fromkeys(messages))
            
            if messages:
                print(f"✅ 메시지 {len(messages)}개 추출 완료")
                return messages
            else:
                print("⚠️  메시지가 없습니다")
                await human_like_delay(2000, 4000)
                
        except Exception as e:
            print(f"❌ 추출 오류 {attempt + 1}/{max_retries}: {e}")
            await human_like_delay(3000, 5000)
            
    return None

async def main():
    """메인 실행 함수"""
    print("🚀 MACHO-GPT v3.4-mini WhatsApp 자동 추출 시작")
    print(f"📅 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 모듈 import 시도
    llm_summarise, load_db, save_db = safe_import()
    
    if not llm_summarise:
        print("⚠️  메인 모듈 사용 불가. 대체 함수 사용")
        llm_summarise = fallback_llm_summarise
        load_db = fallback_load_db
        save_db = fallback_save_db
    
    # 브라우저 초기화
    playwright, browser, page = await init_browser()
    
    if not browser:
        print("❌ 브라우저 초기화 실패. 종료합니다.")
        return
    
    try:
        # 메시지 추출
        messages = await extract_messages(page, CHAT_TITLE)
        
        if not messages:
            print("❌ 메시지 추출 실패")
            return
        
        # 메시지 정리
        text = "\\n".join(messages)
        print(f"📝 추출된 텍스트 길이: {len(text)} 문자")
        
        # AI 요약
        print("🤖 AI 요약 처리 중...")
        try:
            result = llm_summarise(text)
            confidence = result.get('confidence', 0.0)
            
            if confidence < CONFIDENCE_THRESHOLD:
                print(f"⚠️  신뢰도 {confidence:.2f} < {CONFIDENCE_THRESHOLD} (임계값)")
                
        except Exception as e:
            print(f"❌ 요약 오류: {e}")
            result = fallback_llm_summarise(text)
        
        # 데이터 저장
        key = datetime.now().strftime("%Y-%m-%d_%H-%M")
        try:
            db = load_db()
            db[key] = {
                "summary": result["summary"],
                "tasks": result["tasks"],
                "urgent": [],
                "important": [],
                "raw": text,
                "confidence": result.get("confidence", 0.75),
                "timestamp": datetime.now().isoformat(),
                "message_count": len(messages)
            }
            save_db(db)
            
            print(f"✅ 데이터 저장 완료: {key}")
            print(f"📊 요약: {result['summary'][:100]}...")
            print(f"📋 태스크: {len(result['tasks'])}개")
            
        except Exception as e:
            print(f"❌ 데이터 저장 오류: {e}")
            traceback.print_exc()
    
    finally:
        # 정리
        try:
            await browser.close()
            await playwright.stop()
            print("🔚 브라우저 종료 완료")
        except Exception as e:
            print(f"⚠️  브라우저 종료 오류: {e}")

def setup_authentication():
    """인증 설정 (QR 코드 스캔)"""
    print("🔐 WhatsApp Web 인증 설정")
    print("브라우저가 열리면 QR 코드를 스캔하세요.")
    
    import asyncio
    
    async def auth_setup():
        playwright, browser, page = await init_browser()
        
        if not browser:
            return
        
        try:
            await page.goto("https://web.whatsapp.com/")
            print("QR 코드 스캔 후 Enter를 눌러주세요...")
            input()
            
            # 인증 정보 저장
            storage_state = await page.context.storage_state()
            
            with open(AUTH_FILE, 'w', encoding='utf-8') as f:
                json.dump(storage_state, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 인증 정보 저장: {AUTH_FILE}")
            
        finally:
            await browser.close()
            await playwright.stop()
    
    asyncio.run(auth_setup())

if __name__ == "__main__":
    # 명령행 인자 처리
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_authentication()
    else:
        # 메인 실행
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\\n🛑 사용자 중단")
        except Exception as e:
            print(f"❌ 실행 오류: {e}")
            traceback.print_exc()
        finally:
            print("\\n🔧 **추천 명령어:**")
            print("/logi_master check [추출 결과 검증 - 신뢰도 및 데이터 품질 확인]")
            print("/visualize_data dashboard [실시간 KPI 대시보드 - 워크플로우 상태 모니터링]")
            print("/automate schedule [자동화 스케줄링 - 정기적 메시지 추출 설정]") 