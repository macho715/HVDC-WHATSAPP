#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini 수동 테스트 스크립트
전체 파이프라인을 단계별로 테스트할 수 있습니다.
"""

import os
import sys
import subprocess
from pathlib import Path

def test_python_version():
    """Python 버전 확인"""
    print("🔍 1단계: Python 버전 확인")
    try:
        version = sys.version
        print(f"✅ Python 버전: {version}")
        return True
    except Exception as e:
        print(f"❌ Python 버전 확인 실패: {e}")
        return False

def test_google_cloud_vision():
    """Google Cloud Vision 설정 테스트"""
    print("\n🔍 2단계: Google Cloud Vision 설정 테스트")
    try:
        # 환경변수 확인
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            print("⚠️ GOOGLE_APPLICATION_CREDENTIALS 환경변수가 설정되지 않았습니다.")
            return False
        
        if not Path(credentials_path).exists():
            print(f"❌ 서비스 계정 파일을 찾을 수 없습니다: {credentials_path}")
            return False
        
        print(f"✅ Google Cloud Vision 자격 증명 확인: {credentials_path}")
        
        # 라이브러리 확인
        try:
            from google.cloud import vision
            print("✅ Google Cloud Vision 라이브러리 설치됨")
            return True
        except ImportError:
            print("❌ Google Cloud Vision 라이브러리 미설치")
            return False
            
    except Exception as e:
        print(f"❌ Google Cloud Vision 설정 테스트 실패: {e}")
        return False

def test_whatsapp_auth():
    """WhatsApp 인증 상태 확인"""
    print("\n🔍 3단계: WhatsApp 인증 상태 확인")
    
    auth_files = [
        "auth_backups/auth.json",
        "auth_backups/whatsapp_auth.json"
    ]
    
    for auth_file in auth_files:
        if Path(auth_file).exists():
            file_size = Path(auth_file).stat().st_size
            print(f"✅ WhatsApp 인증 파일 존재: {auth_file} ({file_size} bytes)")
            return True
    
    print("❌ WhatsApp 인증 파일 없음")
    return False

def test_individual_modules():
    """개별 모듈 테스트"""
    print("\n🔍 4단계: 개별 모듈 테스트")
    
    modules = [
        ("whatsapp_media_ocr_extractor", "미디어 OCR 모듈"),
        ("extract_whatsapp_auto", "WhatsApp 스크래핑 모듈"),
        ("analyze_latest", "AI 분석 모듈")
    ]
    
    results = {}
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {description} 로드 성공")
            results[module_name] = True
        except ImportError as e:
            print(f"❌ {description} 로드 실패: {e}")
            results[module_name] = False
    
    return results

def run_test_pipeline():
    """테스트 파이프라인 실행"""
    print("\n🔍 5단계: 테스트 파이프라인 실행")
    
    print("테스트 옵션:")
    print("1. Google Cloud Vision OCR 테스트")
    print("2. WhatsApp 스크래핑 테스트")
    print("3. 전체 파이프라인 테스트")
    print("4. 종료")
    
    try:
        choice = input("\n선택 (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n테스트 중단됨")
        return
    
    if choice == "1":
        print("\n🚀 Google Cloud Vision OCR 테스트 시작...")
        try:
            subprocess.run([
                sys.executable, "whatsapp_media_ocr_extractor.py",
                "--chat", "HVDC 물류팀",
                "--media-only",
                "--ocr-engine", "gcv",
                "--max-media", "2"
            ], check=True)
            print("✅ Google Cloud Vision OCR 테스트 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ Google Cloud Vision OCR 테스트 실패: {e}")
    
    elif choice == "2":
        print("\n🚀 WhatsApp 스크래핑 테스트 시작...")
        try:
            subprocess.run([
                sys.executable, "extract_whatsapp_auto.py",
                "--chat", "HVDC 물류팀"
            ], check=True)
            print("✅ WhatsApp 스크래핑 테스트 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ WhatsApp 스크래핑 테스트 실패: {e}")
    
    elif choice == "3":
        print("\n🚀 전체 파이프라인 테스트 시작...")
        
        # 1) WhatsApp 스크래핑
        print("1) WhatsApp 스크래핑")
        try:
            subprocess.run([
                sys.executable, "extract_whatsapp_auto.py",
                "--chat", "HVDC 물류팀"
            ], check=True)
            print("✅ WhatsApp 스크래핑 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ WhatsApp 스크래핑 실패: {e}")
        
        # 2) 미디어 OCR 처리
        print("\n2) 미디어 OCR 처리")
        try:
            subprocess.run([
                sys.executable, "whatsapp_media_ocr_extractor.py",
                "--chat", "HVDC 물류팀",
                "--media-only",
                "--ocr-engine", "gcv",
                "--max-media", "2"
            ], check=True)
            print("✅ 미디어 OCR 처리 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ 미디어 OCR 처리 실패: {e}")
        
        # 3) AI 분석
        print("\n3) AI 분석")
        try:
            subprocess.run([sys.executable, "analyze_latest.py"], check=True)
            print("✅ AI 분석 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ AI 분석 실패: {e}")
    
    else:
        print("테스트 종료")

def check_results():
    """결과 파일 확인"""
    print("\n📊 테스트 결과 확인...")
    
    # WhatsApp 데이터 파일 확인
    data_files = list(Path("data").glob("hvdc_whatsapp_extraction_*.json"))
    if data_files:
        print("✅ WhatsApp 데이터 추출 완료")
        for file in data_files:
            print(f"  - {file.name}")
    else:
        print("⚠️ WhatsApp 데이터 파일 없음")
    
    # 미디어 OCR 결과 파일 확인
    ocr_files = list(Path("data").glob("whatsapp_media_ocr_*.json"))
    if ocr_files:
        print("✅ 미디어 OCR 결과 완료")
        for file in ocr_files:
            print(f"  - {file.name}")
    else:
        print("⚠️ 미디어 OCR 결과 파일 없음")
    
    # AI 분석 결과 파일 확인
    analysis_files = list(Path("reports").glob("ai_analysis_*.json"))
    if analysis_files:
        print("✅ AI 분석 결과 완료")
        for file in analysis_files:
            print(f"  - {file.name}")
    else:
        print("⚠️ AI 분석 결과 파일 없음")

def main():
    """메인 함수"""
    print("🧪 MACHO-GPT v3.4-mini 수동 테스트")
    print("=" * 50)
    
    # 1. Python 버전 확인
    if not test_python_version():
        print("❌ Python 환경 설정 실패")
        return
    
    # 2. Google Cloud Vision 설정 테스트
    gcv_ok = test_google_cloud_vision()
    
    # 3. WhatsApp 인증 상태 확인
    whatsapp_ok = test_whatsapp_auth()
    
    # 4. 개별 모듈 테스트
    module_results = test_individual_modules()
    
    # 5. 테스트 파이프라인 실행
    run_test_pipeline()
    
    # 6. 결과 확인
    check_results()
    
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약:")
    print(f"✅ Python: 정상")
    print(f"{'✅' if gcv_ok else '⚠️'} Google Cloud Vision: {'설정됨' if gcv_ok else '설정 필요'}")
    print(f"{'✅' if whatsapp_ok else '⚠️'} WhatsApp: {'인증됨' if whatsapp_ok else '인증 필요'}")
    
    module_success = sum(module_results.values())
    module_total = len(module_results)
    print(f"{'✅' if module_success == module_total else '⚠️'} 모듈: {module_success}/{module_total} 성공")
    
    print("\n🎉 수동 테스트 완료!")

if __name__ == "__main__":
    main() 