#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini WhatsApp Summary CLI Tool
Samsung C&T Logistics · HVDC Project

Command-line interface for WhatsApp message summarization with AI integration.
Supports both Gemini API and fallback processing.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

import requests

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from logi_base_model import LogiBaseModel
from macho_gpt.core.logi_whatsapp_241219 import WhatsAppProcessor
from macho_gpt.core.role_config import get_enhanced_system_prompt, get_role_status


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SummaryResult(LogiBaseModel):
    """대화 요약 결과 / Chat summary result"""
    
    key_points: List[str]
    urgent_items: List[str]
    total_messages: int
    summary_date: str
    confidence_score: float = 0.0
    processing_mode: str = "PRIME"


class CLI:
    """WhatsApp CLI 도우미 / WhatsApp CLI helper"""

    def __init__(self, mode: str = "PRIME") -> None:
        self.processor = WhatsAppProcessor(mode=mode)
        self.mode = mode
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
    def call_gemini_api(self, prompt: str) -> dict[str, Any]:
        """Gemini API 호출 / Call Gemini API"""
        if not self.gemini_api_key:
            logger.warning("Gemini API 키가 설정되지 않았습니다. 기본 요약을 사용합니다.")
            return {}
            
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={self.gemini_api_key}"
        )
        
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.3,
                "maxOutputTokens": 1000
            }
        }
        
        try:
            logger.info("Gemini API 호출 중...")
            response = requests.post(url, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text")
            )
            
            if text:
                result = json.loads(text)
                logger.info("Gemini API 호출 성공")
                return result
            else:
                logger.warning("Gemini API 응답에서 텍스트를 찾을 수 없습니다.")
                return {}
                
        except requests.exceptions.Timeout:
            logger.error("Gemini API 호출 시간 초과")
            return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API 호출 실패: {e}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Gemini API 응답 JSON 파싱 실패: {e}")
            return {}
        except Exception as e:
            logger.error(f"Gemini API 호출 중 예상치 못한 오류: {e}")
            return {}

    def simple_summary(self, text: str) -> SummaryResult:
        """간단 요약 수행 / Run basic summary"""
        try:
            messages = self.processor.parse_whatsapp_text(text)
            
            # 긴급 메시지 추출
            urgent_items = [m.content for m in messages if m.is_urgent][:3]
            
            # 주요 메시지 추출 (긴급하지 않은 것들)
            key_points = [m.content for m in messages if not m.is_urgent][:5]
            
            # 기본값 설정
            if not key_points:
                key_points = ["주요 내용을 찾을 수 없습니다."]
            if not urgent_items:
                urgent_items = ["긴급 처리 사항이 없습니다."]
                
            return SummaryResult(
                key_points=key_points,
                urgent_items=urgent_items,
                total_messages=len(messages),
                summary_date=datetime.now().isoformat(),
                confidence_score=0.7,
                processing_mode="BASIC"
            )
            
        except Exception as e:
            logger.error(f"기본 요약 처리 중 오류: {e}")
            return SummaryResult(
                key_points=["요약 처리 중 오류가 발생했습니다."],
                urgent_items=["시스템 오류로 인해 긴급 사항을 확인할 수 없습니다."],
                total_messages=0,
                summary_date=datetime.now().isoformat(),
                confidence_score=0.0,
                processing_mode="ERROR"
            )

    def generate(self, text: str) -> SummaryResult:
        """요약 생성 / Generate summary"""
        # Role Configuration 적용
        base_prompt = """
        다음 WhatsApp 대화를 분석하여 핵심 내용과 긴급 사항을 요약해주세요.
        
        요구사항:
        1. keyPoints: 주요 활동 및 논의 사항 (3-5개)
        2. urgentItems: 긴급 처리 필요한 사항 (1-3개)
        3. 한국어로 응답
        4. JSON 형식으로만 응답
        
        대화 내용:
        """
        
        enhanced_prompt = get_enhanced_system_prompt(base_prompt + text)
        
        # Gemini API 호출
        data = self.call_gemini_api(enhanced_prompt)
        
        if data and "keyPoints" in data and "urgentItems" in data:
            # AI 요약 성공
            messages = self.processor.parse_whatsapp_text(text)
            return SummaryResult(
                key_points=data["keyPoints"],
                urgent_items=data["urgentItems"],
                total_messages=len(messages),
                summary_date=datetime.now().isoformat(),
                confidence_score=0.9,
                processing_mode=self.mode
            )
        else:
            # AI 요약 실패 시 기본 요약 사용
            logger.info("AI 요약 실패, 기본 요약으로 대체")
            return self.simple_summary(text)

    def save_summary(self, result: SummaryResult, output_file: Optional[Path] = None) -> None:
        """요약 결과 저장 / Save summary result"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Path(f"whatsapp_summary_{timestamp}.json")
            
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result.model_dump(), f, ensure_ascii=False, indent=2)
            logger.info(f"요약 결과가 저장되었습니다: {output_file}")
        except Exception as e:
            logger.error(f"파일 저장 중 오류: {e}")

    def display_summary(self, result: SummaryResult, verbose: bool = False) -> None:
        """요약 결과 표시 / Display summary result"""
        print("\n" + "="*60)
        print("🤖 MACHO-GPT v3.4-mini WhatsApp 요약 결과")
        print("="*60)
        
        print(f"📅 생성일시: {result.summary_date}")
        print(f"🎯 처리모드: {result.processing_mode}")
        print(f"📊 신뢰도: {result.confidence_score:.1%}")
        print(f"💬 총 메시지: {result.total_messages}개")
        
        print("\n🔑 주요 내용:")
        for i, point in enumerate(result.key_points, 1):
            print(f"  {i}. {point}")
            
        print("\n🚨 긴급 사항:")
        for i, item in enumerate(result.urgent_items, 1):
            print(f"  {i}. {item}")
            
        if verbose:
            print(f"\n📋 Role Configuration 상태:")
            role_status = get_role_status()
            for key, value in role_status.items():
                print(f"  {key}: {value}")
        
        print("="*60)


def main() -> None:
    """CLI 엔트리 포인트 / CLI entry point"""
    parser = argparse.ArgumentParser(
        description="MACHO-GPT v3.4-mini WhatsApp Summary CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python whatsapp_summary_cli.py chat.txt
  python whatsapp_summary_cli.py chat.txt --output summary.json
  python whatsapp_summary_cli.py chat.txt --mode ZERO --verbose
        """
    )
    
    parser.add_argument("file", type=Path, help="WhatsApp 대화 파일 경로")
    parser.add_argument(
        "--output", "-o", 
        type=Path, 
        help="출력 파일 경로 (기본: 자동 생성)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["PRIME", "ZERO", "LATTICE", "RHYTHM"],
        default="PRIME",
        help="처리 모드 (기본: PRIME)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="상세 정보 출력"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="결과를 파일로 저장"
    )
    
    args = parser.parse_args()
    
    # 파일 존재 확인
    if not args.file.exists():
        logger.error(f"파일을 찾을 수 없습니다: {args.file}")
        sys.exit(1)
    
    try:
        # 파일 읽기
        text = args.file.read_text(encoding="utf-8")
        logger.info(f"파일 읽기 완료: {args.file} ({len(text)} 문자)")
        
        # CLI 초기화 및 요약 생성
        cli = CLI(mode=args.mode)
        result = cli.generate(text)
        
        # 결과 표시
        cli.display_summary(result, verbose=args.verbose)
        
        # 파일 저장
        if args.save or args.output:
            cli.save_summary(result, args.output)
            
        # JSON 출력 (기본)
        if not args.verbose:
            print("\n📄 JSON 형식:")
            print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
            
    except UnicodeDecodeError:
        logger.error("파일 인코딩 오류. UTF-8 형식으로 저장된 파일인지 확인하세요.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"처리 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 