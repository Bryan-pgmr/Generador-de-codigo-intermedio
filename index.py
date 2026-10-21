from infrastructure.lexer import RegexLexer
from infrastructure.parser import ThreeAddressParser
from application.generate_intermediate_code import GenerateIntermediateCode
from presentation.main_window import MainWindow


def main():
    lexer = RegexLexer()
    parser = ThreeAddressParser()

    generate_code = GenerateIntermediateCode(
        lexer=lexer,
        translator=parser
    )

    app = MainWindow(generate_code)
    app.run()


if __name__ == "__main__":
    main()
