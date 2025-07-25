#!/usr/bin/env python3
"""
최신 WhatsApp 추출 데이터 AI 분석 스크립트
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from macho_gpt.core.logi_ai_summarizer_241219 import LogiAISummarizer

def main():
    print("🤖 MACHO-GPT v3.4-mini AI 분석 시작")
    print("=" * 50)
    
    # 최신 파일 찾기
    data_dir = Path('data')
    data_files = list(data_dir.glob('hvdc_whatsapp_extraction_*.json'))
    
    if not data_files:
        print("❌ 추출 데이터 파일을 찾을 수 없습니다.")
        return
    
    latest_file = max(data_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 최신 파일: {latest_file}")
    
    # AI 분석 실행
    try:
        summarizer = LogiAISummarizer()
        print("🔍 AI 분석 중...")
        
        result = summarizer.analyze_extraction_file(str(latest_file))
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'reports/ai_analysis_{timestamp}.json'
        
        summarizer.save_analysis(result, output_file)
        
        print(f"✅ 분석 완료!")
        print(f"📄 결과 파일: {output_file}")
        
        # 주요 결과 출력
        print("\n📊 분석 결과 요약:")
        print("-" * 30)
        
        if 'overall_summary' in result:
            summary = result['overall_summary']
            print(f"총 채팅방: {summary.get('total_chats', 0)}개")
            print(f"총 메시지: {summary.get('total_messages', 0)}개")
            print(f"관련 메시지: {summary.get('relevant_messages', 0)}개")
            
            if 'key_insights' in summary:
                print(f"\n🔑 주요 인사이트:")
                for insight in summary['key_insights'][:3]:
                    print(f"  • {insight}")
        
        if 'chat_analyses' in result:
            print(f"\n📱 채팅방별 분석:")
            for chat in result['chat_analyses'][:3]:
                print(f"  • {chat.get('chat_title', 'Unknown')}: {chat.get('message_count', 0)}개 메시지")
        
    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main() 