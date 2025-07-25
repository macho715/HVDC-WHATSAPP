#!/usr/bin/env python3
"""
Google Cloud Vision 설정 테스트 스크립트
MACHO-GPT v3.4-mini
"""

import os
import sys

def test_gcv_setup():
    """Google Cloud Vision 설정 테스트"""
    print("🔍 Google Cloud Vision 설정 테스트")
    print("=" * 50)
    
    # 1. 환경변수 확인
    print("1. 환경변수 확인...")
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS 환경변수가 설정되지 않았습니다.")
        print("   설정 방법: setx GOOGLE_APPLICATION_CREDENTIALS \"C:\\path\\to\\vision-sa.json\"")
        return False
    
    print(f"✅ 환경변수 설정됨: {credentials_path}")
    
    # 2. 파일 존재 확인
    print("\n2. 서비스 계정 파일 확인...")
    if not os.path.exists(credentials_path):
        print(f"❌ 서비스 계정 파일을 찾을 수 없습니다: {credentials_path}")
        return False
    
    print(f"✅ 서비스 계정 파일 존재: {credentials_path}")
    
    # 3. Google Cloud Vision 라이브러리 확인
    print("\n3. Google Cloud Vision 라이브러리 확인...")
    try:
        from google.cloud import vision
        from google.oauth2 import service_account
        print("✅ Google Cloud Vision 라이브러리 설치됨")
    except ImportError as e:
        print(f"❌ Google Cloud Vision 라이브러리 미설치: {e}")
        print("   설치 방법: pip install google-cloud-vision")
        return False
    
    # 4. 인증 테스트
    print("\n4. 인증 테스트...")
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        print("✅ 서비스 계정 인증 성공")
    except Exception as e:
        print(f"❌ 서비스 계정 인증 실패: {e}")
        return False
    
    # 5. Vision 클라이언트 테스트
    print("\n5. Vision 클라이언트 테스트...")
    try:
        client = vision.ImageAnnotatorClient(credentials=credentials)
        print("✅ Vision 클라이언트 생성 성공")
    except Exception as e:
        print(f"❌ Vision 클라이언트 생성 실패: {e}")
        return False
    
    # 6. 패치 모듈 테스트
    print("\n6. 패치 모듈 테스트...")
    try:
        from google_vision_ocr_patch import gcv_ocr
        print("✅ 패치 모듈 로드 성공")
    except ImportError as e:
        print(f"⚠️ 패치 모듈 로드 실패: {e}")
        print("   패치 모듈이 없어도 기본 GCV 클라이언트는 사용 가능합니다.")
    
    print("\n" + "=" * 50)
    print("✅ Google Cloud Vision 설정 테스트 완료!")
    print("이제 WhatsApp 미디어 OCR을 사용할 수 있습니다.")
    print("\n사용 예시:")
    print("  python whatsapp_media_ocr_extractor.py --chat \"HVDC 물류팀\" --ocr-engine gcv")
    print("  run_gcv_ocr.bat")
    
    return True

if __name__ == "__main__":
    success = test_gcv_setup()
    if not success:
        sys.exit(1) 