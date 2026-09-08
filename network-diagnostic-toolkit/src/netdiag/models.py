from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class CheckResult:
    name: str
    status: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class Diagnosis:
    code: str
    severity: str
    title: str
    explanation: str
    recommendations: list[str]
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
