# 🎮 Pong Arcade OOP

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Arcade Version](https://img.shields.io/badge/arcade-3.3.3-orange.svg)](https://api.arcade.academy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Game State](https://img.shields.io/badge/status-active_MVP-success.svg)](#)

Una versión educativa, moderna y altamente modular del clásico juego arcade **Pong**. Desarrollado en Python bajo el enfoque de **Programación Orientada a Objetos (OOP)** y potenciado por la biblioteca gráfica **Arcade v3**. Este proyecto ha sido diseñado específicamente para estudiantes de desarrollo de software y videojuegos, ilustrando cómo estructurar entidades físicas de juego, resolver problemas de rendimiento e independencia de la tasa de refresco (FPS) y controlar la concurrencia de periféricos en tiempo de ejecución.

---

## 📌 Tabla de Contenidos

- [🎮 Pong Arcade OOP](#-pong-arcade-oop)
  - [📌 Tabla de Contenidos](#-tabla-de-contenidos)
  - [⚡ Características Principales](#-características principales)
  - [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
  - [📋 Requisitos Previos](#-requisitos-previos)
  - [⚙️ Guía de Instalación (Paso a Paso)](#️-guía-de-instalación-paso-a-paso)
  - [🚀 Ejecución y Uso](#-ejecución-y-uso)
    - [🎮 Controles del Juego](#-controles-del-juego)
  - [📂 Estructura del Proyecto](#-estructura-del-proyecto)
  - [🤝 Contribución y Licencia](#-contribución-y-licencia)

---

## ⚡ Características Principales

*   **👥 Multijugador Local Suave**: Soporte inmediato para dos jugadores compartiendo el mismo teclado físico, ideal para sesiones rápidas 1v1.
*   **⌨️ Input Buffer Anti-Interferencias**: Implementación de almacenamiento de estados de teclas en conjunto (`set`) para prevenir que la pulsación o liberación de teclas de un jugador interrumpa o bloquee las acciones del otro.
*   **⏱️ FPS Independence (Delta Time Scaling)**: Todo el sistema de movimiento físico está sincronizado con la delta de tiempo real de ejecución (`dt * 60`), garantizando que la velocidad del juego sea idéntica tanto en pantallas tradicionales de 60Hz como de 144Hz o superiores.
*   **📐 Colisiones AABB Precisas**: Algoritmo de intersección de cajas alineadas en el espacio (Axis-Aligned Bounding Box) con vectores absolutos unidireccionales para evitar el atasco geométrico de la pelota dentro de las paletas.
*   **🗃️ Arquitectura Modular Limpia**: Código estructurado bajo el paradigma OOP clásico, segregando la configuración inmutable, los modelos lógicos/físicos y el ciclo de vida de la ventana de renderizado OpenGL.

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología / Librería | Versión | Rol en el Proyecto |
| :--- | :--- | :--- | :--- |
| **Lenguaje Core** | [Python](https://www.python.org/) | `3.10+` | Lenguaje de desarrollo principal con anotaciones de tipo estáticas. |
| **Motor Gráfico** | [Arcade](https://api.arcade.academy/) | `3.3.3` | Framework 2D basado en OpenGL para el renderizado acelerado por hardware y gestión de la ventana. |
| **Multimedia y Ventanas** | [Pyglet](https://pyglet.org/) | `2.1.14` | Wrapper OpenGL subyacente para el manejo nativo del teclado y del bucle de eventos. |
| **Contenedores de Datos** | Dataclasses | Standard | Modelado de configuraciones (`GameConfig`) e información volátil de puntuación (`Score`). |

---

## 📋 Requisitos Previos

Antes de configurar y ejecutar este videojuego localmente, asegúrate de contar con los siguientes elementos instalados en tu sistema:

1.  **Python 3.10 o superior**: Puedes verificar tu versión actual de Python ejecutando:
    ```bash
    python --version
    ```
2.  **Git (Control de versiones)**: Para clonar el repositorio de forma rápida:
    ```bash
    git --version
    ```

---

## ⚙️ Guía de Instalación (Paso a Paso)

Sigue estos pasos en tu terminal para compilar el entorno y las dependencias locales del juego:

1.  **Clona el repositorio:**
    ```bash
    git clone [URL_DEL_REPOSITORIO]
    ```
2.  **Accede al directorio del proyecto:**
    ```bash
    cd Pong_Arcade
    ```
3.  **Crea un entorno virtual de Python aislado:**
    *   *En Windows (PowerShell/CMD):*
        ```bash
        python -m venv .venv
        ```
    *   *En macOS/Linux:*
        ```bash
        python3 -m venv .venv
        ```
4.  **Activa el entorno virtual:**
    *   *En Windows (PowerShell):*
        ```bash
        .venv\Scripts\Activate.ps1
        ```
    *   *En Windows (CMD):*
        ```bash
        .venv\Scripts\activate.bat
        ```
    *   *En macOS/Linux:*
        ```bash
        source .venv/bin/activate
        ```
5.  **Instala las dependencias necesarias:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Ejecución y Uso

Una vez que el entorno virtual esté activo y las dependencias hayan sido instaladas con éxito, puedes lanzar el juego con el siguiente comando:

```bash
python src/main.py
```

### 🎮 Controles del Juego

El juego cuenta con un esquema de control simétrico para dos jugadores locales en el mismo teclado:

*   **Paleta Izquierda (Jugador 1):**
    *   `W` ➡️ Mover paleta hacia **arriba**
    *   `S` ➡️ Mover paleta hacia **abajo**
*   **Paleta Derecha (Jugador 2):**
    *   `↑` (Flecha arriba) ➡️ Mover paleta hacia **arriba**
    *   `↓` (Flecha abajo) ➡️ Mover paleta hacia **abajo**

---

## 📂 Estructura del Proyecto

A continuación se detalla la distribución de archivos del proyecto para comprender dónde reside cada capa de lógica:

```text
Pong_Arcade/
├── .venv/                     # Entorno virtual aislado con las dependencias instaladas.
├── requirements.txt           # Definición de dependencias e inmutabilidad de paquetes.
├── README.md                  # Guía de documentación del proyecto (este archivo).
├── project_context.md         # Fichero maestro de arquitectura y auditoría técnica.
└── src/                       # Carpeta raíz del código fuente.
    ├── __init__.py            # Inicializador para estructurar src como paquete de Python.
    ├── config.py              # Clase 'GameConfig': parámetros físicos, colores y dimensiones.
    ├── main.py                # Entrada principal del programa, bucle del juego y colisiones.
    └── models.py              # Entidades del juego ('Paddle', 'Ball', 'Score') y su comportamiento.
```

---

## 🤝 Contribución y Licencia

### Contribución
¡Las contribuciones son siempre bienvenidas para hacer de este un proyecto educativo aún mejor! Si deseas proponer cambios, añadir efectos de sonido, físicas avanzadas con `pymunk` o mejorar los gráficos:
1. Haz un fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-mejora`).
3. Envía un Pull Request detallando tus cambios.

### Licencia
Este proyecto se encuentra bajo la licencia **MIT** de código abierto. Consulta el archivo `LICENSE` (o un placeholder legal equivalente) para obtener más detalles.

---
*Desarrollado con fines educativos. ¡Esperamos que sirva para inspirar y enseñar a futuros desarrolladores de videojuegos! 🚀*
