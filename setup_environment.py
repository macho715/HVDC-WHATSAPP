#!/usr/bin/env python3
"""
환경 설정 스크립트
MACHO-GPT v3.4-mini
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_python_path():
    """Python PATH 설정"""
    print("🔧 Python PATH 설정 중...")
    
    # 일반적인 Python 설치 경로들
    python_paths = [
        r"C:\Python311",
        r"C:\Python310", 
        r"C:\Python39",
        r"C:\Users\{}\AppData\Local\Programs\Python\Python311".format(os.getenv('USERNAME')),
        r"C:\Users\{}\AppData\Local\Programs\Python\Python310".format(os.getenv('USERNAME')),
    ]
    
    for path in python_paths:
        python_exe = Path(path) / "python.exe"
        if python_exe.exists():
            print(f"✅ Python 발견: {path}")
            
            # PATH에 추가
            current_path = os.getenv('PATH', '')
            if path not in current_path:
                new_path = f"{current_path};{path};{path}\\Scripts"
                os.environ['PATH'] = new_path
                print(f"✅ PATH 업데이트: {path}")
            
            return path
    
    print("❌ Python을 찾을 수 없습니다.")
    return None

def setup_google_cloud_credentials():
    """Google Cloud Vision API 자격 증명 설정"""
    print("\n🔧 Google Cloud Vision API 설정 중...")
    
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        print("⚠️ GOOGLE_APPLICATION_CREDENTIALS 환경변수가 설정되지 않았습니다.")
        print("설정 방법:")
        print("1. Google Cloud Console에서 서비스 계정 JSON 키 다운로드")
        print("2. 환경변수 설정: setx GOOGLE_APPLICATION_CREDENTIALS \"C:\\keys\\vision-sa.json\"")
        return False
    
    if not Path(credentials_path).exists():
        print(f"❌ 서비스 계정 파일을 찾을 수 없습니다: {credentials_path}")
        return False
    
    print(f"✅ Google Cloud Vision 자격 증명 확인: {credentials_path}")
    return True

def install_required_packages():
    """필요한 패키지 설치"""
    print("\n📦 필요한 패키지 설치 중...")
    
    packages = [
        'google-cloud-vision',
        'pytest',
        'pytest-asyncio',
        'playwright',
        'easyocr',
        'openai'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} 설치 완료")
        except subprocess.CalledProcessError:
            print(f"⚠️ {package} 설치 실패")

def setup_whatsapp_auth():
    """WhatsApp 인증 설정"""
    print("\n📱 WhatsApp 인증 설정 중...")
    
    auth_file = Path("auth_backups/auth.json")
    if not auth_file.exists():
        print("⚠️ WhatsApp 인증 파일이 없습니다.")
        print("실행 방법: python auth_setup.py")
        return False
    
    print(f"✅ WhatsApp 인증 파일 확인: {auth_file}")
    return True

def main():
    """메인 설정 함수"""
    print("🚀 MACHO-GPT v3.4-mini 환경 설정")
    print("=" * 50)
    
    # 1. Python PATH 설정
    python_path = setup_python_path()
    if not python_path:
        print("❌ Python 설정 실패")
        return False
    
    # 2. Google Cloud Vision 설정
    gcv_ok = setup_google_cloud_credentials()
    
    # 3. 패키지 설치
    install_required_packages()
    
    # 4. WhatsApp 인증 설정
    whatsapp_ok = setup_whatsapp_auth()
    
    print("\n" + "=" * 50)
    print("📊 설정 결과:")
    print(f"✅ Python: {python_path}")
    print(f"{'✅' if gcv_ok else '⚠️'} Google Cloud Vision: {'설정됨' if gcv_ok else '설정 필요'}")
    print(f"{'✅' if whatsapp_ok else '⚠️'} WhatsApp: {'인증됨' if whatsapp_ok else '인증 필요'}")
    
    if gcv_ok and whatsapp_ok:
        print("\n🎉 모든 설정이 완료되었습니다!")
        print("다음 명령어로 테스트해보세요:")
        print("  python test_gcv_setup.py")
        print("  python auth_setup.py")
        print("  run_gcv_ocr.bat")
    else:
        print("\n⚠️ 일부 설정이 필요합니다.")
        if not gcv_ok:
            print("- Google Cloud Vision API 설정 필요")
        if not whatsapp_ok:
            print("- WhatsApp 인증 필요")
    
    return True

if __name__ == "__main__":
    main() 