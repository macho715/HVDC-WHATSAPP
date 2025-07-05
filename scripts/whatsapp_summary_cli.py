from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

import requests

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from logi_base_model import LogiBaseModel
from macho_gpt.core.logi_whatsapp_241219 import WhatsAppProcessor


class SummaryResult(LogiBaseModel):
    """대화 요약 결과 / Chat summary result"""

    key_points: List[str]
    urgent_items: List[str]


class CLI:
    """WhatsApp CLI 도우미 / WhatsApp CLI helper"""

    def __init__(self) -> None:
        self.processor = WhatsAppProcessor(mode="PRIME")

    def call_gemini_api(self, prompt: str) -> dict[str, Any]:
        """Gemini API 호출 / Call Gemini API"""
        api_key = ""
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={api_key}"
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text")
            )
            return json.loads(text) if text else {}
        except Exception:
            return {}

    def simple_summary(self, text: str) -> SummaryResult:
        """간단 요약 수행 / Run basic summary"""
        messages = self.processor.parse_whatsapp_text(text)
        urgent_items = [m.content for m in messages if m.is_urgent]
        key_points = [m.content for m in messages if not m.is_urgent][:5]
        if not key_points:
            key_points = ["주요 내용을 찾을 수 없습니다."]
        if not urgent_items:
            urgent_items = ["긴급 처리 사항이 없습니다."]
        return SummaryResult(key_points=key_points, urgent_items=urgent_items)

    def generate(self, text: str) -> SummaryResult:
        """요약 생성 / Generate summary"""
        prompt = (
            "너는 10년차 프로젝트 관리 전문가(PM)야. 다음 대화를 분석하여 핵심 "
            "내용과 긴급 사항을 요약해 JSON으로 답해줘. 반드시 keyPoints와 "
            "urgentItems 배열을 포함해야 해.\n\n" + text
        )
        data = self.call_gemini_api(prompt)
        if not data:
            return self.simple_summary(text)
        return SummaryResult(**data)


def main() -> None:
    """CLI 엔트리 포인트 / CLI entry point"""
    parser = argparse.ArgumentParser(description="WhatsApp Summary CLI")
    parser.add_argument("file", type=Path, help="WhatsApp 대화 파일 경로")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    cli = CLI()
    result = cli.generate(text)
    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main() 