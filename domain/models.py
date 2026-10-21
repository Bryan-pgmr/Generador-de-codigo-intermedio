from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    value: str


@dataclass
class TranslationResult:
    code: List[str]
    explanations: List[str]
