#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp RPA 간단 테스트
----------------------------------------
Samsung C&T Logistics · HVDC Project

기능:
- WhatsApp RPA 기본 기능 테스트
- 브라우저 실행 확인
- 모듈 import 테스트
"""

import asyncio
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_whatsapp_rpa_basic():
    """WhatsApp RPA 기본 기능 테스트"""
    print("🤖 MACHO-GPT v3.4-mini WhatsApp RPA 기본 테스트")
    print("=" * 50)
    
    try:
        # 1. 모듈 import 테스트
        print("1️⃣ 모듈 import 테스트...")
        from macho_gpt.rpa.logi_rpa_whatsapp_241219 import WhatsAppRPAExtractor
        print("✅ WhatsAppRPAExtractor import 성공")
        
        # 2. 클래스 인스턴스 생성 테스트
        print("2️⃣ 클래스 인스턴스 생성 테스트...")
        extractor = WhatsAppRPAExtractor(mode="LATTICE")
        print("✅ WhatsAppRPAExtractor 인스턴스 생성 성공")
        
        # 3. 상태 확인 테스트
        print("3️⃣ 상태 확인 테스트...")
        status = extractor.get_status()
        print(f"✅ 상태 확인 성공: {status['status']}")
        
        # 4. Playwright 브라우저 테스트
        print("4️⃣ Playwright 브라우저 테스트...")
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://web.whatsapp.com/")
            title = await page.title()
            await browser.close()
            print(f"✅ 브라우저 테스트 성공: {title}")
        
        # 5. 파일 시스템 테스트
        print("5️⃣ 파일 시스템 테스트...")
        data_dir = Path("data")
        logs_dir = Path("logs")
        auth_file = Path("auth.json")
        
        print(f"   - data 디렉토리: {'✅' if data_dir.exists() else '❌'}")
        print(f"   - logs 디렉토리: {'✅' if logs_dir.exists() else '❌'}")
        print(f"   - auth.json 파일: {'✅' if auth_file.exists() else '❌'}")
        
        print("\n🎉 모든 기본 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
        return False

async def test_whatsapp_rpa_advanced():
    """WhatsApp RPA 고급 기능 테스트"""
    print("\n🔬 고급 기능 테스트...")
    
    try:
        from macho_gpt.rpa.logi_rpa_whatsapp_241219 import WhatsAppRPAExtractor
        
        extractor = WhatsAppRPAExtractor(mode="LATTICE")
        
        # 채팅방 목록 테스트
        print(f"📱 기본 채팅방: {extractor.default_chat_titles}")
        
        # 설정 확인
        print(f"🎯 모드: {extractor.mode}")
        print(f"📊 신뢰도 임계값: {extractor.confidence_threshold}")
        print(f"🌐 User Agent: {extractor.user_agents[0][:50]}...")
        
        print("✅ 고급 기능 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"❌ 고급 테스트 실패: {str(e)}")
        return False

async def main():
    """메인 테스트 함수"""
    print("🚀 MACHO-GPT v3.4-mini WhatsApp RPA 테스트 시작")
    print("=" * 60)
    
    # 기본 테스트
    basic_result = await test_whatsapp_rpa_basic()
    
    # 고급 테스트
    advanced_result = await test_whatsapp_rpa_advanced()
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약:")
    print(f"   - 기본 테스트: {'✅ 통과' if basic_result else '❌ 실패'}")
    print(f"   - 고급 테스트: {'✅ 통과' if advanced_result else '❌ 실패'}")
    
    if basic_result and advanced_result:
        print("\n🎉 모든 테스트 통과! WhatsApp RPA가 정상적으로 작동합니다.")
        print("\n🔧 다음 단계:")
        print("   1. python whatsapp_rpa_auto_extract.py --chat 'MR.CHA 전용'")
        print("   2. 브라우저에서 QR 코드 스캔")
        print("   3. 자동 메시지 추출 대기")
    else:
        print("\n⚠️ 일부 테스트 실패. 문제를 해결한 후 다시 시도하세요.")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 