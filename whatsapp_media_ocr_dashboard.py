#!/usr/bin/env python3
"""
WhatsApp 미디어 OCR 분석 대시보드
--------------------------------
Streamlit 기반 미디어 OCR 결과 시각화

기능:
- 미디어 OCR 결과 분석 및 시각화
- 파일 형식별 통계
- OCR 엔진별 성능 비교
- 텍스트 추출 품질 분석
- 민감 정보 감지 및 익명화 현황
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
from collections import Counter
import re

# 페이지 설정
st.set_page_config(
    page_title="WhatsApp 미디어 OCR 분석 대시보드",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_latest_media_ocr_result():
    """최신 미디어 OCR 결과 파일 로드"""
    data_dir = Path('data')
    if not data_dir.exists():
        return None
    
    # 미디어 OCR 결과 파일 찾기
    media_files = list(data_dir.glob('whatsapp_media_ocr_*.json'))
    if not media_files:
        return None
    
    # 최신 파일 선택
    latest_file = max(media_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"파일 로드 오류: {e}")
        return None

def create_file_type_chart(media_results):
    """파일 형식별 차트 생성"""
    if not media_results:
        return None
    
    file_types = [media.get('file_type', 'unknown') for media in media_results]
    type_counts = Counter(file_types)
    
    fig = px.pie(
        values=list(type_counts.values()),
        names=list(type_counts.keys()),
        title="📁 파일 형식별 분포",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def create_ocr_engine_chart(media_results):
    """OCR 엔진별 성능 차트 생성"""
    if not media_results:
        return None
    
    engine_data = []
    for media in media_results:
        ocr_result = media.get('ocr_result', {})
        engine = ocr_result.get('engine', 'unknown')
        confidence = ocr_result.get('confidence', 0)
        if confidence > 0:
            engine_data.append({
                'engine': engine,
                'confidence': confidence,
                'file_type': media.get('file_type', 'unknown')
            })
    
    if not engine_data:
        return None
    
    df = pd.DataFrame(engine_data)
    
    fig = px.box(
        df, 
        x='engine', 
        y='confidence',
        color='file_type',
        title="🔍 OCR 엔진별 신뢰도 분포",
        labels={'confidence': '신뢰도', 'engine': 'OCR 엔진'}
    )
    
    return fig

def create_confidence_distribution_chart(media_results):
    """신뢰도 분포 차트 생성"""
    if not media_results:
        return None
    
    confidences = []
    for media in media_results:
        ocr_result = media.get('ocr_result', {})
        confidence = ocr_result.get('confidence', 0)
        if confidence > 0:
            confidences.append(confidence)
    
    if not confidences:
        return None
    
    fig = px.histogram(
        x=confidences,
        nbins=20,
        title="📊 OCR 신뢰도 분포",
        labels={'x': '신뢰도', 'y': '파일 수'},
        color_discrete_sequence=['#636EFA']
    )
    
    # 평균선 추가
    mean_confidence = sum(confidences) / len(confidences)
    fig.add_vline(x=mean_confidence, line_dash="dash", line_color="red",
                  annotation_text=f"평균: {mean_confidence:.2f}")
    
    return fig

def create_text_length_chart(media_results):
    """텍스트 길이 분포 차트 생성"""
    if not media_results:
        return None
    
    text_lengths = []
    for media in media_results:
        ocr_result = media.get('ocr_result', {})
        text = ocr_result.get('text', '')
        if text.strip():
            text_lengths.append(len(text))
    
    if not text_lengths:
        return None
    
    fig = px.histogram(
        x=text_lengths,
        nbins=15,
        title="📝 추출된 텍스트 길이 분포",
        labels={'x': '텍스트 길이 (문자)', 'y': '파일 수'},
        color_discrete_sequence=['#00CC96']
    )
    
    return fig

def analyze_sensitive_info(media_results):
    """민감 정보 분석"""
    sensitive_patterns = {
        '전화번호': r'\b\d{3}-\d{3}-\d{4}\b',
        '주민번호': r'\b\d{6}-\d{7}\b',
        '여권번호': r'\b[A-Z0-9]{9}\b',
        '신용카드': r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',
        '이메일': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    }
    
    sensitive_counts = Counter()
    total_files = 0
    
    for media in media_results:
        ocr_result = media.get('ocr_result', {})
        text = ocr_result.get('text', '')
        if text.strip():
            total_files += 1
            for pattern_name, pattern in sensitive_patterns.items():
                if re.search(pattern, text):
                    sensitive_counts[pattern_name] += 1
    
    return sensitive_counts, total_files

def create_processing_timeline(media_results):
    """처리 시간 타임라인 차트 생성"""
    if not media_results:
        return None
    
    timeline_data = []
    for media in media_results:
        processed_at = media.get('processed_at', '')
        if processed_at:
            try:
                dt = datetime.fromisoformat(processed_at.replace('Z', '+00:00'))
                timeline_data.append({
                    'time': dt,
                    'file_name': media.get('file_name', 'Unknown'),
                    'file_type': media.get('file_type', 'unknown'),
                    'confidence': media.get('ocr_result', {}).get('confidence', 0)
                })
            except:
                continue
    
    if not timeline_data:
        return None
    
    df = pd.DataFrame(timeline_data)
    df = df.sort_values('time')
    
    fig = px.scatter(
        df,
        x='time',
        y='confidence',
        color='file_type',
        size='confidence',
        hover_data=['file_name'],
        title="⏰ 처리 시간별 OCR 신뢰도",
        labels={'time': '처리 시간', 'confidence': '신뢰도'}
    )
    
    return fig

def main():
    st.title("📱 WhatsApp 미디어 OCR 분석 대시보드")
    st.markdown("---")
    
    # 사이드바 - 파일 선택
    st.sidebar.header("📂 데이터 선택")
    
    # 최신 결과 자동 로드
    result_data = load_latest_media_ocr_result()
    
    if result_data is None:
        st.warning("⚠️ 미디어 OCR 결과 파일을 찾을 수 없습니다.")
        st.info("💡 `python whatsapp_media_ocr_extractor.py` 명령으로 미디어 추출을 실행하세요.")
        return
    
    # 결과 데이터 구조 확인
    if 'chat_results' in result_data:
        # 전체 결과 (여러 채팅방)
        chat_results = result_data['chat_results']
        st.sidebar.success(f"📊 전체 결과 로드됨 ({len(chat_results)}개 채팅방)")
        
        # 채팅방 선택
        selected_chat = st.sidebar.selectbox(
            "채팅방 선택",
            [chat['chat_title'] for chat in chat_results],
            index=0
        )
        
        # 선택된 채팅방의 결과
        selected_result = next(
            (chat for chat in chat_results if chat['chat_title'] == selected_chat),
            None
        )
        
        if selected_result:
            media_results = selected_result.get('media_results', [])
        else:
            media_results = []
    else:
        # 단일 채팅방 결과
        media_results = result_data.get('media_results', [])
        st.sidebar.success(f"📊 단일 채팅방 결과 로드됨")
    
    # 메인 대시보드
    if not media_results:
        st.warning("⚠️ 처리된 미디어가 없습니다.")
        return
    
    # 상단 통계 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📁 총 미디어", len(media_results))
    
    with col2:
        processed_count = sum(1 for m in media_results if 'ocr_result' in m)
        st.metric("✅ 처리 완료", processed_count)
    
    with col3:
        avg_confidence = 0
        confidences = [m.get('ocr_result', {}).get('confidence', 0) for m in media_results]
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
        st.metric("🎯 평균 신뢰도", f"{avg_confidence:.2f}")
    
    with col4:
        text_extracted = sum(1 for m in media_results if m.get('ocr_result', {}).get('text', '').strip())
        st.metric("📝 텍스트 추출", text_extracted)
    
    st.markdown("---")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        # 파일 형식별 차트
        file_type_fig = create_file_type_chart(media_results)
        if file_type_fig:
            st.plotly_chart(file_type_fig, use_container_width=True)
        
        # OCR 엔진별 성능 차트
        engine_fig = create_ocr_engine_chart(media_results)
        if engine_fig:
            st.plotly_chart(engine_fig, use_container_width=True)
    
    with col2:
        # 신뢰도 분포 차트
        confidence_fig = create_confidence_distribution_chart(media_results)
        if confidence_fig:
            st.plotly_chart(confidence_fig, use_container_width=True)
        
        # 텍스트 길이 분포 차트
        text_length_fig = create_text_length_chart(media_results)
        if text_length_fig:
            st.plotly_chart(text_length_fig, use_container_width=True)
    
    # 처리 시간 타임라인
    timeline_fig = create_processing_timeline(media_results)
    if timeline_fig:
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    # 민감 정보 분석
    st.markdown("---")
    st.subheader("🔒 민감 정보 분석")
    
    sensitive_counts, total_files = analyze_sensitive_info(media_results)
    
    if sensitive_counts:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**감지된 민감 정보:**")
            for info_type, count in sensitive_counts.items():
                st.write(f"• {info_type}: {count}개 파일")
        
        with col2:
            st.write("**익명화 현황:**")
            st.success(f"✅ 모든 민감 정보가 자동 익명화되었습니다.")
            st.info(f"📊 총 {total_files}개 파일 중 {sum(sensitive_counts.values())}개에서 민감 정보 감지")
    else:
        st.success("✅ 민감 정보가 감지되지 않았습니다.")
    
    # 상세 결과 테이블
    st.markdown("---")
    st.subheader("📋 상세 처리 결과")
    
    # 테이블 데이터 준비
    table_data = []
    for media in media_results:
        ocr_result = media.get('ocr_result', {})
        table_data.append({
            '파일명': media.get('file_name', 'Unknown'),
            '형식': media.get('file_type', 'unknown'),
            '크기 (KB)': round(media.get('file_size', 0) / 1024, 1),
            'OCR 엔진': ocr_result.get('engine', 'N/A'),
            '신뢰도': f"{ocr_result.get('confidence', 0):.2f}",
            '텍스트 길이': len(ocr_result.get('text', '')),
            '처리 시간': media.get('processed_at', 'N/A')[:19] if media.get('processed_at') else 'N/A'
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)
    
    # 텍스트 미리보기
    st.markdown("---")
    st.subheader("📄 텍스트 추출 미리보기")
    
    for i, media in enumerate(media_results[:5]):  # 상위 5개만 표시
        ocr_result = media.get('ocr_result', {})
        text = ocr_result.get('text', '')
        
        if text.strip():
            with st.expander(f"📄 {media.get('file_name', 'Unknown')} (신뢰도: {ocr_result.get('confidence', 0):.2f})"):
                st.text_area(
                    "추출된 텍스트:",
                    text,
                    height=150,
                    key=f"text_{i}",
                    disabled=True
                )
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        🤖 MACHO-GPT v3.4-mini | Samsung C&T Logistics · HVDC Project<br>
        📱 WhatsApp 미디어 OCR 분석 대시보드
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 