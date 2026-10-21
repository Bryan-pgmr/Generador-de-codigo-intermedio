from typing import Protocol, List
from domain.models import Token, TranslationResult


class LexerPort(Protocol):
    def tokenize(self, source: str) -> List[Token]:
        pass


class TranslatorPort(Protocol):
    def translate(self, tokens: List[Token]) -> TranslationResult:
        pass
