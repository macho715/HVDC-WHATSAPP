#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp Web 인증 설정
Samsung C&T Logistics · HVDC Project

안전하고 효율적인 WhatsApp Web 인증 절차
- QR 코드 스캔 후 세션 저장
- auth.json 파일에 인증 상태 저장
- 자동화 스크립트에서 재사용 가능
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright


class WhatsAppAuthSetup:
    """WhatsApp Web 인증 설정 클래스"""
    
    def __init__(self):
        self.auth_file = Path("auth.json")
        self.backup_dir = Path("auth_backups")
        self.backup_dir.mkdir(exist_ok=True)
        
    async def setup_authentication(self):
        """인증 설정 실행"""
        print("🔐 MACHO-GPT v3.4-mini WhatsApp Web 인증 설정")
        print("=" * 50)
        
        # 기존 인증 파일 백업
        if self.auth_file.exists():
            await self._backup_existing_auth()
        
        try:
            async with async_playwright() as p:
                # 브라우저 설정
                browser = await p.chromium.launch(
                    headless=False,  # QR 코드 스캔을 위해 headless=False
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-web-security",
                        "--disable-features=VizDisplayCompositor"
                    ]
                )
                
                # 컨텍스트 설정
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                )
                
                page = await context.new_page()
                
                # WhatsApp Web 접속
                print("📱 WhatsApp Web 접속 중...")
                await page.goto("https://web.whatsapp.com/")
                
                # QR 코드 스캔 대기
                print("\n📋 QR 코드 스캔 안내:")
                print("1. 휴대폰에서 WhatsApp 앱 열기")
                print("2. 설정 → 연결된 기기 → 기기 연결")
                print("3. 화면의 QR 코드를 스캔")
                print("4. 로그인 완료 후 Enter 키를 누르세요")
                print("\n" + "=" * 50)
                
                # 사용자 입력 대기
                input("QR 코드 스캔 완료 후 Enter를 눌러주세요...")
                
                # 로그인 상태 확인
                print("🔍 로그인 상태 확인 중...")
                
                # 채팅방 목록이 로드될 때까지 대기
                try:
                    await page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                    print("✅ 로그인 성공!")
                except Exception as e:
                    print("⚠️  채팅방 목록을 찾을 수 없습니다. 다시 시도해주세요.")
                    await browser.close()
                    return False
                
                # 인증 정보 저장
                print("💾 인증 정보 저장 중...")
                await context.storage_state(path=str(self.auth_file))
                
                # 저장된 정보 확인
                if self.auth_file.exists():
                    file_size = self.auth_file.stat().st_size
                    print(f"✅ 인증 정보 저장 완료: {self.auth_file} ({file_size:,} bytes)")
                    
                    # 저장된 정보 미리보기
                    await self._preview_auth_info()
                else:
                    print("❌ 인증 정보 저장 실패")
                    return False
                
                await browser.close()
                return True
                
        except Exception as e:
            print(f"❌ 인증 설정 오류: {e}")
            return False
    
    async def _backup_existing_auth(self):
        """기존 인증 파일 백업"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"auth_backup_{timestamp}.json"
            
            # 기존 파일 복사
            import shutil
            shutil.copy2(self.auth_file, backup_file)
            
            print(f"📦 기존 인증 파일 백업: {backup_file}")
            
        except Exception as e:
            print(f"⚠️  백업 실패: {e}")
    
    async def _preview_auth_info(self):
        """저장된 인증 정보 미리보기"""
        try:
            with open(self.auth_file, 'r', encoding='utf-8') as f:
                auth_data = json.load(f)
            
            print("\n📊 저장된 인증 정보:")
            print(f"   - 쿠키: {len(auth_data.get('cookies', []))}개")
            print(f"   - 로컬스토리지: {len(auth_data.get('origins', []))}개 도메인")
            print(f"   - 저장 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"⚠️  인증 정보 미리보기 실패: {e}")
    
    async def verify_authentication(self):
        """인증 상태 검증"""
        if not self.auth_file.exists():
            print("❌ 인증 파일이 없습니다. 인증 설정을 먼저 실행하세요.")
            return False
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(storage_state=str(self.auth_file))
                page = await context.new_page()
                
                await page.goto("https://web.whatsapp.com/")
                
                # 로그인 상태 확인
                try:
                    await page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)
                    print("✅ 인증 상태 유효")
                    await browser.close()
                    return True
                except:
                    print("❌ 인증 상태 만료됨")
                    await browser.close()
                    return False
                    
        except Exception as e:
            print(f"❌ 인증 검증 오류: {e}")
            return False
    
    def list_backups(self):
        """백업 파일 목록"""
        if not self.backup_dir.exists():
            print("📦 백업 파일이 없습니다.")
            return
        
        backup_files = list(self.backup_dir.glob("auth_backup_*.json"))
        if not backup_files:
            print("📦 백업 파일이 없습니다.")
            return
        
        print(f"📦 백업 파일 목록 ({len(backup_files)}개):")
        for backup_file in sorted(backup_files, reverse=True):
            file_size = backup_file.stat().st_size
            file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            print(f"   - {backup_file.name} ({file_size:,} bytes, {file_time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    def restore_backup(self, backup_name: str):
        """백업 파일 복원"""
        backup_file = self.backup_dir / backup_name
        if not backup_file.exists():
            print(f"❌ 백업 파일을 찾을 수 없습니다: {backup_name}")
            return False
        
        try:
            import shutil
            shutil.copy2(backup_file, self.auth_file)
            print(f"✅ 백업 복원 완료: {backup_name}")
            return True
        except Exception as e:
            print(f"❌ 백업 복원 실패: {e}")
            return False


async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MACHO-GPT v3.4-mini WhatsApp Web 인증 설정")
    parser.add_argument("--setup", action="store_true", help="새로운 인증 설정")
    parser.add_argument("--verify", action="store_true", help="인증 상태 검증")
    parser.add_argument("--backups", action="store_true", help="백업 파일 목록")
    parser.add_argument("--restore", type=str, help="백업 파일 복원")
    
    args = parser.parse_args()
    
    auth_setup = WhatsAppAuthSetup()
    
    if args.setup:
        # 새로운 인증 설정
        success = await auth_setup.setup_authentication()
        if success:
            print("\n🎉 인증 설정 완료!")
            print("이제 자동화 스크립트에서 auth.json을 사용할 수 있습니다.")
        else:
            print("\n❌ 인증 설정 실패")
    
    elif args.verify:
        # 인증 상태 검증
        await auth_setup.verify_authentication()
    
    elif args.backups:
        # 백업 파일 목록
        auth_setup.list_backups()
    
    elif args.restore:
        # 백업 파일 복원
        auth_setup.restore_backup(args.restore)
    
    else:
        # 기본: 새로운 인증 설정
        print("🔐 MACHO-GPT v3.4-mini WhatsApp Web 인증 설정")
        print("사용법:")
        print("  python auth_setup.py --setup     # 새로운 인증 설정")
        print("  python auth_setup.py --verify    # 인증 상태 검증")
        print("  python auth_setup.py --backups   # 백업 파일 목록")
        print("  python auth_setup.py --restore <파일명>  # 백업 복원")


if __name__ == "__main__":
    asyncio.run(main()) 