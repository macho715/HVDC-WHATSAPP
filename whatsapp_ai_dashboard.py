"""
MACHO-GPT v3.4-mini WhatsApp AI Dashboard
HVDC Project - Samsung C&T Logistics
"""

import json
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from collections import Counter

def load_ai_analysis(file_path: str):
    """Load AI analysis results"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load analysis: {e}")
        return None

def create_keyword_chart(keywords: list):
    """Create keyword frequency chart"""
    if not keywords:
        return None
    
    # Count keyword frequency
    keyword_counts = Counter(keywords)
    
    # Create DataFrame
    df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Frequency'])
    df = df.sort_values('Frequency', ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(df, x='Frequency', y='Keyword', orientation='h',
                 title='🔍 핵심 키워드 빈도 분석',
                 color='Frequency',
                 color_continuous_scale='viridis')
    
    fig.update_layout(
        height=400,
        xaxis_title="빈도",
        yaxis_title="키워드",
        showlegend=False
    )
    
    return fig

def create_sentiment_chart(analyses: list):
    """Create sentiment analysis chart"""
    sentiments = []
    for analysis in analyses:
        if 'analysis' in analysis and isinstance(analysis['analysis'], dict):
            sentiment = analysis['analysis'].get('sentiment', '중립')
            sentiments.append(sentiment)
    
    if not sentiments:
        return None
    
    # Count sentiments
    sentiment_counts = Counter(sentiments)
    
    # Create pie chart
    fig = px.pie(values=list(sentiment_counts.values()), 
                 names=list(sentiment_counts.keys()),
                 title='📊 감정 분석 결과',
                 color_discrete_map={
                     '긍정': '#2E8B57',
                     '부정': '#DC143C', 
                     '중립': '#4682B4'
                 })
    
    fig.update_layout(height=400)
    return fig

def create_message_count_chart(analyses: list):
    """Create message count chart"""
    chat_titles = []
    message_counts = []
    
    for analysis in analyses:
        chat_titles.append(analysis.get('chat_title', 'Unknown'))
        message_counts.append(analysis.get('message_count', 0))
    
    if not chat_titles:
        return None
    
    # Create bar chart
    fig = px.bar(x=chat_titles, y=message_counts,
                 title='📱 채팅방별 메시지 수',
                 labels={'x': '채팅방', 'y': '메시지 수'},
                 color=message_counts,
                 color_continuous_scale='plasma')
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig

def create_issue_timeline_chart(analyses: list):
    """Create issue timeline chart"""
    issues = []
    for analysis in analyses:
        if 'analysis' in analysis and isinstance(analysis['analysis'], dict):
            issue = analysis['analysis'].get('issues', '')
            if issue and issue != '문제점 없음':
                issues.append({
                    'chat': analysis.get('chat_title', 'Unknown'),
                    'issue': issue[:50] + '...' if len(issue) > 50 else issue
                })
    
    if not issues:
        return None
    
    # Create timeline chart
    fig = go.Figure()
    
    for i, issue_data in enumerate(issues):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[issue_data['chat']],
            mode='markers+text',
            marker=dict(size=15, color='red'),
            text=issue_data['issue'],
            textposition='top center',
            name=issue_data['chat'],
            showlegend=False
        ))
    
    fig.update_layout(
        title='⚠️ 문제점 타임라인',
        height=300,
        xaxis=dict(showticklabels=False),
        yaxis=dict(title='채팅방'),
        showlegend=False
    )
    
    return fig

def create_action_priority_chart(analyses: list):
    """Create action priority chart"""
    actions = []
    for analysis in analyses:
        if 'analysis' in analysis and isinstance(analysis['analysis'], dict):
            action = analysis['analysis'].get('actions', '')
            if action and action != '조치사항 없음':
                actions.append({
                    'chat': analysis.get('chat_title', 'Unknown'),
                    'action': action[:50] + '...' if len(action) > 50 else action
                })
    
    if not actions:
        return None
    
    # Create priority chart
    fig = go.Figure()
    
    for i, action_data in enumerate(actions):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[action_data['chat']],
            mode='markers+text',
            marker=dict(size=15, color='green'),
            text=action_data['action'],
            textposition='top center',
            name=action_data['chat'],
            showlegend=False
        ))
    
    fig.update_layout(
        title='✅ 조치사항 우선순위',
        height=300,
        xaxis=dict(showticklabels=False),
        yaxis=dict(title='채팅방'),
        showlegend=False
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="MACHO-GPT WhatsApp AI Dashboard",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 MACHO-GPT v3.4-mini WhatsApp AI 대시보드")
    st.subheader("HVDC Project - Samsung C&T Logistics")
    
    # Load latest analysis
    reports_dir = Path("reports")
    if not reports_dir.exists():
        st.error("📁 reports 폴더를 찾을 수 없습니다.")
        return
    
    # Find latest analysis file
    analysis_files = list(reports_dir.glob("ai_analysis_*.json"))
    if not analysis_files:
        st.error("📊 AI 분석 파일을 찾을 수 없습니다.")
        return
    
    latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
    st.info(f"📄 분석 파일: {latest_file.name}")
    
    # Load analysis
    analysis = load_ai_analysis(latest_file)
    if not analysis:
        return
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("채팅방 수", analysis.get('total_chats_analyzed', 0))
    
    with col2:
        st.metric("총 메시지", analysis.get('total_messages', 0))
    
    with col3:
        st.metric("키워드 수", analysis.get('overall_summary', {}).get('total_keywords', 0))
    
    with col4:
        timestamp = analysis.get('analysis_timestamp', '')
        if timestamp:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            st.metric("분석 시간", dt.strftime('%H:%M:%S'))
    
    st.divider()
    
    # Create charts - First row
    col1, col2 = st.columns(2)
    
    with col1:
        # Message count chart
        message_fig = create_message_count_chart(analysis.get('chat_analyses', []))
        if message_fig:
            st.plotly_chart(message_fig, use_container_width=True)
        
        # Sentiment chart
        sentiment_fig = create_sentiment_chart(analysis.get('chat_analyses', []))
        if sentiment_fig:
            st.plotly_chart(sentiment_fig, use_container_width=True)
    
    with col2:
        # Keyword chart
        keywords = analysis.get('overall_summary', {}).get('common_keywords', [])
        keyword_fig = create_keyword_chart(keywords)
        if keyword_fig:
            st.plotly_chart(keyword_fig, use_container_width=True)
    
    st.divider()
    
    # Create charts - Second row (Issues and Actions)
    col1, col2 = st.columns(2)
    
    with col1:
        # Issue timeline chart
        issue_fig = create_issue_timeline_chart(analysis.get('chat_analyses', []))
        if issue_fig:
            st.plotly_chart(issue_fig, use_container_width=True)
    
    with col2:
        # Action priority chart
        action_fig = create_action_priority_chart(analysis.get('chat_analyses', []))
        if action_fig:
            st.plotly_chart(action_fig, use_container_width=True)
    
    st.divider()
    
    # Display unique insights
    st.subheader("🎯 핵심 인사이트")
    
    # Extract unique insights from all analyses
    unique_insights = set()
    unique_issues = set()
    unique_actions = set()
    
    for chat_analysis in analysis.get('chat_analyses', []):
        if 'analysis' in chat_analysis and isinstance(chat_analysis['analysis'], dict):
            analysis_data = chat_analysis['analysis']
            
            # Collect unique insights
            summary = analysis_data.get('summary', '')
            if summary and summary != '요약 없음':
                unique_insights.add(summary[:100] + '...' if len(summary) > 100 else summary)
            
            # Collect unique issues
            issues = analysis_data.get('issues', '')
            if issues and issues != '문제점 없음':
                unique_issues.add(issues[:100] + '...' if len(issues) > 100 else issues)
            
            # Collect unique actions
            actions = analysis_data.get('actions', '')
            if actions and actions != '조치사항 없음':
                unique_actions.add(actions[:100] + '...' if len(actions) > 100 else actions)
    
    # Display unique insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**💡 주요 인사이트:**")
        if unique_insights:
            for insight in list(unique_insights)[:3]:
                st.write(f"• {insight}")
        else:
            st.write("인사이트 없음")
    
    with col2:
        st.write("**⚠️ 주요 문제점:**")
        if unique_issues:
            for issue in list(unique_issues)[:3]:
                st.write(f"• {issue}")
        else:
            st.write("문제점 없음")
    
    with col3:
        st.write("**✅ 주요 조치사항:**")
        if unique_actions:
            for action in list(unique_actions)[:3]:
                st.write(f"• {action}")
        else:
            st.write("조치사항 없음")
    
    st.divider()
    
    # Display chat-specific highlights
    st.subheader("📱 채팅방별 주요 특징")
    
    for chat_analysis in analysis.get('chat_analyses', []):
        chat_title = chat_analysis.get('chat_title', 'Unknown')
        message_count = chat_analysis.get('message_count', 0)
        
        with st.expander(f"💬 {chat_title} ({message_count}개 메시지)"):
            analysis_data = chat_analysis.get('analysis', {})
            
            # Show only unique or important information
            col1, col2 = st.columns(2)
            
            with col1:
                # Keywords
                keywords = analysis_data.get('keywords', [])
                if keywords:
                    st.write("**🏷️ 주요 키워드:**")
                    st.write(", ".join(keywords[:5]))  # Show only top 5
                
                # Schedule
                schedule = analysis_data.get('schedule', '')
                if schedule and schedule != '일정 없음':
                    st.write("**📅 주요 일정:**")
                    st.write(schedule)
                
                # Progress
                progress = analysis_data.get('progress', '')
                if progress and progress != '진행 현황 없음':
                    st.write("**🔄 진행 현황:**")
                    st.write(progress)
            
            with col2:
                # Sentiment with color coding
                sentiment = analysis_data.get('sentiment', '중립')
                st.write("**😊 감정 분석:**")
                if sentiment == '긍정':
                    st.success(sentiment)
                elif sentiment == '부정':
                    st.error(sentiment)
                else:
                    st.info(sentiment)
                
                # Unique issues (if different from common ones)
                issues = analysis_data.get('issues', '')
                if issues and issues != '문제점 없음':
                    st.write("**⚠️ 특이사항:**")
                    st.write(issues)
                
                # Unique actions (if different from common ones)
                actions = analysis_data.get('actions', '')
                if actions and actions != '조치사항 없음':
                    st.write("**✅ 특별 조치:**")
                    st.write(actions)
    
    # Overall summary
    st.divider()
    st.subheader("🎯 전체 프로젝트 현황")
    
    overall = analysis.get('overall_summary', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🔍 핵심 키워드 (상위 10개):**")
        keywords = overall.get('common_keywords', [])
        if keywords:
            for i, keyword in enumerate(keywords[:10], 1):
                st.write(f"{i}. {keyword}")
        else:
            st.write("키워드 없음")
    
    with col2:
        st.write("**⚠️ 주요 문제점:**")
        issues = overall.get('main_issues', [])
        if issues:
            for i, issue in enumerate(issues[:5], 1):  # Show only top 5
                st.write(f"{i}. {issue}")
        else:
            st.write("문제점 없음")
    
    st.write("**✅ 우선 조치사항:**")
    actions = overall.get('required_actions', [])
    if actions:
        for i, action in enumerate(actions[:5], 1):  # Show only top 5
            st.write(f"{i}. {action}")
    else:
        st.write("조치사항 없음")
    
    # Footer
    st.divider()
    st.caption("🤖 MACHO-GPT v3.4-mini | HVDC Project | Samsung C&T Logistics")

if __name__ == "__main__":
    main() 