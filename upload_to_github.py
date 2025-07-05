#!/usr/bin/env python3
"""
🚀 MACHO-GPT v3.4-mini GitHub 업로드 자동화 스크립트
Samsung C&T Logistics · HVDC Project

Repository: https://github.com/macho715/HVDC-WHATSAPP.git
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
from datetime import datetime

def print_header():
    """헤더 출력"""
    print("🚀 MACHO-GPT v3.4-mini GitHub 업로드 도구")
    print("=" * 60)
    print("📋 Repository: https://github.com/macho715/HVDC-WHATSAPP.git")
    print("🎯 Project: Samsung C&T Logistics · HVDC WhatsApp Automation")
    print()

def check_git_installation():
    """Git 설치 확인"""
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Git 설치됨: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git이 설치되지 않았습니다!")
        print()
        print("📥 Git 설치 방법:")
        print("1. Windows: https://git-scm.com/download/win")
        print("2. Chocolatey: choco install git")
        print("3. Winget: winget install Git.Git")
        print()
        return False

def check_git_config():
    """Git 설정 확인"""
    try:
        name = subprocess.run(['git', 'config', '--global', 'user.name'], 
                            capture_output=True, text=True, check=True)
        email = subprocess.run(['git', 'config', '--global', 'user.email'], 
                             capture_output=True, text=True, check=True)
        
        if name.stdout.strip() and email.stdout.strip():
            print(f"✅ Git 사용자: {name.stdout.strip()} <{email.stdout.strip()}>")
            return True
        else:
            print("⚠️ Git 사용자 정보가 설정되지 않았습니다.")
            return False
    except subprocess.CalledProcessError:
        print("⚠️ Git 사용자 정보가 설정되지 않았습니다.")
        return False

def setup_git_config():
    """Git 설정 안내"""
    print("\n🔧 Git 사용자 정보 설정이 필요합니다:")
    print("다음 명령어를 실행하세요:")
    print()
    print('git config --global user.name "Your Name"')
    print('git config --global user.email "your.email@example.com"')
    print()
    
    choice = input("설정을 완료했습니까? (y/n): ").lower()
    return choice == 'y'

def create_project_structure():
    """프로젝트 구조 정리"""
    print("\n📁 프로젝트 구조 정리 중...")
    
    # 제외할 파일 목록
    excluded_files = [
        'auth.json',
        '__pycache__',
        'logs',
        '.streamlit',
        'temp',
        '.temp',
        'screenshots',
        'test_results'
    ]
    
    # 현재 디렉토리의 파일 목록
    current_files = os.listdir('.')
    important_files = []
    
    for file in current_files:
        if not any(excluded in file for excluded in excluded_files):
            important_files.append(file)
    
    print(f"✅ 업로드할 파일 수: {len(important_files)}")
    return important_files

def init_git_repo():
    """Git 저장소 초기화"""
    print("\n🔧 Git 저장소 초기화 중...")
    
    try:
        # Git 저장소 초기화
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git 저장소 초기화 완료")
        
        # 원격 저장소 연결
        subprocess.run(['git', 'remote', 'add', 'origin', 
                       'https://github.com/macho715/HVDC-WHATSAPP.git'], 
                      check=True)
        print("✅ 원격 저장소 연결 완료")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 초기화 실패: {e}")
        return False

def commit_and_push():
    """파일 커밋 및 푸시"""
    print("\n📤 파일 커밋 및 푸시 중...")
    
    try:
        # 모든 파일 추가
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ 파일 추가 완료")
        
        # 커밋 메시지 생성
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"[FEAT] Initial MACHO-GPT v3.4-mini WhatsApp automation system - {timestamp}"
        
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ 커밋 완료")
        
        # 기본 브랜치 설정
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        
        # 푸시
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("✅ GitHub에 푸시 완료!")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 커밋/푸시 실패: {e}")
        return False

def show_alternatives():
    """Git 없이 업로드하는 방법 안내"""
    print("\n🔧 Git 없이 업로드하는 방법:")
    print()
    print("1️⃣ GitHub Desktop 사용 (추천)")
    print("   - 다운로드: https://desktop.github.com/")
    print("   - GUI로 쉽게 업로드 가능")
    print()
    print("2️⃣ 웹 브라우저 업로드")
    print("   - https://github.com/macho715/HVDC-WHATSAPP")
    print("   - 'Add file' > 'Upload files' 클릭")
    print("   - 파일 드래그 앤 드롭")
    print()
    print("3️⃣ VS Code Git 확장")
    print("   - VS Code의 Git 기능 사용")
    print("   - Source Control 패널 활용")
    print()
    
    # 업로드할 핵심 파일 목록 출력
    print("📋 업로드할 핵심 파일 목록:")
    core_files = [
        'START_HERE.md',
        'PROJECT_SUMMARY.md', 
        'whatsapp_executive_dashboard.py',
        'simplified_whatsapp_app.py',
        'run_app.py',
        'extract_whatsapp_auto.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
        'GITHUB_UPDATE_GUIDE.md'
    ]
    
    for file in core_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (없음)")

def main():
    """메인 함수"""
    print_header()
    
    # Git 설치 확인
    if not check_git_installation():
        show_alternatives()
        return
    
    # Git 설정 확인
    if not check_git_config():
        if not setup_git_config():
            show_alternatives()
            return
        
        # 다시 확인
        if not check_git_config():
            print("❌ Git 설정이 완료되지 않았습니다.")
            show_alternatives()
            return
    
    # 프로젝트 구조 정리
    important_files = create_project_structure()
    
    # 진행 확인
    print(f"\n🎯 {len(important_files)}개 파일을 GitHub에 업로드합니다.")
    print("📋 Repository: https://github.com/macho715/HVDC-WHATSAPP.git")
    print()
    
    choice = input("계속 진행하시겠습니까? (y/n): ").lower()
    if choice != 'y':
        print("❌ 업로드 취소됨")
        return
    
    # Git 저장소 초기화
    if not init_git_repo():
        show_alternatives()
        return
    
    # 커밋 및 푸시
    if commit_and_push():
        print("\n🎉 GitHub 업로드 완료!")
        print("🌐 확인: https://github.com/macho715/HVDC-WHATSAPP")
    else:
        print("\n❌ 업로드 실패")
        show_alternatives()

if __name__ == "__main__":
    main() 