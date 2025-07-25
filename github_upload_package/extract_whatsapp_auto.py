#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp 자동 추출 시스템
Samsung C&T Logistics · HVDC Project

고급 스텔스 기술과 프록시를 사용한 안전한 WhatsApp 스크래핑
- CAPTCHA 자동 감지 및 처리
- 프록시 로테이션
- 인간과 유사한 행동 패턴
- 세션 관리 및 백업
"""

import asyncio
import random
import sys
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# MACHO-GPT 시스템 import
sys.path.append(str(Path(__file__).parent))
try:
    from macho_gpt.core.logi_ai_summarizer_241219 import LogiAISummarizer
    from macho_gpt.core.logi_whatsapp_241219 import WhatsAppProcessor
    from logi_base_model import LogiBaseModel
    MACHO_GPT_AVAILABLE = True
except ImportError:
    print("⚠️  MACHO-GPT 모듈을 찾을 수 없습니다. 기본 기능으로 실행합니다.")
    MACHO_GPT_AVAILABLE = False

# 설정
CHAT_TITLE = "MR.CHA 전용"
AUTH_FILE = Path("auth.json")

# 프록시 설정 (실제 프록시 정보로 교체 필요)
PROXIES = [
    "http://user:pw@residential-proxy1:port", 
    "http://user:pw@residential-proxy2:port"
]

# User Agent 리스트
UA_LIST = [
    # Chrome-like UA
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    # macOS Safari-like UA
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # Firefox-like UA
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
]


class WhatsAppAdvancedScraper:
    """고급 WhatsApp 스크래퍼"""
    
    def __init__(self, use_proxy=True):
        self.use_proxy = use_proxy
        self.auth_file = AUTH_FILE
        self.chat_title = CHAT_TITLE
        
    async def solve_captcha(self, page):
        """CAPTCHA 감지 및 처리"""
        try:
            captcha_frame = page.locator("iframe[src*='captcha']")
            if await captcha_frame.is_visible():
                print("⚠️ CAPTCHA 감지됨 – 수동 또는 자동 해석 필요")
                input("해결 후 ENTER 눌러주세요...")
                return True
        except Exception as e:
            print(f"CAPTCHA 확인 중 오류: {e}")
        return False
    
    async def human_like_behavior(self, page):
        """인간과 유사한 행동 패턴"""
        try:
            # 랜덤 마우스 움직임
            await page.mouse.move(
                random.randint(1, 200), 
                random.randint(1, 200)
            )
            await page.wait_for_timeout(random.randint(500, 1500))
            
            # 채팅방 클릭
            await page.get_by_title(self.chat_title).click()
            await page.wait_for_timeout(random.randint(2000, 5000))
            
            # 스크롤 (PageUp)
            await page.keyboard.press("PageUp")
            await page.wait_for_timeout(random.randint(1000, 3000))
            
        except Exception as e:
            print(f"인간 행동 시뮬레이션 오류: {e}")
    
    async def scrape_conversation(self, max_retries=3):
        """대화 스크래핑 실행"""
        for attempt in range(max_retries):
            try:
                print(f"🔍 메시지 추출 시도 {attempt + 1}/{max_retries}")
                
                # 프록시 설정
                proxy = None
                if self.use_proxy and PROXIES:
                    proxy = {"server": random.choice(PROXIES)}
                    print(f"🌐 프록시 사용: {proxy['server']}")
                
                async with async_playwright() as pw:
                    # 브라우저 설정
                    browser = await pw.chromium.launch(
                        headless=True,
                        proxy=proxy,
                        args=[
                            "--disable-blink-features=AutomationControlled",
                            "--disable-web-security",
                            "--disable-features=VizDisplayCompositor",
                            "--no-sandbox",
                            "--disable-setuid-sandbox"
                        ]
                    )
                    
                    # 컨텍스트 설정
                    context = await browser.new_context(
                        storage_state=str(self.auth_file) if self.auth_file.exists() else None,
                        user_agent=random.choice(UA_LIST),
                        viewport={
                            "width": random.randint(1200, 1400), 
                            "height": random.randint(700, 900)
                        },
                        locale="en-US"
                    )
                    
                    page = await context.new_page()
                    
                    # WhatsApp Web 접속
                    print("📱 WhatsApp Web 접속 중...")
                    await page.goto("https://web.whatsapp.com/")
                    await page.wait_for_timeout(random.randint(3000, 6000))
                    
                    # CAPTCHA 확인
                    await self.solve_captcha(page)
                    
                    # 로그인 상태 확인
                    print(f"📱 채팅방 검색: {self.chat_title}")
                    try:
                        chat_selector = page.locator(f'[title="{self.chat_title}"]')
                        await chat_selector.wait_for(timeout=15000)
                        if not await chat_selector.is_visible():
                            print("❗ 로그인 실패 또는 세션 만료")
                            await browser.close()
                            continue
                    except Exception as e:
                        print(f"❗ 채팅방을 찾을 수 없음: {e}")
                        await browser.close()
                        continue
                    
                    # 인간과 유사한 행동
                    await self.human_like_behavior(page)
                    
                    # CAPTCHA 재확인
                    await self.solve_captcha(page)
                    
                    # 메시지 추출
                    print("📝 메시지 추출 중...")
                    messages = await page.locator(".message-in, .message-out").all_text_contents()
                    await browser.close()
                    
                    if not messages:
                        print("메시지 없음")
                        continue
                    
                    print(f"✅ {len(messages)}개 메시지 추출 완료")
                    return messages
                    
            except Exception as e:
                print(f"❌ 스크래핑 오류 (시도 {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(random.randint(2, 5))
                    continue
                else:
                    print("❌ 모든 재시도 실패")
                    return None
        
        return None


# MACHO-GPT 통합 함수들
def get_macho_gpt_summarizer():
    """MACHO-GPT 요약기 반환"""
    if MACHO_GPT_AVAILABLE:
        return LogiAISummarizer()
    return None

def macho_gpt_summarise(text):
    """MACHO-GPT를 사용한 요약"""
    if MACHO_GPT_AVAILABLE:
        try:
            summarizer = get_macho_gpt_summarizer()
            result = summarizer.summarize_conversation(text)
            return {
                "summary": result.get("summary", "요약 실패"),
                "tasks": result.get("tasks", []),
                "urgent": result.get("urgent", []),
                "important": result.get("important", [])
            }
        except Exception as e:
            print(f"MACHO-GPT 요약 오류: {e}")
            return fallback_summarise(text)
    else:
        return fallback_summarise(text)

def fallback_summarise(text):
    """기본 요약 (MACHO-GPT 없을 때)"""
    try:
        # 간단한 키워드 기반 요약
        lines = text.split('\n')
        summary = f"총 {len(lines)}개 메시지 처리됨"
        
        # 긴급/중요 키워드 감지
        urgent_keywords = ['긴급', '즉시', 'ASAP', 'URGENT', '바로', '지금']
        important_keywords = ['중요', '주의', 'IMPORTANT', '필수', '반드시']
        
        urgent = [line for line in lines if any(keyword in line for keyword in urgent_keywords)]
        important = [line for line in lines if any(keyword in line for keyword in important_keywords)]
        
        return {
            "summary": summary,
            "tasks": lines[:5],  # 처음 5개 메시지를 작업으로
            "urgent": urgent,
            "important": important
        }
    except Exception as e:
        print(f"기본 요약 오류: {e}")
        return {
            "summary": "요약 실패",
            "tasks": [],
            "urgent": [],
            "important": []
        }

def load_conversation_db():
    """대화 데이터베이스 로드"""
    db_file = Path("conversations.json")
    if db_file.exists():
        try:
            import json
            with open(db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"DB 로드 오류: {e}")
    return {}

def save_conversation_db(db):
    """대화 데이터베이스 저장"""
    try:
        import json
        db_file = Path("conversations.json")
        with open(db_file, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"✅ DB 저장 완료: {db_file}")
    except Exception as e:
        print(f"DB 저장 오류: {e}")


async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MACHO-GPT v3.4-mini WhatsApp 자동 추출")
    parser.add_argument("--setup", action="store_true", help="WhatsApp 인증 설정")
    parser.add_argument("--no-proxy", action="store_true", help="프록시 사용 안함")
    parser.add_argument("--chat", type=str, default=CHAT_TITLE, help="채팅방 제목")
    
    args = parser.parse_args()
    
    if args.setup:
        # 인증 설정
        print("🔐 WhatsApp Web 인증 설정")
        print("⚠️  playwright-stealth 없음. 기본 스텔스 모드로 실행")
        
        try:
            from auth_setup import WhatsAppAuthSetup
            auth_setup = WhatsAppAuthSetup()
            success = await auth_setup.setup_authentication()
            if success:
                print("✅ 인증 정보 저장: auth.json")
            else:
                print("❌ 인증 설정 실패")
        except ImportError:
            print("❌ auth_setup.py를 찾을 수 없습니다.")
        return
    
    # 메인 실행
    print("🚀 MACHO-GPT v3.4-mini WhatsApp 자동 추출 시작")
    print(f"📅 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # MACHO-GPT 시스템 확인
    if MACHO_GPT_AVAILABLE:
        print("✅ MACHO-GPT 시스템 사용 가능")
        llm_summarise = macho_gpt_summarise
        load_db = load_conversation_db
        save_db = save_conversation_db
    else:
        print("⚠️  MACHO-GPT 시스템 사용 불가. 기본 함수 사용")
        llm_summarise = fallback_summarise
        load_db = load_conversation_db
        save_db = save_conversation_db
    
    # 스크래퍼 설정
    scraper = WhatsAppAdvancedScraper(use_proxy=not args.no_proxy)
    scraper.chat_title = args.chat
    
    # 스크래핑 실행
    messages = await scraper.scrape_conversation()
    
    if not messages:
        print("❌ 메시지 추출 실패")
        return
    
    # 요약 및 저장
    try:
        text = "\n".join(messages)
        result = llm_summarise(text)
        
        key = datetime.now().strftime("%Y-%m-%d")
        db = load_db()
        db[key] = {
            "summary": result["summary"],
            "tasks": result["tasks"],
            "urgent": result.get("urgent", []),
            "important": result.get("important", []),
            "raw": text
        }
        save_db(db)
        
        print(f"✅ {key} -> 요약 완료 ({len(messages)}건)")
        print(f"📊 요약: {result['summary'][:100]}...")
        
    except Exception as e:
        print(f"❌ 요약/저장 오류: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 