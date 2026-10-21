# Generador de Código Intermedio

Proyecto de Lenguajes y Autómatas II para generar código intermedio de tres direcciones a partir de un lenguaje prototipo.

## Estructura

- `index.py`: punto de entrada.
- `domain/`: modelos e interfaces.
- `application/`: caso de uso principal.
- `infrastructure/`: lexer, parser y generadores de temporales/etiquetas.
- `presentation/`: interfaz gráfica con Tkinter.

## Ejecutar

Desde la carpeta raíz:

```bash
python index.py
```

## Ejemplo válido

```c
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
```
