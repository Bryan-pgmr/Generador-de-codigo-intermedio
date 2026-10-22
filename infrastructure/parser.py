from typing import List

from domain.models import Token, TranslationResult
from infrastructure.generators import (
    TemporaryGenerator,
    LabelGenerator
)


class ThreeAddressParser:

    def translate(
        self,
        tokens: List[Token]
    ) -> TranslationResult:

        parser = Parser(tokens)
        return parser.parse()


class Parser:

    def __init__(
        self,
        tokens: List[Token]
    ):

        self.tokens = tokens
        self.position = 0

        self.code = []
        self.explanations = []

        self.temp_generator = TemporaryGenerator()
        self.label_generator = LabelGenerator()

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
        self.position += 1
        return token

    def check(self, token_type, value=None):
        token = self.current()

        if token.type != token_type:
            return False

        if value is not None and token.value != value:
            return False

        return True

    def match(self, token_type, value=None):
        if self.check(token_type, value):
            return self.advance()

        return None

    def expect(self, token_type, value=None):
        token = self.current()

        if not self.check(token_type, value):

            expected = (
                value
                if value is not None
                else token_type
            )

            raise SyntaxError(
                f"Se esperaba '{expected}' "
                f"pero se encontró '{token.value}'"
            )

        return self.advance()

    def emit(self, instruction):
        self.code.append(instruction)

    def explain(self, text):
        self.explanations.append(text)

    def parse(self):
        while not self.check("EOF"):
            self.statement()

        return TranslationResult(
            code=self.code,
            explanations=self.explanations
        )

    def statement(self):
        if self.check("IF"):
            self.if_statement()

        elif self.check("WHILE"):
            self.while_statement()

        elif self.check("LBRACE"):
            self.block()

        elif self.check("ID"):
            self.assignment()

        else:
            raise SyntaxError(
                "Instrucción no reconocida "
                f"cerca de '{self.current().value}'"
            )

    def block(self):
        self.expect("LBRACE")

        while (
            not self.check("RBRACE")
            and not self.check("EOF")
        ):
            self.statement()

        self.expect("RBRACE")

    def assignment(self):
        variable = self.expect("ID").value
        self.expect("OP", "=")

        result = self.expression()

        self.emit(
            f"{variable} = {result}"
        )

        self.explain(
            f"El resultado almacenado en {result} "
            f"se asigna a {variable}."
        )

        self.match("SEMICOLON")

    def if_statement(self):
        self.expect("IF")
        self.expect("OP", "(")

        condition = self.expression()

        self.expect("OP", ")")

        false_label = self.label_generator.new()
        end_label = self.label_generator.new()

        self.emit(
            f"ifFalse {condition} goto {false_label}"
        )

        self.statement()

        if self.match("ELSE"):

            self.emit(
                f"goto {end_label}"
            )

            self.emit(
                f"{false_label}:"
            )

            self.statement()

            self.emit(
                f"{end_label}:"
            )

            self.explain(
                f"{false_label} representa la rama falsa del if."
            )

            self.explain(
                f"{end_label} representa el final del if/else."
            )

        else:
            self.emit(
                f"{false_label}:"
            )

            self.explain(
                f"{false_label} representa la salida del if."
            )

    def while_statement(self):
        self.expect("WHILE")

        start_label = self.label_generator.new()
        end_label = self.label_generator.new()

        self.emit(
            f"{start_label}:"
        )

        self.expect("OP", "(")

        condition = self.expression()

        self.expect("OP", ")")

        self.emit(
            f"ifFalse {condition} goto {end_label}"
        )

        self.statement()

        self.emit(
            f"goto {start_label}"
        )

        self.emit(
            f"{end_label}:"
        )

        self.explain(
            f"{start_label} marca el inicio del ciclo."
        )

        self.explain(
            f"{end_label} marca la salida del ciclo."
        )

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        left = self.logical_and()

        while self.check("OP", "||"):
            operator = self.advance().value
            right = self.logical_and()

            left = self.generate_operation(
                left,
                operator,
                right
            )

        return left

    def logical_and(self):
        left = self.equality()

        while self.check("OP", "&&"):
            operator = self.advance().value
            right = self.equality()

            left = self.generate_operation(
                left,
                operator,
                right
            )

        return left

    def equality(self):
        left = self.relational()

        while (
            self.check("OP", "==")
            or self.check("OP", "!=")
        ):
            operator = self.advance().value
            right = self.relational()

            left = self.generate_operation(
                left,
                operator,
                right
            )

        return left

    def relational(self):
        left = self.addition()

        while (
            self.check("OP", "<")
            or self.check("OP", ">")
            or self.check("OP", "<=")
            or self.check("OP", ">=")
        ):
            operator = self.advance().value
            right = self.addition()

            left = self.generate_operation(
                left,
                operator,
                right
            )

        return left

    def addition(self):
        left = self.multiplication()

        while (
            self.check("OP", "+")
            or self.check("OP", "-")
        ):
            operator = self.advance().value
            right = self.multiplication()

            left = self.generate_operation(
                left,
                operator,
                right
            )

        return left

    def multiplication(self):
        left = self.unary()

        while (
            self.check("OP", "*")
            or self.check("OP", "/")
            or self.check("OP", "%")
        ):
            operator = self.advance().value
            right = self.unary()

            left = self.generate_operation(
                left,
                operator,
                right
            )

        return left

    def unary(self):
        if (
            self.check("OP", "!")
            or self.check("OP", "-")
        ):
            operator = self.advance().value
            operand = self.unary()

            temp = self.temp_generator.new()

            self.emit(
                f"{temp} = {operator}{operand}"
            )

            self.explain(
                f"{temp} almacena el resultado de "
                f"{operator}{operand}."
            )

            return temp

        return self.primary()

    def primary(self):
        if self.check("NUMBER"):
            return self.advance().value

        if self.check("ID"):
            return self.advance().value

        if self.check("TRUE"):
            self.advance()
            return "true"

        if self.check("FALSE"):
            self.advance()
            return "false"

        if self.match("OP", "("):
            result = self.expression()
            self.expect("OP", ")")
            return result

        raise SyntaxError(
            "Expresión no válida "
            f"cerca de '{self.current().value}'"
        )

    def generate_operation(
        self,
        left,
        operator,
        right
    ):

        temp = self.temp_generator.new()

        self.emit(
            f"{temp} = {left} {operator} {right}"
        )

        self.explain(
            f"{temp} guarda temporalmente el resultado "
            f"de {left} {operator} {right}."
        )

        return temp
