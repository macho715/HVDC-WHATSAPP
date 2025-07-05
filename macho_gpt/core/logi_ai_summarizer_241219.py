"""
MACHO-GPT v3.4-mini - AI Summarizer Module
Samsung C&T Logistics · HVDC Project Integration
"""

import openai
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class LogiAISummarizer:
    """MACHO-GPT AI 요약 처리기"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        AI 요약 처리기 초기화
        
        Args:
            api_key: OpenAI API 키
            model: 사용할 모델 (기본값: gpt-4o-mini)
        """
        self.model = model
        self.confidence_threshold = 0.90
        
        if api_key:
            openai.api_key = api_key
    
    def summarize_conversation(self, messages: List[str]) -> Dict[str, Any]:
        """
        대화 내용을 요약하고 태스크를 추출합니다
        
        Args:
            messages: 메시지 리스트
            
        Returns:
            dict: 요약, 태스크, 신뢰도 등을 포함한 결과
        """
        try:
            # 메시지 전처리
            conversation_text = "\n".join(messages)
            
            # OpenAI API 호출
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": conversation_text}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # 응답 파싱
            result = self._parse_response(response.choices[0].message.content)
            result['confidence'] = self._calculate_confidence(result)
            result['timestamp'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"요약 처리 오류: {str(e)}")
            return {
                "summary": "오류로 인해 요약을 생성할 수 없습니다.",
                "tasks": [],
                "urgent": [],
                "important": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _get_system_prompt(self) -> str:
        """시스템 프롬프트 생성"""
        return """
        당신은 MACHO-GPT v3.4-mini, Samsung C&T 물류 전문 AI입니다.
        
        WhatsApp 대화를 분석하여 다음을 추출하세요:
        1. 핵심 요약 (3-5줄)
        2. 실행 가능한 태스크 목록
        3. 긴급 사항
        4. 중요 사항
        
        응답 형식:
        **요약:**
        [핵심 내용 요약]
        
        **태스크:**
        - [태스크 1]
        - [태스크 2]
        
        **긴급:**
        - [긴급 사항]
        
        **중요:**
        - [중요 사항]
        
        물류, HVDC 프로젝트, 업무 관련 내용을 우선적으로 분석하세요.
        """
    
    def _parse_response(self, response_text: str) -> Dict[str, List[str]]:
        """AI 응답을 파싱하여 구조화된 데이터로 변환"""
        result = {
            "summary": "",
            "tasks": [],
            "urgent": [],
            "important": []
        }
        
        try:
            lines = response_text.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('**요약:**'):
                    current_section = 'summary'
                elif line.startswith('**태스크:**'):
                    current_section = 'tasks'
                elif line.startswith('**긴급:**'):
                    current_section = 'urgent'
                elif line.startswith('**중요:**'):
                    current_section = 'important'
                elif line.startswith('- '):
                    # 리스트 항목
                    item = line[2:].strip()
                    if current_section in ['tasks', 'urgent', 'important']:
                        result[current_section].append(item)
                else:
                    # 요약 내용
                    if current_section == 'summary':
                        if result['summary']:
                            result['summary'] += ' ' + line
                        else:
                            result['summary'] = line
            
            return result
            
        except Exception as e:
            logger.error(f"응답 파싱 오류: {str(e)}")
            return result
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """결과의 신뢰도 계산"""
        score = 0.0
        
        # 요약 길이 점수 (10-200자 적정)
        summary_len = len(result.get('summary', ''))
        if 10 <= summary_len <= 200:
            score += 0.3
        elif summary_len > 0:
            score += 0.1
        
        # 태스크 개수 점수 (1-10개 적정)
        task_count = len(result.get('tasks', []))
        if 1 <= task_count <= 10:
            score += 0.4
        elif task_count > 0:
            score += 0.2
        
        # 긴급/중요 사항 점수
        urgent_count = len(result.get('urgent', []))
        important_count = len(result.get('important', []))
        if urgent_count > 0 or important_count > 0:
            score += 0.3
        
        return min(score, 1.0)
    
    def get_status(self) -> Dict[str, Any]:
        """처리기 상태 정보 반환"""
        return {
            "model": self.model,
            "confidence_threshold": self.confidence_threshold,
            "status": "ready",
            "version": "3.4-mini"
        }

# 전역 인스턴스 생성
logi_ai_summarizer = LogiAISummarizer()

__all__ = ["LogiAISummarizer", "logi_ai_summarizer"] 