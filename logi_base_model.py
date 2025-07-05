from __future__ import annotations

from pydantic import BaseModel


class LogiBaseModel(BaseModel):
    """기본 로지스틱스 모델 / Base logistics model"""

    class Config:
        arbitrary_types_allowed = True 