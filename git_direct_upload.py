#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini GitHub 직접 업로드 스크립트
Samsung C&T Logistics · HVDC Project · ADNOC·DSV Partnership
"""

import os
import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

def check_git_installed():
    """Git 설치 여부 확인"""
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Git 설치됨: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git이 설치되지 않았습니다.")
        return False

def install_git():
    """Git 설치 시도"""
    print("🔧 Git 설치 중...")
    
    # Windows에서 winget으로 Git 설치 시도
    try:
        subprocess.run(['winget', 'install', '--id', 'Git.Git', '-e', '--source', 'winget'], 
                      check=True)
        print("✅ Git 설치 완료")
        return True
    except subprocess.CalledProcessError:
        print("❌ winget으로 Git 설치 실패")
        
    # 대안: Chocolatey로 설치 시도
    try:
        subprocess.run(['choco', 'install', 'git', '-y'], check=True)
        print("✅ Git 설치 완료 (Chocolatey)")
        return True
    except subprocess.CalledProcessError:
        print("❌ Chocolatey로 Git 설치 실패")
        
    print("⚠️  수동으로 Git을 설치해주세요:")
    print("   https://git-scm.com/download/win")
    return False

def setup_git_config():
    """Git 설정"""
    try:
        # Git 사용자 정보 설정 (예시)
        subprocess.run(['git', 'config', '--global', 'user.name', 'MACHO-GPT'], 
                      check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'macho-gpt@samsung-ct.com'], 
                      check=True)
        print("✅ Git 설정 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 설정 실패: {e}")
        return False

def init_git_repo():
    """Git 저장소 초기화"""
    try:
        # 이미 Git 저장소인지 확인
        if Path('.git').exists():
            print("✅ Git 저장소가 이미 존재합니다.")
            return True
            
        # Git 저장소 초기화
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git 저장소 초기화 완료")
        
        # 원격 저장소 추가
        subprocess.run(['git', 'remote', 'add', 'origin', 
                       'https://github.com/macho715/HVDC-WHATSAPP.git'], 
                      check=True)
        print("✅ 원격 저장소 추가 완료")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 저장소 초기화 실패: {e}")
        return False

def add_files_to_git():
    """Git에 파일 추가"""
    try:
        # 핵심 파일들 추가
        core_files = [
            'simplified_whatsapp_app.py',
            'run_app.py',
            'whatsapp_executive_dashboard.py',
            'extract_whatsapp_auto.py',
            'requirements.txt',
            'requirements_simple.txt',
            'pyproject.toml',
            'README.md',
            'PROJECT_SUMMARY.md',
            'GITHUB_UPDATE_GUIDE.md'
        ]
        
        # 파일 존재 확인 및 추가
        added_files = []
        for file in core_files:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
                added_files.append(file)
                print(f"✅ 추가됨: {file}")
            else:
                print(f"⚠️  파일 없음: {file}")
        
        # macho_gpt 모듈 추가
        if Path('macho_gpt').exists():
            subprocess.run(['git', 'add', 'macho_gpt/'], check=True)
            print("✅ macho_gpt/ 모듈 추가됨")
        
        # 설정 폴더들 추가
        config_dirs = ['configs', 'templates', 'tests', 'data']
        for dir_name in config_dirs:
            if Path(dir_name).exists():
                subprocess.run(['git', 'add', f'{dir_name}/'], check=True)
                print(f"✅ {dir_name}/ 폴더 추가됨")
        
        # 데이터 파일 추가 (보안 파일 제외)
        if Path('summaries.json').exists():
            subprocess.run(['git', 'add', 'summaries.json'], check=True)
            print("✅ summaries.json 추가됨")
        
        return len(added_files) > 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 파일 추가 실패: {e}")
        return False

def commit_changes():
    """변경사항 커밋"""
    try:
        commit_message = f"""feat: Add MACHO-GPT v3.4-mini core applications

- Add simplified_whatsapp_app.py (port 8506 - stable version)
- Add run_app.py (port 8507 - integrated execution)
- Add whatsapp_executive_dashboard.py (port 8505 - executive dashboard)
- Add extract_whatsapp_auto.py (RPA automation)
- Add macho_gpt module structure (core + rpa)
- Add requirements and configuration files
- Update project with current operational status

System Status:
- Running services: 3 ports (8505, 8506, 8507)
- Mode: ZERO (safe mode)
- Confidence: 51.0% → Target: 90%+
- Partnership: Samsung C&T Logistics · ADNOC·DSV Partnership
- Project: HVDC Integration Complete

Deployment ready: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ 커밋 완료")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 커밋 실패: {e}")
        return False

def push_to_github():
    """GitHub에 푸시"""
    try:
        # 먼저 원격 저장소에서 pull
        print("🔄 원격 저장소에서 최신 변경사항 가져오는 중...")
        subprocess.run(['git', 'pull', 'origin', 'main', '--allow-unrelated-histories'], 
                      check=True)
        print("✅ 원격 저장소 동기화 완료")
        
        # GitHub에 푸시
        print("🚀 GitHub에 업로드 중...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ GitHub 업로드 완료")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub 업로드 실패: {e}")
        print("💡 Personal Access Token이 필요할 수 있습니다.")
        print("   GitHub Settings > Developer settings > Personal access tokens")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 MACHO-GPT v3.4-mini GitHub 직접 업로드 시작...")
    print("=" * 60)
    
    # 1. Git 설치 확인
    if not check_git_installed():
        print("🔧 Git 설치를 진행합니다...")
        if not install_git():
            print("❌ Git 설치 실패. 수동 설치 후 다시 시도하세요.")
            return False
    
    # 2. Git 설정
    if not setup_git_config():
        print("❌ Git 설정 실패")
        return False
    
    # 3. Git 저장소 초기화
    if not init_git_repo():
        print("❌ Git 저장소 초기화 실패")
        return False
    
    # 4. 파일 추가
    if not add_files_to_git():
        print("❌ 파일 추가 실패")
        return False
    
    # 5. 커밋
    if not commit_changes():
        print("❌ 커밋 실패")
        return False
    
    # 6. GitHub에 푸시
    if not push_to_github():
        print("❌ GitHub 업로드 실패")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 GitHub 업로드 성공!")
    print("🔗 저장소: https://github.com/macho715/HVDC-WHATSAPP")
    print("📊 현재 상태: MACHO-GPT v3.4-mini 운영 중")
    print("🚀 포트: 8505 (Executive), 8506 (Simplified), 8507 (Integrated)")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ 업로드 완료!")
        else:
            print("\n❌ 업로드 실패!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  업로드 중단됨")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        sys.exit(1) 