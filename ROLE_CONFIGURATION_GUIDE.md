# 🛠️ MACHO-GPT v3.4-mini Role Configuration 가이드

## Executive Summary

아래 예시는 **MACHO-GPT v3.4-mini** (WhatsApp 자동화 시스템) 안에 "내 업무 정의"를 **한·영 혼용**으로 요약하여 **시스템 프롬프트/환경설정에 삽입**하는 방법이다. 프로젝트 코드에서 공통으로 임포트할 수 있는 **`role_config.py`** 파일(또는 `.env`, `config.yaml`)을 만들어 두면, 이후 모든 LLM 호출 시 **자동으로 내 역할이 주입**되어 답변 일관성을 확보할 수 있다.

---

## 1️⃣ Python 모듈 방식 (권장)

```python
# macho_gpt/core/role_config.py
ROLE_DESCRIPTION: str = """
🛠️ Samsung C&T Logistics – Middle-East HVDC Mega-Project Copilot (영·한)
• Position: Logistics · Customs · Contract Lead (PMT Tier-1)
• Scope: Import/Export clearance, ADNOC-DSV port ops, storage & inland haulage,
         contract negotiation, cost simulation, regulatory diff-watch, KPI dashboard
• Mission: T+0 decision support, document automation, risk mitigation,
           25 %+ productivity uplift across 10 modules
• Key APIs / Docs: eDAS, UAE Customs, AD Ports, MOEI, FANR, HVDC Mapping System
"""
```

### 사용 예

```python
from macho_gpt.core.role_config import ROLE_DESCRIPTION
from openai import OpenAI

SYSTEM_PROMPT = (
    f"{ROLE_DESCRIPTION}\n\n"
    "You are MACHO-GPT v3.4-mini. Follow company style guides and safety rules."
)

response = OpenAI().chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": SYSTEM_PROMPT},
              {"role": "user", "content": user_query}]
)
```

> **장점**
>
> * 파이썬 import 한 줄로 전 모듈 재사용 (DRY)
> * Git 버전 관리 용이, 다중 환경(dev/stg/prod) 지원

---

## 2️⃣ `.env` 환경변수 방식 (초간단)

```bash
# .env  (루트 디렉터리)
USER_ROLE="SCT Logistics – HVDC Mega Project Lead · 통관·물류·계약 담당"
```

```python
from dotenv import load_dotenv, dotenv_values
load_dotenv()
ROLE_DESCRIPTION = dotenv_values().get("USER_ROLE", "")
```

---

## 3️⃣ `config.yaml` 중앙관리 (대규모 팀)

```yaml
# config/config.yaml
role:
  id: SCT-HVDC-LOGI-LEAD
  description: >
    Samsung C&T Logistics – HVDC Mega-Project Copilot.
    Oversees customs clearance, contracts, inland & offshore transport, KPI boards.
  version: "3.4-mini"
  project: "HVDC"
```

```python
import yaml, pathlib
ROLE_DESCRIPTION = yaml.safe_load(
    pathlib.Path("config/config.yaml").read_text()
)["role"]["description"]
```

---

## 4️⃣ 통합 적용 가이드

| 단계 | 작업                                    | 스크립트/파일                        | 확인 포인트                   |
| -- | ------------------------------------- | ------------------------------ | ------------------------ |
| ①  | `role_config.py` 또는 `.env` 작성         | `macho_gpt/core/`              | 한·영 혼용, 최신 직책 반영         |
| ②  | AI 호출 부분에 **`ROLE_DESCRIPTION` 프리펜드** | `logi_ai_summarizer_*.py`      | 기존 `SYSTEM_PROMPT` 변수 수정 |
| ③  | 단위테스트 추가                              | `tests/test_role_injection.py` | 프롬프트에 직책 문구 포함 여부        |
| ④  | CI 배포                                 | `GitHub Actions`               | `.env secrets` 암호화 관리    |

---

## 5️⃣ 실제 구현 예제

### Step 1: Role Configuration 파일 생성

