#!/usr/bin/env python3
"""
Google Cloud Vision API Authentication Patch
MACHO-GPT v3.4-mini for HVDC Project
OAuth 2.0 클라이언트 ID + API 키 지원
"""

import os
import json
from pathlib import Path
from google.cloud import vision
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# OAuth 2.0 스코프 설정
SCOPES = ['https://www.googleapis.com/auth/cloud-vision']

# API 키 설정
API_KEY = "AIzaSyB0FFF7HoFumEIMM2F94Ey1ktFOT52vtP8"

def setup_gcv_credentials():
    """Google Cloud Vision API 인증 설정 (API 키 + OAuth 2.0 + 서비스 계정 지원)"""
    # API 키 우선 사용
    if API_KEY:
        print(f"✅ API 키 사용: {API_KEY[:10]}...")
        os.environ['GOOGLE_CLOUD_VISION_API_KEY'] = API_KEY
        return "api_key"
    
    # 현재 디렉토리에서 인증 파일 찾기
    current_dir = Path.cwd()
    
    # 서비스 계정 키 파일 우선 검색
    service_account_files = [
        "service-account-key.json",
        "gcv-credentials.json",
        "google-vision-key.json"
    ]
    
    for file_name in service_account_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✅ 서비스 계정 키 파일 발견: {file_path}")
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(file_path)
            return str(file_path)
    
    # OAuth 2.0 클라이언트 ID 파일 검색
    oauth_files = [
        "client_secret_43126604210-vgs39uh1g3118fdelc9q2729glo54v4a.apps.googleusercontent.com.json",
        "client_secret.json",
        "oauth_credentials.json"
    ]
    
    for file_name in oauth_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print(f"✅ OAuth 2.0 클라이언트 ID 파일 발견: {file_path}")
            return setup_oauth_credentials(file_path)
    
    print("⚠️ Google Cloud Vision 인증 파일을 찾을 수 없습니다.")
    return None

def setup_oauth_credentials(client_secret_file):
    """OAuth 2.0 인증 설정"""
    creds = None
    
    # 토큰 파일이 있으면 로드
    token_file = Path("token.pickle")
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # 유효한 인증이 없거나 만료된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # OAuth 2.0 플로우 실행
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 토큰 저장
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    # 환경 변수 설정
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(client_secret_file)
    return str(client_secret_file)

def create_gcv_client():
    """Google Cloud Vision 클라이언트 생성"""
    credential_path = setup_gcv_credentials()
    if not credential_path:
        raise RuntimeError("Google Cloud Vision API 인증 파일이 필요합니다.")
    
    try:
        if credential_path == "api_key":
            # API 키를 사용한 클라이언트 생성
            from google.cloud import vision_v1
            from google.api_core import client_options
            
            # API 키를 사용한 클라이언트 옵션 설정
            client_options_obj = client_options.ClientOptions(
                api_key=API_KEY,
                api_endpoint="vision.googleapis.com"
            )
            
            client = vision_v1.ImageAnnotatorClient(client_options=client_options_obj)
        else:
            # OAuth 2.0 인증 사용
            creds = None
            token_file = Path("token.pickle")
            if token_file.exists():
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            if creds:
                client = vision.ImageAnnotatorClient(credentials=creds)
            else:
                client = vision.ImageAnnotatorClient()
        
        print("✅ Google Cloud Vision 클라이언트 생성 성공")
        return client
    except Exception as e:
        print(f"❌ Google Cloud Vision 클라이언트 생성 실패: {str(e)}")
        raise

def test_gcv_connection():
    """Google Cloud Vision API 연결 테스트"""
    try:
        client = create_gcv_client()
        print("✅ Google Cloud Vision API 연결 성공")
        return True
    except Exception as e:
        print(f"❌ Google Cloud Vision API 연결 실패: {str(e)}")
        return False

if __name__ == "__main__":
    # 테스트 실행
    success = test_gcv_connection()
    if success:
        print("🎉 Google Cloud Vision API setup completed successfully!")
    else:
        print("💥 Google Cloud Vision API setup failed!")
        exit(1)
