from dataclasses import dataclass


@dataclass
class JudgeBonkoResponse:
    id: int
    value: str
    file: bool
