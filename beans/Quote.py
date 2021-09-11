from dataclasses import dataclass


@dataclass
class Quote:
    id: int
    quote: str
    reaction: str
    file: bool
