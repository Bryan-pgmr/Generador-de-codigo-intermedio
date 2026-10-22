# Descripción del código

Este proyecto consiste en un generador de código intermedio de tres direcciones desarrollado en Python para la materia de Lenguajes y Autómatas II.

El programa recibe fragmentos escritos en un lenguaje prototipo y realiza su análisis para generar una representación intermedia utilizando variables temporales y etiquetas. Actualmente puede procesar asignaciones, expresiones aritméticas, comparaciones, estructuras `if/else` y ciclos `while`.

La aplicación está organizada siguiendo principios de SOLID y Clean Architecture, separando el proyecto en distintas capas. La capa de dominio contiene los modelos e interfaces principales, la capa de aplicación controla el caso de uso de generación de código intermedio, la infraestructura se encarga del análisis léxico, sintáctico y de la generación de temporales y etiquetas, mientras que la capa de presentación contiene la interfaz gráfica.

El archivo `index.py` funciona como punto de entrada del programa y se encarga de conectar todas las capas y ejecutar la interfaz.

Esta organización permite que el código sea más fácil de mantener, modificar y ampliar, además de facilitar la incorporación de nuevas estructuras del lenguaje en versiones futuras.

# Generador de Código Intermedio

Proyecto de Lenguajes y Autómatas II para generar código intermedio de tres direcciones a partir de un lenguaje prototipo.

## Estructura

- `index.py`: punto de entrada.
- `domain/`: modelos e interfaces.
- `application/`: caso de uso principal.
- `infrastructure/`: lexer, parser y generadores de temporales/etiquetas.
- `presentation/`: interfaz gráfica con Tkinter.

## Instrucciones de Ejecución

Descargue el proyecto de GitHub mediente "Code" --> Download ZIP.

Descomprimir el proyecto a una carpeta de visual studio.

Tener python instalado en la computadora.

Abre una terminal dentro de la carpeta del proyecto.

Desde la carpeta raíz del proyecto ejecuta:

```bash
python index.py
```

En otro caso Ejecute el index.py desde el boton de ejecutar de visual studio.

## Ejemplo válido precargado

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
