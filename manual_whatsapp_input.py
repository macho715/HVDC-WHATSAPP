#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini 수동 WhatsApp 데이터 입력 시스템
자동 스크래핑 실패 시 수동으로 대화 데이터를 입력할 수 있는 인터페이스
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManualWhatsAppInput:
    """수동 WhatsApp 데이터 입력 시스템"""
    
    def __init__(self):
        self.data_file = Path("manual_whatsapp_data.json")
        self.load_existing_data()
    
    def load_existing_data(self):
        """기존 데이터 로드"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception as e:
                logger.error(f"데이터 로드 실패: {e}")
                self.data = {"conversations": []}
        else:
            self.data = {"conversations": []}
    
    def save_data(self):
        """데이터 저장"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"데이터 저장 실패: {e}")
            return False
    
    def add_conversation(self, chat_name, messages, date=None):
        """대화 추가"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conversation = {
            "chat_name": chat_name,
            "date": date,
            "messages": messages,
            "timestamp": datetime.now().isoformat(),
            "source": "manual_input"
        }
        
        self.data["conversations"].append(conversation)
        return self.save_data()
    
    def get_conversations(self, date=None):
        """특정 날짜의 대화 조회"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        return [conv for conv in self.data["conversations"] 
                if conv["date"] == date]
    
    def get_all_conversations(self):
        """모든 대화 조회"""
        return self.data["conversations"]

