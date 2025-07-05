#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini GitHub 업로드 패키지 생성기
Samsung C&T Logistics · HVDC Project · ADNOC·DSV Partnership
"""

import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path

def create_github_upload_package():
    """GitHub 업로드용 패키지 생성"""
    
    print("🚀 MACHO-GPT v3.4-mini GitHub 업로드 패키지 생성 중...")
    
    # 업로드 제외 파일/폴더 목록
    exclude_patterns = {
        'auth.json',           # WhatsApp 인증 정보
        '__pycache__',         # Python 캐시
        'logs',                # 로그 파일
        '.git',                # Git 폴더
        'temp',                # 임시 파일
        'node_modules',        # Node.js 의존성
        '.env',                # 환경 변수
        '*.pyc',               # Python 컴파일 파일
        'upload_package',      # 이전 업로드 패키지
        'github_upload_package' # 패키지 폴더 자체
    }
    
    # 핵심 업로드 파일 목록
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
        'GITHUB_UPDATE_GUIDE.md',
        'summaries.json'
    ]
    
    # 업로드 패키지 폴더 생성
    package_dir = Path('github_upload_package')
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # 핵심 파일 복사
    copied_files = []
    for file_name in core_files:
        if Path(file_name).exists():
            shutil.copy2(file_name, package_dir)
            copied_files.append(file_name)
            print(f"✅ 복사됨: {file_name}")
        else:
            print(f"⚠️  파일 없음: {file_name}")
    
    # macho_gpt 모듈 복사
    macho_gpt_dir = Path('macho_gpt')
    if macho_gpt_dir.exists():
        package_macho_dir = package_dir / 'macho_gpt'
        shutil.copytree(macho_gpt_dir, package_macho_dir, 
                       ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        print("✅ macho_gpt/ 모듈 복사됨")
    
    # 설정 폴더 복사
    for config_dir in ['configs', 'templates', 'tests']:
        if Path(config_dir).exists():
            shutil.copytree(Path(config_dir), package_dir / config_dir,
                           ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            print(f"✅ {config_dir}/ 폴더 복사됨")
    
    # 데이터 폴더 (보안 파일 제외)
    data_dir = Path('data')
    if data_dir.exists():
        package_data_dir = package_dir / 'data'
        package_data_dir.mkdir()
        for file_path in data_dir.glob('*.json'):
            if 'auth' not in file_path.name.lower():
                shutil.copy2(file_path, package_data_dir)
                print(f"✅ 데이터 파일 복사됨: {file_path.name}")
    
    # 업로드 정보 파일 생성
    upload_info = {
        'upload_date': datetime.now().isoformat(),
        'project': 'MACHO-GPT v3.4-mini WhatsApp Automation',
        'partnership': 'Samsung C&T Logistics · ADNOC·DSV Partnership',
        'system_status': {
            'running_ports': [8505, 8506, 8507],
            'mode': 'ZERO',
            'confidence': '51.0%',
            'target_confidence': '90%+'
        },
        'files_included': copied_files,
        'security_notes': 'auth.json 및 민감 정보 제외됨'
    }
    
    with open(package_dir / 'UPLOAD_INFO.json', 'w', encoding='utf-8') as f:
        json.dump(upload_info, f, indent=2, ensure_ascii=False)
    
    # ZIP 파일 생성
    zip_path = f'HVDC_WHATSAPP_Upload_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 업로드 패키지 생성 완료!")
    print(f"📦 ZIP 파일: {zip_path}")
    print(f"📁 패키지 폴더: {package_dir}")
    print(f"📊 총 파일 수: {len(copied_files)}")
    
    print("\n🔗 GitHub 업로드 방법:")
    print("1. https://github.com/macho715/HVDC-WHATSAPP 접속")
    print("2. 'Add file' → 'Upload files' 클릭")
    print("3. ZIP 파일을 압축 해제하여 개별 파일 업로드")
    print("4. 또는 드래그 앤 드롭으로 개별 파일 업로드")
    
    return zip_path, package_dir

if __name__ == "__main__":
    try:
        zip_path, package_dir = create_github_upload_package()
        print(f"\n✅ 업로드 준비 완료: {zip_path}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc() 