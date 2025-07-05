#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini 최소 실행 스크립트
"""

import os
import sys
import subprocess

def main():
    print("🤖 MACHO-GPT v3.4-mini 실행 중...")
    
    # 1. Python 환경 확인
    print(f"Python 버전: {sys.version}")
    
    # 2. 필수 패키지 확인
    try:
        import streamlit
        print("✅ Streamlit 사용 가능")
    except ImportError:
        print("❌ Streamlit 설치 필요: pip install streamlit")
        return
    
    # 3. 기존 데이터 정리 (선택사항)
    data_files = ["data/workflow_data.json", "summaries.json"]
    for file in data_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️  {file} 삭제됨")
            except:
                pass
    
    # 4. 앱 실행
    print("🚀 Streamlit 앱 실행 중...")
    print("   브라우저에서 http://localhost:8507 접속하세요")
    
    try:
        # simplified_whatsapp_app.py 실행
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "simplified_whatsapp_app.py", "--server.port", "8507"
        ])
    except KeyboardInterrupt:
        print("\n🛑 앱 중단됨")
    except Exception as e:
        print(f"❌ 실행 오류: {e}")
        print("대안: streamlit run simplified_whatsapp_app.py --server.port 8507")

if __name__ == "__main__":
    main() 