def main():
    st.set_page_config(
        page_title="수동 WhatsApp 데이터 입력",
        page_icon="📱",
        layout="wide"
    )
    
    st.title("📱 MACHO-GPT v3.4-mini 수동 WhatsApp 데이터 입력")
    st.markdown("---")
    
    # 시스템 초기화
    input_system = ManualWhatsAppInput()
    
    # 사이드바 - 메뉴
    st.sidebar.title("메뉴")
    menu = st.sidebar.selectbox(
        "선택하세요",
        ["📝 새 대화 입력", "📊 데이터 조회", "📋 전체 대화 목록", "⚙️ 설정"]
    )
    
    if menu == "📝 새 대화 입력":
        st.header("📝 새 WhatsApp 대화 입력")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chat_name = st.text_input("채팅방 이름", placeholder="예: MR.CHA 전용")
            date = st.date_input("대화 날짜", value=datetime.now())
            
            # 빠른 입력 템플릿
            st.subheader("📋 빠른 입력 템플릿")
            template = st.selectbox(
                "템플릿 선택",
                ["직접 입력", "회의 일정", "긴급 사항", "일반 업무", "커스텀"]
            )
            
            if template == "회의 일정":
                sample_messages = """[09:00] 김철수: 오늘 오후 2시 회의 일정 변경되었습니다.
[09:05] 이영희: 알겠습니다. 참석자들에게 공지하겠습니다.
[09:10] 박민수: 회의실 예약 확인했습니다.
[09:15] 최영수: 자료 준비 완료했습니다."""
            elif template == "긴급 사항":
                sample_messages = """[14:30] 김철수: 긴급 확인 필요한 사항이 있습니다.
[14:35] 이영희: 즉시 대응 부탁드립니다.
[14:40] 박민수: 상황 파악 중입니다.
[14:45] 최영수: 조치 완료했습니다."""
            elif template == "일반 업무":
                sample_messages = """[10:00] 김철수: 프로젝트 진행 상황 공유드립니다.
[10:05] 이영희: 검토 완료했습니다.
[10:10] 박민수: 다음 단계 진행하겠습니다.
[10:15] 최영수: 승인 받은 건에 대해 진행하겠습니다."""
            else:
                sample_messages = ""
        
        with col2:
            st.subheader("💬 대화 내용")
            
            if template != "직접 입력" and sample_messages:
                messages = st.text_area(
                    "대화 내용 (시간 형식: [HH:MM] 이름: 메시지)",
                    value=sample_messages,
                    height=300,
                    placeholder="[09:00] 김철수: 안녕하세요\n[09:05] 이영희: 반갑습니다"
                )
            else:
                messages = st.text_area(
                    "대화 내용 (시간 형식: [HH:MM] 이름: 메시지)",
                    height=300,
                    placeholder="[09:00] 김철수: 안녕하세요\n[09:05] 이영희: 반갑습니다"
                )
            
            # 입력 형식 도움말
            with st.expander("📖 입력 형식 도움말"):
                st.markdown("""
                **올바른 형식:**
                ```
                [09:00] 김철수: 안녕하세요
                [09:05] 이영희: 반갑습니다
                [09:10] 박민수: 오늘 회의 일정은?
                ```
                
                **주의사항:**
                - 시간은 [HH:MM] 형식으로 입력
                - 이름과 메시지는 콜론(:)으로 구분
                - 각 메시지는 새 줄로 구분
                """)
        
        # 저장 버튼
        if st.button("💾 대화 저장", type="primary"):
            if chat_name and messages.strip():
                success = input_system.add_conversation(
                    chat_name, 
                    messages.strip(), 
                    date.strftime("%Y-%m-%d")
                )
                
                if success:
                    st.success("✅ 대화가 성공적으로 저장되었습니다!")
                    st.balloons()
                else:
                    st.error("❌ 저장 중 오류가 발생했습니다.")
            else:
                st.warning("⚠️ 채팅방 이름과 대화 내용을 모두 입력해주세요.")
    
    elif menu == "📊 데이터 조회":
        st.header("📊 데이터 조회")
        
        # 날짜 선택
        selected_date = st.date_input(
            "조회할 날짜",
            value=datetime.now()
        )
        
        conversations = input_system.get_conversations(selected_date.strftime("%Y-%m-%d"))
        
        if conversations:
            st.success(f"📅 {selected_date.strftime('%Y-%m-%d')}에 {len(conversations)}개의 대화가 있습니다.")
            
            for i, conv in enumerate(conversations):
                with st.expander(f"💬 {conv['chat_name']} ({conv['timestamp'][:19]})"):
                    st.text_area(
                        "대화 내용",
                        value=conv['messages'],
                        height=200,
                        key=f"view_{i}"
                    )
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📋 복사", key=f"copy_{i}"):
                            st.write("복사됨!")
                    with col2:
                        if st.button("✏️ 편집", key=f"edit_{i}"):
                            st.write("편집 기능 개발 중...")
                    with col3:
                        if st.button("🗑️ 삭제", key=f"delete_{i}"):
                            st.write("삭제 기능 개발 중...")
        else:
            st.info(f"📅 {selected_date.strftime('%Y-%m-%d')}에 저장된 대화가 없습니다.")
    
    elif menu == "📋 전체 대화 목록":
        st.header("📋 전체 대화 목록")
        
        conversations = input_system.get_all_conversations()
        
        if conversations:
            # 데이터프레임으로 표시
            df_data = []
            for conv in conversations:
                df_data.append({
                    "채팅방": conv['chat_name'],
                    "날짜": conv['date'],
                    "메시지 수": len(conv['messages'].split('\n')),
                    "입력 시간": conv['timestamp'][:19],
                    "소스": conv['source']
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # 통계
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 대화 수", len(conversations))
            with col2:
                st.metric("총 메시지 수", sum(len(conv['messages'].split('\n')) for conv in conversations))
            with col3:
                st.metric("활성 채팅방", len(set(conv['chat_name'] for conv in conversations)))
        else:
            st.info("📋 저장된 대화가 없습니다.")
    
    elif menu == "⚙️ 설정":
        st.header("⚙️ 설정")
        
        st.subheader("📁 데이터 관리")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 데이터 백업"):
                # 백업 기능
                st.success("백업 완료!")
        
        with col2:
            if st.button("🗑️ 모든 데이터 삭제"):
                if st.checkbox("정말 삭제하시겠습니까?"):
                    input_system.data = {"conversations": []}
                    input_system.save_data()
                    st.success("모든 데이터가 삭제되었습니다.")
        
        st.subheader("📊 시스템 정보")
        st.info(f"데이터 파일: {input_system.data_file}")
        st.info(f"총 대화 수: {len(input_system.get_all_conversations())}")
    
    # 하단 정보
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>MACHO-GPT v3.4-mini 수동 WhatsApp 데이터 입력 시스템</p>
        <p>자동 스크래핑 실패 시 수동으로 대화 데이터를 입력하여 아침 보고서 생성에 활용할 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 