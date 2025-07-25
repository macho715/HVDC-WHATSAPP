#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini 시스템 상태 확인
현재 환경과 설정 상태를 점검합니다.
"""

import os
import sys
from pathlib import Path

def check_python_environment():
    """Python 환경 확인"""
    print("🔍 Python 환경 확인")
    print(f"  Python 버전: {sys.version}")
    print(f"  실행 경로: {sys.executable}")
    print(f"  현재 작업 디렉토리: {os.getcwd()}")
    
    # PATH 확인
    path_dirs = os.getenv('PATH', '').split(os.pathsep)
    python_in_path = any('python' in p.lower() for p in path_dirs)
    print(f"  Python이 PATH에 있음: {'✅' if python_in_path else '❌'}")
    
    return True

def check_google_cloud_vision():
    """Google Cloud Vision 설정 확인"""
    print("\n🔍 Google Cloud Vision 설정 확인")
    
    # 환경변수 확인
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_path:
        print(f"  환경변수: {credentials_path}")
        if Path(credentials_path).exists():
            file_size = Path(credentials_path).stat().st_size
            print(f"  파일 존재: ✅ ({file_size} bytes)")
        else:
            print(f"  파일 존재: ❌")
            return False
    else:
        print("  환경변수: ❌ 설정되지 않음")
        return False
    
    # 라이브러리 확인
    try:
        import google.cloud.vision
        print("  라이브러리: ✅ 설치됨")
        return True
    except ImportError:
        print("  라이브러리: ❌ 미설치")
        return False

def check_whatsapp_auth():
    """WhatsApp 인증 상태 확인"""
    print("\n🔍 WhatsApp 인증 상태 확인")
    
    auth_files = [
        "auth_backups/auth.json",
        "auth_backups/whatsapp_auth.json"
    ]
    
    for auth_file in auth_files:
        if Path(auth_file).exists():
            file_size = Path(auth_file).stat().st_size
            print(f"  인증 파일: {auth_file} ✅ ({file_size} bytes)")
            return True
    
    print("  인증 파일: ❌ 없음")
    return False

def check_modules():
    """모듈 확인"""
    print("\n🔍 모듈 확인")
    
    modules = [
        ("whatsapp_media_ocr_extractor", "미디어 OCR"),
        ("extract_whatsapp_auto", "WhatsApp 스크래핑"),
        ("analyze_latest", "AI 분석"),
        ("macho_gpt", "MACHO-GPT 코어")
    ]
    
    results = {}
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  {description}: ✅ 로드됨")
            results[module_name] = True
        except ImportError as e:
            print(f"  {description}: ❌ 로드 실패 ({e})")
            results[module_name] = False
    
    return results

def check_data_files():
    """데이터 파일 확인"""
    print("\n🔍 데이터 파일 확인")
    
    # data 디렉토리
    data_dir = Path("data")
    if data_dir.exists():
        json_files = list(data_dir.glob("*.json"))
        print(f"  data 디렉토리: ✅ ({len(json_files)}개 JSON 파일)")
        for file in json_files[-3:]:  # 최근 3개만 표시
            print(f"    - {file.name}")
    else:
        print("  data 디렉토리: ❌ 없음")
    
    # reports 디렉토리
    reports_dir = Path("reports")
    if reports_dir.exists():
        json_files = list(reports_dir.glob("*.json"))
        print(f"  reports 디렉토리: ✅ ({len(json_files)}개 JSON 파일)")
        for file in json_files[-3:]:  # 최근 3개만 표시
            print(f"    - {file.name}")
    else:
        print("  reports 디렉토리: ❌ 없음")

def check_test_files():
    """테스트 파일 확인"""
    print("\n🔍 테스트 파일 확인")
    
    test_dir = Path("tests")
    if test_dir.exists():
        test_files = list(test_dir.glob("test_*.py"))
        print(f"  테스트 파일: ✅ ({len(test_files)}개)")
        for file in test_files:
            print(f"    - {file.name}")
    else:
        print("  테스트 파일: ❌ tests 디렉토리 없음")

def main():
    """메인 함수"""
    print("🔍 MACHO-GPT v3.4-mini 시스템 상태 확인")
    print("=" * 60)
    
    # 1. Python 환경 확인
    python_ok = check_python_environment()
    
    # 2. Google Cloud Vision 설정 확인
    gcv_ok = check_google_cloud_vision()
    
    # 3. WhatsApp 인증 상태 확인
    whatsapp_ok = check_whatsapp_auth()
    
    # 4. 모듈 확인
    module_results = check_modules()
    
    # 5. 데이터 파일 확인
    check_data_files()
    
    # 6. 테스트 파일 확인
    check_test_files()
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 시스템 상태 요약:")
    print(f"  Python 환경: {'✅' if python_ok else '❌'}")
    print(f"  Google Cloud Vision: {'✅' if gcv_ok else '❌'}")
    print(f"  WhatsApp 인증: {'✅' if whatsapp_ok else '❌'}")
    
    module_success = sum(module_results.values())
    module_total = len(module_results)
    print(f"  모듈 로드: {module_success}/{module_total} ✅")
    
    # 권장사항
    print("\n💡 권장사항:")
    if not gcv_ok:
        print("  - Google Cloud Vision 설정 필요: GOOGLE_CLOUD_VISION_SETUP.md 참조")
    if not whatsapp_ok:
        print("  - WhatsApp 인증 필요: auth_refresh.bat 실행")
    if module_success < module_total:
        print("  - 일부 모듈 로드 실패: requirements.txt 확인")
    
    print("\n🎯 다음 단계:")
    print("  - 전체 테스트: python manual_test.py")
    print("  - TDD 테스트: run_tdd_tests.bat")
    print("  - 파이프라인 테스트: test_full_pipeline.bat")

if __name__ == "__main__":
    main() 