```python
# macho_gpt/core/role_config.py
"""
MACHO-GPT v3.4-mini Role Configuration
Samsung C&T Logistics · HVDC Project
"""

from typing import Dict, Any
from pathlib import Path
import os

# 기본 역할 정의
DEFAULT_ROLE_DESCRIPTION = """
🛠️ Samsung C&T Logistics – Middle-East HVDC Mega-Project Copilot (영·한)
• Position: Logistics · Customs · Contract Lead (PMT Tier-1)
• Scope: Import/Export clearance, ADNOC-DSV port ops, storage & inland haulage,
         contract negotiation, cost simulation, regulatory diff-watch, KPI dashboard
• Mission: T+0 decision support, document automation, risk mitigation,
           25% productivity uplift across 10 modules
• Key APIs / Docs: eDAS, UAE Customs, AD Ports, MOEI, FANR, HVDC Mapping System
• Mode: PRIME|ORACLE|ZERO|LATTICE|RHYTHM|COST-GUARD
• Confidence: ≥0.90 required for all operations
"""

def get_role_description() -> str:
    """
    역할 설명 반환 (환경변수 우선)
    
    Returns:
        str: 역할 설명 텍스트
    """
    # 환경변수에서 먼저 확인
    env_role = os.getenv('MACHO_GPT_ROLE_DESCRIPTION')
    if env_role:
        return env_role
    
    # 기본값 반환
    return DEFAULT_ROLE_DESCRIPTION

def get_enhanced_system_prompt(base_prompt: str = "") -> str:
    """
    역할 정의가 포함된 향상된 시스템 프롬프트 생성
    
    Args:
        base_prompt: 기본 프롬프트 텍스트
        
    Returns:
        str: 향상된 시스템 프롬프트
    """
    role_desc = get_role_description()
    
    enhanced_prompt = f"""
{role_desc}

{base_prompt}

당신은 MACHO-GPT v3.4-mini입니다. Samsung C&T Logistics의 HVDC 프로젝트를 담당하며, 
상기 역할 정의에 따라 전문적이고 정확한 답변을 제공해야 합니다.
항상 신뢰도 ≥0.90을 유지하고, 필요시 적절한 /cmd 명령어를 추천하세요.
"""
    
    return enhanced_prompt.strip()

# 편의 함수들
ROLE_DESCRIPTION = get_role_description()
"""전역 역할 설명 상수"""

def create_system_message(content: str = "") -> Dict[str, str]:
    """
    시스템 메시지 딕셔너리 생성
    
    Args:
        content: 추가 시스템 프롬프트 내용
        
    Returns:
        dict: OpenAI 형식의 시스템 메시지
    """
    return {
        "role": "system",
        "content": get_enhanced_system_prompt(content)
    }
```

### Step 2: AI Summarizer 통합

```python
# macho_gpt/core/logi_ai_summarizer_241219.py (업데이트)
from .role_config import create_system_message, get_enhanced_system_prompt

class LogiAISummarizer:
    def _get_system_prompt(self) -> str:
        """역할 정의가 포함된 시스템 프롬프트 생성"""
        base_prompt = """
        WhatsApp 대화를 분석하여 다음을 추출하세요:
        1. 핵심 요약 (3-5줄)
        2. 실행 가능한 태스크 목록
        3. 긴급 사항
        4. 중요 사항
        
        물류, HVDC 프로젝트, 업무 관련 내용을 우선적으로 분석하세요.
        """
        
        return get_enhanced_system_prompt(base_prompt)
```

---

## 6️⃣ 테스트 가이드

### 단위 테스트 예제

```python
# tests/test_role_injection.py
import pytest
from macho_gpt.core.role_config import (
    get_role_description,
    get_enhanced_system_prompt,
    create_system_message
)

def test_role_description_contains_key_terms():
    """역할 설명에 핵심 키워드가 포함되어 있는지 테스트"""
    role_desc = get_role_description()
    
    assert "Samsung C&T" in role_desc
    assert "HVDC" in role_desc
    assert "Logistics" in role_desc
    assert "Confidence" in role_desc

def test_enhanced_system_prompt_structure():
    """향상된 시스템 프롬프트 구조 테스트"""
    prompt = get_enhanced_system_prompt("Test prompt")
    
    assert "Samsung C&T" in prompt
    assert "MACHO-GPT v3.4-mini" in prompt
    assert "Test prompt" in prompt

def test_system_message_format():
    """시스템 메시지 형식 테스트"""
    message = create_system_message("Test content")
    
    assert message["role"] == "system"
    assert "Samsung C&T" in message["content"]
    assert "Test content" in message["content"]
```

---

## 7️⃣ 환경별 설정

### 개발 환경
```bash
# .env.development
MACHO_GPT_ROLE_DESCRIPTION="🧪 [DEV] Samsung C&T Logistics - HVDC Project Developer"
```

### 프로덕션 환경
```bash
# .env.production  
MACHO_GPT_ROLE_DESCRIPTION="🛠️ Samsung C&T Logistics – Middle-East HVDC Mega-Project Copilot"
```

---

## 8️⃣ CI/CD 통합

### GitHub Actions 예제

```yaml
# .github/workflows/deploy.yml
name: Deploy MACHO-GPT
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Test Role Configuration
        run: |
          python -m pytest tests/test_role_injection.py -v
        env:
          MACHO_GPT_ROLE_DESCRIPTION: ${{ secrets.PROD_ROLE_DESCRIPTION }}
```

---

## TL;DR

`ROLE_DESCRIPTION` 문자열 하나로 **내 업무 정의**를 중앙에서 관리하고, 모든 GPT 프롬프트 앞단에 삽입하면 **일관된 컨텍스트**를 확보할 수 있다. 필요에 따라 **Python 모듈·환경변수·YAML** 중 한 가지만 선택하여 프로젝트에 통합하면 된다.

### 🚀 빠른 시작

1. **역할 설정**: `macho_gpt/core/role_config.py` 생성
2. **AI 통합**: 기존 summarizer에 role injection 추가
3. **테스트**: `tests/test_role_injection.py` 실행
4. **배포**: 환경변수로 프로덕션 역할 설정

### 🔧 추천 명령어

- `/role_config setup` [역할 설정 초기화]
- `/test_role_injection` [역할 주입 테스트]
- `/update_system_prompts` [모든 AI 모듈에 역할 적용]

---

**📋 이 가이드를 통해 MACHO-GPT v3.4-mini의 모든 AI 응답이 Samsung C&T Logistics HVDC 프로젝트 컨텍스트에 최적화됩니다.** 