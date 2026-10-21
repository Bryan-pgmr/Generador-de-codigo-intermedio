import re
from typing import List

from domain.models import Token


class RegexLexer:

    TOKEN_RULES = [
        ("COMMENT", r"//[^\n]*"),
        ("NUMBER", r"\d+(?:\.\d+)?"),
        ("IF", r"\bif\b"),
        ("ELSE", r"\belse\b"),
        ("WHILE", r"\bwhile\b"),
        ("TRUE", r"\btrue\b"),
        ("FALSE", r"\bfalse\b"),
        ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("OP", r"==|!=|<=|>=|&&|\|\||[+\-*/%=<>!()]"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("SEMICOLON", r";"),
        ("SKIP", r"[ \t\r\n]+"),
        ("MISMATCH", r"."),
    ]

    def __init__(self):
        self.master_regex = "|".join(
            f"(?P<{name}>{pattern})"
            for name, pattern in self.TOKEN_RULES
        )

    def tokenize(self, source: str) -> List[Token]:
        tokens = []

        for match in re.finditer(self.master_regex, source):
            token_type = match.lastgroup
            value = match.group()

            if token_type in ("SKIP", "COMMENT"):
                continue

            if token_type == "MISMATCH":
                raise SyntaxError(
                    f"Símbolo no reconocido: {value}"
                )

            tokens.append(Token(token_type, value))

        tokens.append(Token("EOF", ""))
        return tokens
