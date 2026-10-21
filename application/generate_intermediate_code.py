from domain.ports import LexerPort, TranslatorPort
from domain.models import TranslationResult


class GenerateIntermediateCode:

    def __init__(
        self,
        lexer: LexerPort,
        translator: TranslatorPort
    ):
        self.lexer = lexer
        self.translator = translator

    def execute(self, source: str) -> TranslationResult:
        if not source.strip():
            raise ValueError("El código fuente está vacío.")

        tokens = self.lexer.tokenize(source)
        return self.translator.translate(tokens)
