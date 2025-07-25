#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp Scraper
Samsung C&T Logistics · HVDC Project

WhatsApp Web에서 대화를 자동으로 스크래핑하는 모듈
"""

import asyncio
import json
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from playwright.async_api import async_playwright
# playwright-stealth 제거하고 기본 Playwright 사용

import sys
sys.path.append(str(Path(__file__).parent.parent))

from logi_base_model import LogiBaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WhatsAppMessage(LogiBaseModel):
    """WhatsApp 메시지 모델 / WhatsApp message model"""
    
    content: str
    timestamp: str
    sender: str
    message_type: str = "text"  # text, file, image, etc.
    is_urgent: bool = False


class WhatsAppScraper:
    """WhatsApp 스크래퍼 / WhatsApp scraper"""
    
    def __init__(self, chat_title: str = "MR.CHA 전용"):
        self.chat_title = chat_title
        self.auth_file = Path("auth.json")
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
            "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        ]
        
    async def scrape_conversation(self, hours_back: int = 24) -> List[WhatsAppMessage]:
        """대화 스크래핑 / Scrape conversation"""
        try:
            logger.info(f"WhatsApp 대화 스크래핑 시작: {self.chat_title}")
            
            async with async_playwright() as p:
                # 브라우저 설정
                browser = await p.chromium.launch(
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                # 컨텍스트 설정
                context = await browser.new_context(
                    storage_state=self.auth_file if self.auth_file.exists() else None,
                    user_agent=random.choice(self.ua_list),
                    viewport={"width": 1280, "height": 720},
                    locale="en-US"
                )
                
                page = await context.new_page()
                # 기본 Playwright 사용 (stealth_async 제거)
                
                # WhatsApp Web 접속
                await page.goto("https://web.whatsapp.com/")
                logger.info("WhatsApp Web 접속 완료")
                
                # 채팅방 대기 및 선택
                await page.wait_for_selector(f'[title="{self.chat_title}"]', timeout=60000)
                logger.info(f"채팅방 발견: {self.chat_title}")
                
                # 사람처럼 클릭 + 랜덤 지연
                await page.get_by_title(self.chat_title).click()
                await page.wait_for_timeout(random.randint(2000, 5000))
                
                # 스크롤하여 과거 메시지 로드
                await self._scroll_for_messages(page, hours_back)
                
                # 메시지 추출
                messages = await self._extract_messages(page)
                
                await browser.close()
                
                logger.info(f"스크래핑 완료: {len(messages)}개 메시지")
                return messages
                
        except Exception as e:
            logger.error(f"WhatsApp 스크래핑 오류: {e}")
            return []
    
    async def _scroll_for_messages(self, page, hours_back: int):
        """메시지 로드를 위한 스크롤 / Scroll to load messages"""
        try:
            # 지정된 시간만큼 과거로 스크롤
            scroll_count = max(1, hours_back // 2)  # 2시간당 1번 스크롤
            
            for i in range(scroll_count):
                await page.keyboard.press('PageUp')
                await page.wait_for_timeout(random.randint(1000, 3000))
                
                # 로딩 대기
                try:
                    await page.wait_for_selector(".message-in, .message-out", timeout=5000)
                except:
                    break
                    
            logger.info(f"스크롤 완료: {scroll_count}회")
            
        except Exception as e:
            logger.warning(f"스크롤 중 오류: {e}")
    
    async def _extract_messages(self, page) -> List[WhatsAppMessage]:
        """메시지 추출 / Extract messages"""
        try:
            # 메시지 요소들 찾기
            message_elements = await page.locator(".message-in, .message-out").all()
            
            messages = []
            for element in message_elements:
                try:
                    # 메시지 내용 추출
                    content = await element.text_content()
                    if not content or not content.strip():
                        continue
                    
                    # 메시지 타입 확인
                    message_type = "text"
                    if await element.locator("img").count() > 0:
                        message_type = "image"
                    elif await element.locator("video").count() > 0:
                        message_type = "video"
                    elif await element.locator("a").count() > 0:
                        message_type = "file"
                    
                    # 긴급성 판단
                    is_urgent = self._check_urgency(content)
                    
                    # 발신자 정보 (간단한 추정)
                    sender = "Unknown"
                    if await element.locator(".message-in").count() > 0:
                        sender = "상대방"
                    else:
                        sender = "나"
                    
                    message = WhatsAppMessage(
                        content=content.strip(),
                        timestamp=datetime.now().isoformat(),
                        sender=sender,
                        message_type=message_type,
                        is_urgent=is_urgent
                    )
                    
                    messages.append(message)
                    
                except Exception as e:
                    logger.warning(f"개별 메시지 추출 오류: {e}")
                    continue
            
            return messages
            
        except Exception as e:
            logger.error(f"메시지 추출 오류: {e}")
            return []
    
    def _check_urgency(self, content: str) -> bool:
        """긴급성 확인 / Check urgency"""
        urgent_keywords = [
            "긴급", "urgent", "즉시", "immediate", "빠르게", "asap",
            "중요", "important", "주의", "attention", "경고", "warning"
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in urgent_keywords)
    
    def save_conversation(self, messages: List[WhatsAppMessage], filename: Optional[str] = None) -> Path:
        """대화 내용 저장 / Save conversation"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"whatsapp_conversation_{timestamp}.json"
            
            filepath = Path("data/conversations") / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # 메시지 데이터를 딕셔너리로 변환
            conversation_data = {
                "chat_title": self.chat_title,
                "scraped_at": datetime.now().isoformat(),
                "total_messages": len(messages),
                "messages": [msg.model_dump() for msg in messages]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"대화 내용 저장 완료: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"대화 내용 저장 오류: {e}")
            return Path()
    
    def export_as_text(self, messages: List[WhatsAppMessage], filename: Optional[str] = None) -> Path:
        """텍스트 형식으로 내보내기 / Export as text format"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"whatsapp_conversation_{timestamp}.txt"
            
            filepath = Path("data/conversations") / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"=== WhatsApp 대화 내용 ===\n")
                f.write(f"채팅방: {self.chat_title}\n")
                f.write(f"스크래핑 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"총 메시지: {len(messages)}개\n\n")
                
                for i, msg in enumerate(messages, 1):
                    urgency_mark = "🚨" if msg.is_urgent else ""
                    f.write(f"[{i:03d}] {msg.sender}: {msg.content} {urgency_mark}\n")
            
            logger.info(f"텍스트 내보내기 완료: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"텍스트 내보내기 오류: {e}")
            return Path()


class WhatsAppScraperManager:
    """WhatsApp 스크래퍼 관리자 / WhatsApp scraper manager"""
    
    def __init__(self):
        self.scrapers = {}
        self.chat_rooms = [
            "MR.CHA 전용",
            "물류팀",
            "통관팀", 
            "계약팀",
            "프로젝트팀"
        ]
    
    async def scrape_all_conversations(self, hours_back: int = 24) -> Dict[str, List[WhatsAppMessage]]:
        """모든 채팅방 스크래핑 / Scrape all conversations"""
        results = {}
        
        for chat_room in self.chat_rooms:
            try:
                logger.info(f"채팅방 스크래핑 시작: {chat_room}")
                scraper = WhatsAppScraper(chat_room)
                messages = await scraper.scrape_conversation(hours_back)
                
                if messages:
                    results[chat_room] = messages
                    
                    # 자동 저장
                    scraper.save_conversation(messages)
                    scraper.export_as_text(messages)
                    
                else:
                    logger.warning(f"채팅방에서 메시지를 찾을 수 없음: {chat_room}")
                    
            except Exception as e:
                logger.error(f"채팅방 스크래핑 오류 ({chat_room}): {e}")
                continue
        
        logger.info(f"전체 스크래핑 완료: {len(results)}개 채팅방")
        return results
    
    async def scrape_single_conversation(self, chat_room: str, hours_back: int = 24) -> List[WhatsAppMessage]:
        """단일 채팅방 스크래핑 / Scrape single conversation"""
        try:
            scraper = WhatsAppScraper(chat_room)
            messages = await scraper.scrape_conversation(hours_back)
            
            if messages:
                # 자동 저장
                scraper.save_conversation(messages)
                scraper.export_as_text(messages)
            
            return messages
            
        except Exception as e:
            logger.error(f"단일 채팅방 스크래핑 오류 ({chat_room}): {e}")
            return []


async def main():
    """메인 함수 / Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MACHO-GPT v3.4-mini WhatsApp Scraper")
    parser.add_argument("--chat", type=str, help="스크래핑할 채팅방 이름")
    parser.add_argument("--hours", type=int, default=24, help="몇 시간 전까지 스크래핑할지")
    parser.add_argument("--all", action="store_true", help="모든 채팅방 스크래핑")
    
    args = parser.parse_args()
    
    manager = WhatsAppScraperManager()
    
    if args.all:
        # 모든 채팅방 스크래핑
        results = await manager.scrape_all_conversations(args.hours)
        print(f"총 {len(results)}개 채팅방에서 {sum(len(msgs) for msgs in results.values())}개 메시지 스크래핑 완료")
        
    elif args.chat:
        # 단일 채팅방 스크래핑
        messages = await manager.scrape_single_conversation(args.chat, args.hours)
        print(f"채팅방 '{args.chat}'에서 {len(messages)}개 메시지 스크래핑 완료")
        
    else:
        # 기본: MR.CHA 전용 채팅방
        messages = await manager.scrape_single_conversation("MR.CHA 전용", args.hours)
        print(f"기본 채팅방에서 {len(messages)}개 메시지 스크래핑 완료")


if __name__ == "__main__":
    asyncio.run(main()) 