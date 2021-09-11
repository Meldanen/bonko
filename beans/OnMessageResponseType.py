from dataclasses import dataclass

from enums.SentimentEnum import SentimentEnum


@dataclass
class OnMessageResponseType:
    id: int
    value: str
    sentiment: SentimentEnum
