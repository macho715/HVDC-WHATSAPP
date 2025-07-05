#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini Simplified WhatsApp App
모든 의존성 문제 해결 및 Fallback 기능 포함
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Streamlit 안전한 import
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    print("❌ Streamlit이 설치되지 않았습니다: pip install streamlit")
    STREAMLIT_AVAILABLE = False

# Pandas 안전한 import
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    print("⚠️  Pandas 없음. 기본 기능으로 실행")
    PANDAS_AVAILABLE = False

# OpenAI 안전한 import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    print("⚠️  OpenAI 없음. Mock 요약 기능 사용")
    OPENAI_AVAILABLE = False

# MACHO-GPT 모듈 안전한 import
try:
    from macho_gpt import get_system_status, WORKFLOW_AVAILABLE
    if WORKFLOW_AVAILABLE:
        from macho_gpt.core.logi_workflow_241219 import workflow_manager, ChatRoomType, TaskPriority, TaskStatus
    MACHO_GPT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  MACHO-GPT 모듈 없음: {e}")
    MACHO_GPT_AVAILABLE = False
    WORKFLOW_AVAILABLE = False

# 설정
DB_FILE = Path("summaries.json")

def load_db() -> Dict[str, Dict]:
    """데이터베이스 로딩"""
    try:
        if DB_FILE.exists():
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"DB 로딩 오류: {e}")
    return {}

def save_db(db: Dict[str, Dict]):
    """데이터베이스 저장"""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"DB 저장 오류: {e}")

def mock_llm_summarise(text: str) -> Dict[str, Any]:
    """Mock AI 요약 함수"""
    lines = text.split('\n')
    word_count = len(text.split())
    
    # 간단한 키워드 추출
    keywords = []
    for line in lines[:10]:  # 첫 10줄만 분석
        if any(word in line.lower() for word in ['긴급', '중요', '완료', '확인', '검토', '승인', '마감']):
            keywords.append(line.strip())
    
    return {
        'summary': f"WhatsApp 대화 분석 결과\\n- 총 {len(lines)}개 메시지\\n- {word_count}단어\\n- 주요 키워드: {len(keywords)}개 발견",
        'tasks': keywords[:5] if keywords else ["대화 내용 검토 필요"],
        'confidence': 0.75,
        'analysis_time': datetime.now().isoformat()
    }

