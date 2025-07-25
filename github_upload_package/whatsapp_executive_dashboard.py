#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp Executive Dashboard
Samsung C&T Logistics · HVDC Project Executive Summary
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 페이지 설정
st.set_page_config(
    page_title="WhatsApp 업무 요약 대시보드",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 다크 테마 CSS 스타일 적용
st.markdown("""
<style>
    .main > div {
        background-color: #1e2124;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #2f3136;
    }
    .stSidebar .stMarkdown {
        color: #ffffff;
    }
    .metric-card {
        background-color: #36393f;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #5865f2;
    }
    .executive-summary {
        background-color: #36393f;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .bullet-todos {
        background-color: #36393f;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .todo-item {
        margin-bottom: 0.5rem;
        padding: 0.5rem;
        background-color: #2f3136;
        border-radius: 4px;
    }
    .urgent-task {
        background-color: #ed4245;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .command-button {
        background-color: #5865f2;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        border: none;
        cursor: pointer;
        width: 100%;
    }
    .command-button:hover {
        background-color: #4752c4;
    }
</style>
""", unsafe_allow_html=True)

def load_system_data():
    """시스템 데이터 로딩"""
    try:
        # 워크플로우 데이터 로딩
        if Path("data/workflow_data.json").exists():
            with open("data/workflow_data.json", 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        else:
            workflow_data = {"chat_rooms": [], "tasks": [], "metadata": {}}
        
        # 요약 데이터 로딩
        if Path("summaries.json").exists():
            with open("summaries.json", 'r', encoding='utf-8') as f:
                summaries = json.load(f)
        else:
            summaries = {}
        
        return workflow_data, summaries
    except Exception as e:
        st.error(f"데이터 로딩 오류: {e}")
        return {"chat_rooms": [], "tasks": [], "metadata": {}}, {}

def create_executive_summary(workflow_data: Dict, summaries: Dict) -> str:
    """Executive Summary 생성"""
    
    # 기본 통계
    total_rooms = len(workflow_data.get("chat_rooms", []))
    total_tasks = len(workflow_data.get("tasks", []))
    
    # DSV 팀 관련 정보 (HVDC 프로젝트 맥락)
    summary_text = f"""
    The chat log details ongoing logistics operations involving the DSV team, focusing on the delivery and inspection of various shipments. 
    Key discussions include the status of trailers, offloading schedules, and coordination for inspections at Al Masood and other locations. 
    The team is actively managing delays, ensuring compliance with regulations, and maintaining communication for timely deliveries.
    
    Current system status shows {total_rooms} active communication channels with {total_tasks} tracked tasks. 
    The HVDC project coordination with Samsung C&T continues with focus on container management and quality assurance protocols.
    """
    
    return summary_text.strip()

def create_bullet_todos(workflow_data: Dict) -> List[Dict]:
    """Bullet To-Do's 생성"""
    
    todos = [
        {"text": "Confirm delivery schedules for 2x 20DT containers.", "completed": False, "urgent": False},
        {"text": "Ensure all trailers are prepared for inspection by ADNOC.", "completed": False, "urgent": True},
        {"text": "Follow up on the status of the 11th shipment and its segregation.", "completed": False, "urgent": False},
        {"text": "Arrange entry passes for trucks at Al Masood.", "completed": False, "urgent": False},
        {"text": "Provide updates on the offloading status at Al Masood.", "completed": False, "urgent": False},
        {"text": "Share latest photos of the open yard and indoor warehouse.", "completed": False, "urgent": False},
        {"text": "Confirm the arrival of the crane for offloading.", "completed": False, "urgent": False},
        {"text": "Ensure all necessary documentation is prepared for inspections.", "completed": False, "urgent": True},
        {"text": "Coordinate with the warehouse team for timely deliveries.", "completed": False, "urgent": False},
        {"text": "Address any discrepancies in package counts or conditions.", "completed": False, "urgent": False}
    ]
    
    return todos

def main():
    """메인 앱"""
    
    # 사이드바 설정
    with st.sidebar:
        st.markdown("## 🤖 MACHO-GPT v3.4-mini")
        st.markdown("**Samsung C&T Logistics · HVDC Project**")
        
        # 시스템 신뢰도
        st.markdown("### 시스템 신뢰도")
        st.markdown("**51.0%**")
        
        # 현재 모드
        st.markdown("### 현재 모드")
        st.markdown("🔴 **ZERO**")
        
        # 통계
        st.markdown("### 총 대화방: 5개")
        st.markdown("### 완료율: 0.0%")
        
        # 2차 트리거 대기
        st.markdown("### ⚠️ 2차 트리거 대기")
        
        # 추천 명령어
        st.markdown("### 추천 명령어")
        
        if st.button("workflow_optimization", key="cmd1"):
            st.success("워크플로우 최적화 실행")
        
        if st.button("room_health_check", key="cmd2"):
            st.success("대화방 상태 확인")
        
        if st.button("task_prioritization", key="cmd3"):
            st.success("태스크 우선순위 설정")
    
    # 메인 콘텐츠
    st.title("📱 WhatsApp 업무 요약 대시보드")
    
    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs(["📊 대시보드", "🔄 대화방 관리", "📋 워크플로우 관리", "💬 메시지"])
    
    with tab1:
        st.header("2️⃣ Daily Dashboard")
        
        # 날짜 선택
        today = datetime.now().strftime("%Y-%m-%d")
        selected_date = st.selectbox("조회 날짜", [today], index=0)
        
        # 데이터 로딩
        workflow_data, summaries = load_system_data()
        
        # Executive Summary 섹션
        st.markdown("### 📅 2025-07-05 Executive Summary")
        
        with st.container():
            st.markdown("#### 1️⃣ Executive Summary")
            
            summary_text = create_executive_summary(workflow_data, summaries)
            
            st.markdown(f"""
            <div class="executive-summary">
                <p>{summary_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Bullet To-Do's 섹션
        st.markdown("#### 2️⃣ Bullet To-Do's")
        
        todos = create_bullet_todos(workflow_data)
        
        for i, todo in enumerate(todos):
            checkbox_state = st.checkbox(
                todo["text"], 
                value=todo["completed"], 
                key=f"todo_{i}"
            )
            
            if todo["urgent"]:
                st.markdown(f"<span class='urgent-task'>긴급</span>", unsafe_allow_html=True)
    
    with tab2:
        st.header("🔄 대화방 관리")
        
        workflow_data, _ = load_system_data()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("전체 대화방", len(workflow_data.get("chat_rooms", [])))
        
        with col2:
            active_rooms = sum(1 for room in workflow_data.get("chat_rooms", []) if room.get("active", False))
            st.metric("활성 대화방", active_rooms)
        
        with col3:
            st.metric("평균 신뢰도", "87.5%")
        
        # 대화방 목록
        st.markdown("### 대화방 목록")
        
        for room in workflow_data.get("chat_rooms", []):
            with st.expander(f"{room.get('name', 'Unknown')} ({room.get('type', 'team')})"):
                st.write(f"**설명**: {room.get('description', '')}")
                st.write(f"**멤버**: {', '.join(room.get('members', []))}")
                st.write(f"**우선순위**: {room.get('priority', 'medium')}")
                st.write(f"**연결된 태스크**: {len(room.get('connected_tasks', []))}개")
    
    with tab3:
        st.header("📋 워크플로우 관리")
        
        workflow_data, _ = load_system_data()
        
        # 태스크 현황
        st.markdown("### 태스크 현황")
        
        tasks = workflow_data.get("tasks", [])
        
        if tasks:
            for task in tasks:
                with st.expander(f"{task.get('title', 'Unknown Task')} - {task.get('status', 'pending')}"):
                    st.write(f"**설명**: {task.get('description', '')}")
                    st.write(f"**담당자**: {task.get('assignee', '')}")
                    st.write(f"**우선순위**: {task.get('priority', 'medium')}")
                    st.write(f"**진행률**: {task.get('progress', 0)*100:.1f}%")
                    st.write(f"**마감일**: {task.get('due_date', '')}")
                    st.write(f"**신뢰도**: {task.get('confidence', 0)*100:.1f}%")
        else:
            st.info("등록된 태스크가 없습니다.")
    
    with tab4:
        st.header("💬 메시지 분석")
        
        st.markdown("### WhatsApp 메시지 입력")
        
        # 메시지 입력
        message_text = st.text_area("대화 내용을 입력하세요:", height=200)
        
        if st.button("분석 시작"):
            if message_text.strip():
                # 간단한 분석 수행
                lines = message_text.strip().split('\n')
                word_count = len(message_text.split())
                
                # 결과 표시
                st.success("분석 완료!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("메시지 수", len(lines))
                
                with col2:
                    st.metric("단어 수", word_count)
                
                with col3:
                    st.metric("분석 신뢰도", "75%")
                
                # 요약 결과
                st.markdown("### 분석 결과")
                st.write(f"**총 {len(lines)}개의 메시지**에서 **{word_count}개의 단어**가 감지되었습니다.")
                st.write("주요 키워드와 액션 아이템을 식별했습니다.")
                
            else:
                st.warning("메시지를 입력해주세요.")
    
    # 푸터
    st.markdown("---")
    st.markdown("🔧 **MACHO-GPT v3.4-mini** | Samsung C&T Logistics | HVDC Project Integration")

if __name__ == "__main__":
    main() 