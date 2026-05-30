# src/config.py
"""
Este módulo contiene la configuración global del juego.
Centralizar los parámetros aquí (Single Source of Truth) permite cambiar
el comportamiento del juego (como la velocidad o el tamaño) en un solo lugar
sin modificar el código de los modelos ni de la ventana.
"""

from dataclasses import dataclass

# Usamos @dataclass para crear una clase contenedora de datos de forma rápida.
# Esto nos evita tener que escribir un método __init__ manualmente.
@dataclass
class GameConfig:
    # Dimensiones de la pantalla de juego (en píxeles)
    width: int = 800
    height: int = 600
    
    # Título que se mostrará en la barra superior de la ventana
    title: str = "Pong Arcade OOP"
    
    # Color de fondo de la pantalla en formato RGB (Rojo, Verde, Azul). (0,0,0) es Negro.
    background_color: tuple[int, int, int] = (0, 0, 0)
    
    # Dimensiones físicas de las paletas de los jugadores (ancho y alto en píxeles)
    paddle_width: float = 10
    paddle_height: float = 80
    
    # Velocidad de movimiento vertical de las paletas por frame (factor base)
    paddle_speed: float = 8
    
    # Tamaño de la pelota (radio en píxeles)
    ball_size: float = 10
    
    # Velocidad inicial de la pelota tanto en el eje X (horizontal) como en el eje Y (vertical)
    ball_speed: float = 5