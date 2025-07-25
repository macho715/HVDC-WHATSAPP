#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp 스크래핑 즉시 복구 스크립트
Samsung C&T Logistics · HVDC Project

실패 원인 분석 보고서 기반 즉시 해결 방안
- 인증 상태 진단 및 복구
- 라이브러리 호환성 문제 해결
- 채팅방 접근 문제 진단
"""

import asyncio
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


class WhatsAppSystemDiagnostic:
    """WhatsApp 시스템 진단 및 복구 클래스"""
    
    def __init__(self):
        self.auth_file = Path("auth.json")
        self.backup_dir = Path("auth_backups")
        self.report_file = Path("WHATSAPP_SCRAPING_FAILURE_REPORT.md")
        
    def run_diagnostic(self):
        """전체 시스템 진단 실행"""
        print("🔍 MACHO-GPT v3.4-mini WhatsApp 시스템 진단 시작")
        print("=" * 60)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "diagnostics": {}
        }
        
        # 1. 라이브러리 호환성 진단
        results["diagnostics"]["library"] = self.check_library_compatibility()
        
        # 2. 인증 상태 진단
        results["diagnostics"]["authentication"] = self.check_authentication_status()
        
        # 3. 채팅방 접근 진단
        results["diagnostics"]["chat_access"] = self.check_chat_access()
        
        # 4. 시스템 환경 진단
        results["diagnostics"]["environment"] = self.check_system_environment()
        
        # 결과 저장
        self.save_diagnostic_results(results)
        
        # 권장 조치사항 제시
        self.recommend_actions(results)
        
        return results
    
    def check_library_compatibility(self):
        """라이브러리 호환성 확인"""
        print("📦 라이브러리 호환성 확인 중...")
        
        issues = []
        fixes = []
        
        # playwright-stealth 확인
        try:
            import playwright_stealth
            issues.append("playwright-stealth가 설치되어 있어 호환성 문제 발생 가능")
            fixes.append("pip uninstall playwright-stealth -y")
        except ImportError:
            print("✅ playwright-stealth 미설치 - 호환성 문제 없음")
        
        # playwright 확인
        try:
            import playwright
            print("✅ Playwright 설치됨")
        except ImportError:
            issues.append("Playwright가 설치되지 않음")
            fixes.append("pip install playwright")
            fixes.append("python -m playwright install")
        
        # 기타 의존성 확인
        required_packages = ["asyncio", "json", "pathlib"]
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} 사용 가능")
            except ImportError:
                issues.append(f"{package} 패키지 누락")
        
        return {
            "status": "OK" if not issues else "ISSUES_FOUND",
            "issues": issues,
            "fixes": fixes
        }
    
    def check_authentication_status(self):
        """인증 상태 확인"""
        print("🔐 인증 상태 확인 중...")
        
        issues = []
        fixes = []
        
        if not self.auth_file.exists():
            issues.append("auth.json 파일이 존재하지 않음")
            fixes.append("python auth_setup.py --setup")
        else:
            try:
                with open(self.auth_file, 'r', encoding='utf-8') as f:
                    auth_data = json.load(f)
                
                file_size = self.auth_file.stat().st_size
                print(f"✅ auth.json 파일 존재 ({file_size:,} bytes)")
                
                # 인증 데이터 유효성 확인
                if not auth_data.get("cookies") and not auth_data.get("origins"):
                    issues.append("auth.json 파일이 비어있거나 유효하지 않음")
                    fixes.append("python auth_setup.py --setup")
                else:
                    print(f"✅ 인증 데이터 유효 (쿠키: {len(auth_data.get('cookies', []))}개)")
                    
            except Exception as e:
                issues.append(f"auth.json 파일 읽기 오류: {e}")
                fixes.append("python auth_setup.py --setup")
        
        return {
            "status": "OK" if not issues else "AUTH_REQUIRED",
            "issues": issues,
            "fixes": fixes
        }
    
    def check_chat_access(self):
        """채팅방 접근 확인"""
        print("💬 채팅방 접근 확인 중...")
        
        issues = []
        fixes = []
        
        # 현재 설정된 채팅방명 확인
        chat_titles = ["MR.CHA 전용", "물류팀", "통관팀"]
        
        print("📋 설정된 채팅방명:")
        for i, title in enumerate(chat_titles, 1):
            print(f"  {i}. {title}")
        
        issues.append("실제 채팅방명과 일치하는지 수동 확인 필요")
        fixes.append("WhatsApp Web에서 실제 채팅방명 확인 후 코드 수정")
        
        return {
            "status": "MANUAL_CHECK_REQUIRED",
            "issues": issues,
            "fixes": fixes,
            "configured_chats": chat_titles
        }
    
    def check_system_environment(self):
        """시스템 환경 확인"""
        print("🖥️ 시스템 환경 확인 중...")
        
        issues = []
        fixes = []
        
        # Python 버전 확인
        python_version = sys.version_info
        print(f"✅ Python 버전: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 8):
            issues.append("Python 3.8 이상 필요")
            fixes.append("Python 업그레이드 필요")
        
        # 네트워크 연결 확인
        try:
            import urllib.request
            urllib.request.urlopen("https://web.whatsapp.com/", timeout=5)
            print("✅ WhatsApp Web 접근 가능")
        except Exception as e:
            issues.append(f"WhatsApp Web 접근 불가: {e}")
            fixes.append("네트워크 연결 확인")
        
        # 디스크 공간 확인
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_gb = free // (1024**3)
            print(f"✅ 디스크 공간: {free_gb}GB 사용 가능")
            
            if free_gb < 1:
                issues.append("디스크 공간 부족 (1GB 미만)")
                fixes.append("불필요한 파일 정리")
        except Exception as e:
            print(f"⚠️ 디스크 공간 확인 실패: {e}")
        
        return {
            "status": "OK" if not issues else "ISSUES_FOUND",
            "issues": issues,
            "fixes": fixes
        }
    
    def save_diagnostic_results(self, results):
        """진단 결과 저장"""
        try:
            diagnostic_file = Path("diagnostic_results.json")
            with open(diagnostic_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ 진단 결과 저장: {diagnostic_file}")
        except Exception as e:
            print(f"❌ 진단 결과 저장 실패: {e}")
    
    def recommend_actions(self, results):
        """권장 조치사항 제시"""
        print("\n" + "=" * 60)
        print("📋 권장 조치사항")
        print("=" * 60)
        
        all_issues = []
        all_fixes = []
        
        for category, diagnostic in results["diagnostics"].items():
            if diagnostic["status"] != "OK":
                all_issues.extend(diagnostic["issues"])
                all_fixes.extend(diagnostic["fixes"])
        
        if not all_issues:
            print("🎉 모든 진단 항목이 정상입니다!")
            return
        
        print("🔴 발견된 문제점:")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n🛠️ 해결 방법:")
        for i, fix in enumerate(all_fixes, 1):
            print(f"  {i}. {fix}")
        
        print("\n⚡ 즉시 실행 가능한 명령어:")
        print("  python auth_setup.py --verify")
        print("  python auth_setup.py --setup  # 인증 필요시")
        print("  pip uninstall playwright-stealth -y  # 라이브러리 정리")
    
    def auto_fix_library_issues(self):
        """라이브러리 문제 자동 해결"""
        print("🔧 라이브러리 문제 자동 해결 중...")
        
        try:
            # playwright-stealth 제거
            result = subprocess.run([
                sys.executable, "-m", "pip", "uninstall", "playwright-stealth", "-y"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ playwright-stealth 제거 완료")
            else:
                print("⚠️ playwright-stealth 제거 실패 (이미 제거됨)")
            
            # playwright 업그레이드
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "playwright", "--upgrade"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Playwright 업그레이드 완료")
            else:
                print("❌ Playwright 업그레이드 실패")
            
            # 브라우저 설치
            result = subprocess.run([
                sys.executable, "-m", "playwright", "install"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 브라우저 설치 완료")
            else:
                print("❌ 브라우저 설치 실패")
                
        except Exception as e:
            print(f"❌ 자동 해결 실패: {e}")


async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp 시스템 진단 및 복구")
    parser.add_argument("--diagnose", action="store_true", help="전체 시스템 진단")
    parser.add_argument("--auto-fix", action="store_true", help="자동 복구 실행")
    parser.add_argument("--check-auth", action="store_true", help="인증 상태만 확인")
    
    args = parser.parse_args()
    
    diagnostic = WhatsAppSystemDiagnostic()
    
    if args.diagnose:
        # 전체 진단
        diagnostic.run_diagnostic()
    
    elif args.auto_fix:
        # 자동 복구
        print("🔧 자동 복구 시작...")
        diagnostic.auto_fix_library_issues()
        print("✅ 자동 복구 완료")
    
    elif args.check_auth:
        # 인증 상태만 확인
        auth_status = diagnostic.check_authentication_status()
        print(f"인증 상태: {auth_status['status']}")
        if auth_status['issues']:
            print("발견된 문제:")
            for issue in auth_status['issues']:
                print(f"  - {issue}")
    
    else:
        # 기본: 전체 진단
        print("🔍 WhatsApp 시스템 진단 및 복구 도구")
        print("사용법:")
        print("  python IMMEDIATE_FIX_SCRIPT.py --diagnose    # 전체 진단")
        print("  python IMMEDIATE_FIX_SCRIPT.py --auto-fix    # 자동 복구")
        print("  python IMMEDIATE_FIX_SCRIPT.py --check-auth  # 인증 확인")
        
        # 기본 진단 실행
        diagnostic.run_diagnostic()


if __name__ == "__main__":
    asyncio.run(main()) 