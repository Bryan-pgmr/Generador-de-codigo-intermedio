import tkinter as tk
from tkinter import messagebox, scrolledtext


class MainWindow:

    def __init__(self, generate_code_use_case):
        self.generate_code = generate_code_use_case
        self.root = tk.Tk()

        self.configure_window()
        self.create_widgets()

    def configure_window(self):
        self.root.title(
            "Generador de Código Intermedio"
        )

        self.root.geometry(
            "1100x720"
        )

        self.root.minsize(
            900,
            600
        )

    def create_widgets(self):
        self.create_header()
        self.create_editor()
        self.create_buttons()
        self.create_results()

    def create_header(self):
        title = tk.Label(
            self.root,
            text="Generador de Código Intermedio",
            font=("Arial", 22, "bold")
        )

        title.pack(
            pady=(15, 3)
        )

        subtitle = tk.Label(
            self.root,
            text="Lenguajes y Autómatas II - Actividad A6",
            font=("Arial", 12)
        )

        subtitle.pack(
            pady=(0, 15)
        )

    def create_editor(self):
        frame = tk.Frame(
            self.root
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20
        )

        label = tk.Label(
            frame,
            text="Código del lenguaje prototipo:",
            font=("Arial", 11, "bold")
        )

        label.pack(
            anchor="w"
        )

        self.source_editor = scrolledtext.ScrolledText(
            frame,
            height=12,
            font=("Consolas", 11)
        )

        self.source_editor.pack(
            fill="both",
            expand=True,
            pady=5
        )

    def create_buttons(self):
        frame = tk.Frame(
            self.root
        )

        frame.pack(
            pady=10
        )

        generate_button = tk.Button(
            frame,
            text="Generar código intermedio",
            width=25,
            command=self.generate
        )

        generate_button.grid(
            row=0,
            column=0,
            padx=5
        )

        example_button = tk.Button(
            frame,
            text="Cargar ejemplo",
            width=18,
            command=self.load_example
        )

        example_button.grid(
            row=0,
            column=1,
            padx=5
        )

        clear_button = tk.Button(
            frame,
            text="Limpiar",
            width=15,
            command=self.clear
        )

        clear_button.grid(
            row=0,
            column=2,
            padx=5
        )

    def create_results(self):
        frame = tk.Frame(
            self.root
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.create_code_result(frame)
        self.create_explanation_result(frame)

    def create_code_result(self, parent):
        frame = tk.Frame(
            parent
        )

        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5)
        )

        label = tk.Label(
            frame,
            text="Código de tres direcciones:",
            font=("Arial", 11, "bold")
        )

        label.pack(
            anchor="w"
        )

        self.code_output = scrolledtext.ScrolledText(
            frame,
            height=15,
            font=("Consolas", 11)
        )

        self.code_output.pack(
            fill="both",
            expand=True
        )

    def create_explanation_result(self, parent):
        frame = tk.Frame(
            parent
        )

        frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(5, 0)
        )

        label = tk.Label(
            frame,
            text="Explicación de temporales y etiquetas:",
            font=("Arial", 11, "bold")
        )

        label.pack(
            anchor="w"
        )

        self.explanation_output = scrolledtext.ScrolledText(
            frame,
            height=15,
            font=("Arial", 10)
        )

        self.explanation_output.pack(
            fill="both",
            expand=True
        )

    def generate(self):
        source = self.source_editor.get(
            "1.0",
            tk.END
        )

        try:
            result = self.generate_code.execute(
                source
            )

            self.show_result(
                result
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error)
            )

    def show_result(self, result):
        self.code_output.delete(
            "1.0",
            tk.END
        )

        self.code_output.insert(
            tk.END,
            "\n".join(result.code)
        )

        self.explanation_output.delete(
            "1.0",
            tk.END
        )

        for explanation in result.explanations:
            self.explanation_output.insert(
                tk.END,
                "• " + explanation + "\n"
            )

    def load_example(self):
        source = """
x = 6 * (2 + 3) / 5 - 1;

a = 10;
b = 5;

if (a > b) {
    resultado = a + b * 2;
} else {
    resultado = a - b;
}

while (resultado < 50) {
    resultado = resultado + 1;
}
"""

        self.source_editor.delete(
            "1.0",
            tk.END
        )

        self.source_editor.insert(
            tk.END,
            source.strip()
        )

    def clear(self):
        self.source_editor.delete(
            "1.0",
            tk.END
        )

        self.code_output.delete(
            "1.0",
            tk.END
        )

        self.explanation_output.delete(
            "1.0",
            tk.END
        )

    def run(self):
        self.root.mainloop()
