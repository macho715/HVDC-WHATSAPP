#!/usr/bin/env python3
"""
WhatsApp 미디어 OCR 분석 대시보드 (업그레이드)
-----------------------------------------------
Streamlit 기반 미디어 OCR 결과 시각화
- 다중 OCR 엔진 성능 비교
- 파일 형식별 처리 통계
- 신뢰도 분포 분석
- 처리 시간 추이
- 엔진별 정확도 비교
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
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="WhatsApp 미디어 OCR 분석 대시보드",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_latest_results():
    """최신 OCR 결과 파일 로드"""
    data_dir = Path("data")
    if not data_dir.exists():
        return None
        
    # JSON 파일 찾기
    json_files = list(data_dir.glob("whatsapp_media_ocr_*.json"))
    if not json_files:
        return None
        
    # 최신 파일 선택
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, latest_file.name
    except Exception as e:
        st.error(f"파일 로드 오류: {e}")
        return None, None

def create_engine_comparison_chart(data):
    """OCR 엔진 성능 비교 차트"""
    if not data or 'media_results' not in data:
        return None
        
    engine_stats = {}
    
    for result in data['media_results']:
        ocr_result = result.get('ocr_result', {})
        engine = ocr_result.get('engine', 'unknown')
        confidence = ocr_result.get('confidence', 0)
        
        if engine not in engine_stats:
            engine_stats[engine] = {
                'count': 0,
                'total_confidence': 0,
                'success_count': 0
            }
            
        engine_stats[engine]['count'] += 1
        engine_stats[engine]['total_confidence'] += confidence
        
        if confidence > 0:
            engine_stats[engine]['success_count'] += 1
    
    # DataFrame 생성
    df = pd.DataFrame([
        {
            'engine': engine,
            'total_files': stats['count'],
            'avg_confidence': stats['total_confidence'] / stats['count'] if stats['count'] > 0 else 0,
            'success_rate': stats['success_count'] / stats['count'] if stats['count'] > 0 else 0
        }
        for engine, stats in engine_stats.items()
    ])
    
    if df.empty:
        return None
        
    # 차트 생성
    fig = go.Figure()
    
    # 평균 신뢰도
    fig.add_trace(go.Bar(
        x=df['engine'],
        y=df['avg_confidence'],
        name='평균 신뢰도',
        marker_color='lightblue',
        yaxis='y'
    ))
    
    # 성공률
    fig.add_trace(go.Scatter(
        x=df['engine'],
        y=df['success_rate'],
        name='성공률',
        mode='lines+markers',
        line=dict(color='red', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="OCR 엔진 성능 비교",
        xaxis_title="OCR 엔진",
        yaxis=dict(title="평균 신뢰도", side="left"),
        yaxis2=dict(title="성공률", side="right", overlaying="y"),
        barmode='group',
        height=400
    )
    
    return fig

def create_file_type_distribution(data):
    """파일 형식 분포 차트"""
    if not data or 'media_results' not in data:
        return None
        
    file_types = []
    for result in data['media_results']:
        media_info = result.get('media_info', {})
        file_type = media_info.get('type', 'unknown')
        file_types.append(file_type)
    
    if not file_types:
        return None
        
    # 파일 형식 카운트
    type_counts = Counter(file_types)
    
    fig = px.pie(
        values=list(type_counts.values()),
        names=list(type_counts.keys()),
        title="파일 형식 분포",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_confidence_distribution(data):
    """신뢰도 분포 차트"""
    if not data or 'media_results' not in data:
        return None
        
    confidences = []
    engines = []
    
    for result in data['media_results']:
        ocr_result = result.get('ocr_result', {})
        confidence = ocr_result.get('confidence', 0)
        engine = ocr_result.get('engine', 'unknown')
        
        if confidence > 0:
            confidences.append(confidence)
            engines.append(engine)
    
    if not confidences:
        return None
        
    df = pd.DataFrame({
        'confidence': confidences,
        'engine': engines
    })
    
    fig = px.histogram(
        df,
        x='confidence',
        color='engine',
        title="OCR 신뢰도 분포",
        nbins=20,
        opacity=0.7
    )
    
    fig.update_layout(
        xaxis_title="신뢰도",
        yaxis_title="파일 수",
        height=400
    )
    
    return fig

def create_processing_timeline(data):
    """처리 시간 추이 차트"""
    if not data or 'media_results' not in data:
        return None
        
    timestamps = []
    engines = []
    confidences = []
    
    for result in data['media_results']:
        processed_at = result.get('processed_at')
        ocr_result = result.get('ocr_result', {})
        
        if processed_at:
            try:
                timestamp = datetime.fromisoformat(processed_at.replace('Z', '+00:00'))
                timestamps.append(timestamp)
                engines.append(ocr_result.get('engine', 'unknown'))
                confidences.append(ocr_result.get('confidence', 0))
            except:
                continue
    
    if not timestamps:
        return None
        
    df = pd.DataFrame({
        'timestamp': timestamps,
        'engine': engines,
        'confidence': confidences
    })
    
    fig = px.scatter(
        df,
        x='timestamp',
        y='confidence',
        color='engine',
        title="처리 시간별 OCR 성능",
        size='confidence',
        hover_data=['engine']
    )
    
    fig.update_layout(
        xaxis_title="처리 시간",
        yaxis_title="신뢰도",
        height=400
    )
    
    return fig

def analyze_sensitive_info(data):
    """민감 정보 분석"""
    if not data or 'media_results' not in data:
        return None
        
    sensitive_patterns = {
        'phone': r'\[PHONE\]',
        'email': r'\[EMAIL\]',
        'id_number': r'\[ID_NUMBER\]',
        'card_number': r'\[CARD_NUMBER\]'
    }
    
    sensitive_counts = {k: 0 for k in sensitive_patterns.keys()}
    total_texts = 0
    
    for result in data['media_results']:
        ocr_result = result.get('ocr_result', {})
        text = ocr_result.get('text', '')
        
        if text:
            total_texts += 1
            for pattern_name, pattern in sensitive_patterns.items():
                if re.search(pattern, text):
                    sensitive_counts[pattern_name] += 1
    
    return sensitive_counts, total_texts

def create_performance_metrics(data):
    """성능 지표 카드"""
    if not data:
        return None
        
    metrics = {}
    
    # 기본 통계
    metrics['total_media'] = data.get('media_count', 0)
    metrics['processed_media'] = data.get('processed_count', 0)
    metrics['success_rate'] = (metrics['processed_media'] / metrics['total_media'] * 100) if metrics['total_media'] > 0 else 0
    
    # OCR 엔진 통계
    if 'media_results' in data:
        engines = [r.get('ocr_result', {}).get('engine', 'unknown') for r in data['media_results']]
        engine_counts = Counter(engines)
        metrics['engines_used'] = len(engine_counts)
        metrics['most_used_engine'] = engine_counts.most_common(1)[0][0] if engine_counts else 'N/A'
        
        # 평균 신뢰도
        confidences = [r.get('ocr_result', {}).get('confidence', 0) for r in data['media_results']]
        confidences = [c for c in confidences if c > 0]
        metrics['avg_confidence'] = np.mean(confidences) if confidences else 0
    
    return metrics

def main():
    st.title("📱 WhatsApp 미디어 OCR 분석 대시보드 (업그레이드)")
    st.markdown("---")
    
    # 데이터 로드
    data, filename = load_latest_results()
    
    if not data:
        st.warning("📁 OCR 결과 파일을 찾을 수 없습니다.")
        st.info("먼저 WhatsApp 미디어 OCR 추출기를 실행해주세요.")
        return
    
    st.success(f"✅ 데이터 로드 완료: {filename}")
    
    # 성능 지표
    metrics = create_performance_metrics(data)
    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 미디어", metrics['total_media'])
        with col2:
            st.metric("처리 완료", metrics['processed_media'])
        with col3:
            st.metric("성공률", f"{metrics['success_rate']:.1f}%")
        with col4:
            st.metric("평균 신뢰도", f"{metrics['avg_confidence']:.2f}")
    
    st.markdown("---")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        # OCR 엔진 성능 비교
        engine_chart = create_engine_comparison_chart(data)
        if engine_chart:
            st.plotly_chart(engine_chart, use_container_width=True)
        else:
            st.info("OCR 엔진 성능 데이터가 없습니다.")
    
    with col2:
        # 파일 형식 분포
        file_chart = create_file_type_distribution(data)
        if file_chart:
            st.plotly_chart(file_chart, use_container_width=True)
        else:
            st.info("파일 형식 데이터가 없습니다.")
    
    # 신뢰도 분포
    confidence_chart = create_confidence_distribution(data)
    if confidence_chart:
        st.plotly_chart(confidence_chart, use_container_width=True)
    else:
        st.info("신뢰도 데이터가 없습니다.")
    
    # 처리 시간 추이
    timeline_chart = create_processing_timeline(data)
    if timeline_chart:
        st.plotly_chart(timeline_chart, use_container_width=True)
    else:
        st.info("처리 시간 데이터가 없습니다.")
    
    # 민감 정보 분석
    st.markdown("---")
    st.subheader("🔒 민감 정보 분석")
    
    sensitive_counts, total_texts = analyze_sensitive_info(data)
    if sensitive_counts and total_texts > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("전화번호", sensitive_counts['phone'])
        with col2:
            st.metric("이메일", sensitive_counts['email'])
        with col3:
            st.metric("주민번호", sensitive_counts['id_number'])
        with col4:
            st.metric("카드번호", sensitive_counts['card_number'])
        
        st.info(f"총 {total_texts}개 텍스트에서 민감 정보가 자동으로 익명화되었습니다.")
    else:
        st.info("민감 정보가 포함된 텍스트가 없습니다.")
    
    # 상세 결과 테이블
    st.markdown("---")
    st.subheader("📋 상세 OCR 결과")
    
    if 'media_results' in data and data['media_results']:
        # 결과를 DataFrame으로 변환
        results_data = []
        for i, result in enumerate(data['media_results']):
            media_info = result.get('media_info', {})
            ocr_result = result.get('ocr_result', {})
            
            results_data.append({
                '번호': i + 1,
                '파일명': result.get('file_path', 'N/A').split('/')[-1],
                '미디어 타입': media_info.get('type', 'unknown'),
                'OCR 엔진': ocr_result.get('engine', 'N/A'),
                '신뢰도': f"{ocr_result.get('confidence', 0):.2f}",
                '텍스트 길이': len(ocr_result.get('text', '')),
                '처리 시간': result.get('processed_at', 'N/A')
            })
        
        df = pd.DataFrame(results_data)
        st.dataframe(df, use_container_width=True)
        
        # 텍스트 미리보기
        if st.checkbox("텍스트 내용 미리보기"):
            for i, result in enumerate(data['media_results'][:5]):  # 처음 5개만
                ocr_result = result.get('ocr_result', {})
                text = ocr_result.get('text', '')
                
                if text:
                    st.markdown(f"**파일 {i+1}:**")
                    st.text_area(f"텍스트 내용", text[:500] + "..." if len(text) > 500 else text, 
                               height=100, key=f"text_{i}")
    else:
        st.info("OCR 처리된 미디어가 없습니다.")
    
    # 사이드바 정보
    st.sidebar.title("📊 대시보드 정보")
    st.sidebar.info(f"**데이터 파일:** {filename}")
    st.sidebar.info(f"**채팅방:** {data.get('chat_title', 'N/A')}")
    st.sidebar.info(f"**처리 상태:** {data.get('status', 'N/A')}")
    st.sidebar.info(f"**추출 시간:** {data.get('extraction_time', 'N/A')}")
    
    # 새로고침 버튼
    if st.sidebar.button("🔄 데이터 새로고침"):
        st.rerun()

if __name__ == "__main__":
    main() 