def real_llm_summarise(text: str) -> Dict[str, Any]:
    """실제 OpenAI 요약 함수"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 WhatsApp 대화를 분석하는 AI입니다. 한국어로 요약하고 중요한 작업을 추출하세요."},
                {"role": "user", "content": f"다음 대화를 요약하고 중요한 작업들을 추출해주세요:\\n\\n{text}"}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        return {
            'summary': content,
            'tasks': content.split('\\n')[:5],  # 간단히 첫 5줄을 task로
            'confidence': 0.90,
            'analysis_time': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"OpenAI 요약 오류: {e}")
        return mock_llm_summarise(text)

def llm_summarise(text: str) -> Dict[str, Any]:
    """AI 요약 메인 함수"""
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        return real_llm_summarise(text)
    else:
        return mock_llm_summarise(text)

def create_mock_workflow_data():
    """Mock 워크플로우 데이터 생성"""
    return {
        'total_rooms': 3,
        'total_tasks': 8,
        'completion_rate': 0.65,
        'urgent_tasks': 2,
        'confidence': 0.85,
        'teams': {
            '개발팀': {'tasks': 5, 'members': 3},
            '마케팅팀': {'tasks': 2, 'members': 2},
            '디자인팀': {'tasks': 1, 'members': 1}
        }
    }

def main():
    """메인 앱"""
    if not STREAMLIT_AVAILABLE:
        print("❌ Streamlit이 필요합니다: pip install streamlit")
        print("❌ 설치 후 다음 명령어로 실행: streamlit run simplified_whatsapp_app.py")
        return
    
    # 페이지 설정
    st.set_page_config(
        page_title="MACHO-GPT v3.4-mini Simplified",
        page_icon="🤖",
        layout="wide"
    )
    
    # 헤더
    st.title("🤖 MACHO-GPT v3.4-mini WhatsApp 통합 시스템")
    st.caption("Samsung C&T Logistics · HVDC Project Integration (Simplified Mode)")
    
    # 시스템 상태 표시
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status = "✅" if STREAMLIT_AVAILABLE else "❌"
            st.metric("Streamlit", status)
        
        with col2:
            status = "✅" if OPENAI_AVAILABLE else "⚠️"
            st.metric("OpenAI", status)
        
        with col3:
            status = "✅" if MACHO_GPT_AVAILABLE else "⚠️"
            st.metric("MACHO-GPT", status)
        
        with col4:
            status = "✅" if WORKFLOW_AVAILABLE else "⚠️"
            st.metric("Workflow", status)
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📊 대시보드", "💬 메시지 분석", "📋 데이터 관리"])
    
    with tab1:
        st.header("📊 시스템 대시보드")
        
        # 워크플로우 정보
        if WORKFLOW_AVAILABLE and MACHO_GPT_AVAILABLE:
            try:
                summary = workflow_manager.get_workflow_summary()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("총 대화방", summary.get('total_rooms', 0))
                with col2:
                    st.metric("총 태스크", summary.get('total_tasks', 0))
                with col3:
                    completion = summary.get('completion_rate', 0) * 100
                    st.metric("완료율", f"{completion:.1f}%")
                with col4:
                    st.metric("긴급 태스크", summary.get('urgent_tasks', 0))
                    
            except Exception as e:
                st.error(f"워크플로우 데이터 로딩 오류: {e}")
                mock_data = create_mock_workflow_data()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("총 대화방", mock_data['total_rooms'])
                with col2:
                    st.metric("총 태스크", mock_data['total_tasks'])
                with col3:
                    completion = mock_data['completion_rate'] * 100
                    st.metric("완료율", f"{completion:.1f}%")
                with col4:
                    st.metric("긴급 태스크", mock_data['urgent_tasks'])
        else:
            st.info("워크플로우 모듈이 비활성화되어 Mock 데이터를 표시합니다.")
            mock_data = create_mock_workflow_data()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("총 대화방", mock_data['total_rooms'])
            with col2:
                st.metric("총 태스크", mock_data['total_tasks'])
            with col3:
                completion = mock_data['completion_rate'] * 100
                st.metric("완료율", f"{completion:.1f}%")
            with col4:
                st.metric("긁급 태스크", mock_data['urgent_tasks'])
        
        # 시스템 정보
        st.subheader("🔧 시스템 정보")
        
        if MACHO_GPT_AVAILABLE:
            try:
                status = get_system_status()
                st.json(status)
            except Exception as e:
                st.error(f"시스템 상태 로딩 오류: {e}")
        else:
            st.info("시스템 상태: Simplified Mode (일부 기능 제한)")
    
    with tab2:
        st.header("💬 WhatsApp 메시지 분석")
        
        # 메시지 입력
        message_text = st.text_area(
            "분석할 메시지 입력",
            placeholder="WhatsApp 대화 내용을 여기에 붙여넣으세요...",
            height=200
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🤖 AI 분석 실행", type="primary"):
                if message_text.strip():
                    with st.spinner("AI 분석 중..."):
                        result = llm_summarise(message_text)
                        
                        st.subheader("📋 분석 결과")
                        st.write(result['summary'])
                        
                        st.subheader("📝 추출된 작업")
                        for i, task in enumerate(result.get('tasks', []), 1):
                            st.write(f"{i}. {task}")
                        
                        # 결과 저장
                        db = load_db()
                        key = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        db[key] = {
                            'summary': result['summary'],
                            'tasks': result['tasks'],
                            'raw_text': message_text,
                            'confidence': result.get('confidence', 0.75),
                            'timestamp': datetime.now().isoformat()
                        }
                        save_db(db)
                        
                        st.success(f"✅ 분석 완료! (신뢰도: {result.get('confidence', 0.75):.2f})")
                else:
                    st.warning("분석할 메시지를 입력해주세요.")
        
        with col2:
            if st.button("📁 샘플 데이터 로드"):
                sample_text = '''김민수: 안녕하세요, 오늘 회의 준비는 어떻게 되고 있나요?
이영희: 프레젠테이션 자료는 80% 정도 완성되었습니다.
박철수: 마케팅 보고서도 내일까지 완료 예정입니다.
김민수: 좋습니다. 긴급하게 검토가 필요한 부분이 있나요?
이영희: 예산 부분을 다시 확인해야 할 것 같습니다.
박철수: 네, 내일 오전에 최종 검토하겠습니다.'''
                
                st.text_area("샘플 메시지", value=sample_text, height=150, key="sample")
    
    with tab3:
        st.header("📋 데이터 관리")
        
        # 저장된 데이터 표시
        db = load_db()
        
        if db:
            st.subheader(f"📁 저장된 분석 결과 ({len(db)}개)")
            
            # 데이터 표시
            for key, data in sorted(db.items(), reverse=True):
                with st.expander(f"🕐 {key} (신뢰도: {data.get('confidence', 0.0):.2f})"):
                    st.write("**요약:**", data.get('summary', 'N/A'))
                    st.write("**작업:**")
                    for task in data.get('tasks', []):
                        st.write(f"- {task}")
                    
                    if st.button(f"🗑️ 삭제", key=f"delete_{key}"):
                        del db[key]
                        save_db(db)
                        st.rerun()
        else:
            st.info("저장된 데이터가 없습니다.")
        
        # 데이터 관리 버튼
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 새로고침"):
                st.rerun()
        
        with col2:
            if st.button("📤 데이터 내보내기"):
                if db:
                    json_str = json.dumps(db, ensure_ascii=False, indent=2)
                    st.download_button(
                        label="💾 JSON 다운로드",
                        data=json_str,
                        file_name=f"whatsapp_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.warning("내보낼 데이터가 없습니다.")
        
        with col3:
            if st.button("🗑️ 전체 삭제"):
                if st.checkbox("정말 삭제하시겠습니까?"):
                    save_db({})
                    st.success("모든 데이터가 삭제되었습니다.")
                    st.rerun()
    
    # 푸터
    st.markdown("---")
    st.markdown("**🔧 추천 명령어:**")
    st.code("python extract_whatsapp_auto.py --setup  # WhatsApp 인증")
    st.code("python extract_whatsapp_auto.py          # 메시지 추출") 
    st.code("python simplified_whatsapp_app.py        # 간단 모드 실행")

if __name__ == "__main__":
    main() 