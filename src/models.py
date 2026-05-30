# src/models.py
"""
Este módulo contiene los "Modelos" del juego.
Define cómo representamos y cómo se comportan de forma individual las entidades
del juego: las paletas (Paddle), la pelota (Ball) y el marcador (Score).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import arcade

# Bloque defensivo de importación: permite ejecutar este archivo de manera
# directa o como parte de un módulo empaquetado (con el punto relativo).
try:
    from .config import GameConfig
except ImportError:
    from config import GameConfig


@dataclass
class Score:
    """
    Clase contenedora para las puntuaciones.
    Es un modelo de datos simple que guarda cuántos puntos tiene cada jugador.
    """
    left: int = 0
    right: int = 0


class Paddle(arcade.Sprite):
    """
    Clase que representa a una Paleta (Jugador).
    Hereda de 'arcade.Sprite' para integrarse con el motor gráfico de Arcade,
    pero la dibujamos de forma manual como un rectángulo plano sin textura.
    """
    def __init__(self, x: float, y: float, config: GameConfig) -> None:
        # Llamamos al constructor de la clase padre (arcade.Sprite)
        super().__init__()
        
        # Asignamos las dimensiones y posición inicial basándonos en la configuración inyectada
        self.width = config.paddle_width
        self.height = config.paddle_height
        self.center_x = x
        self.center_y = y
        self.color = arcade.color.WHITE
        
        # Guardamos la velocidad máxima de desplazamiento que puede alcanzar la paleta
        self.speed = config.paddle_speed
        
        # 'change_y' es una propiedad heredada de arcade.Sprite.
        # Indica la velocidad vertical actual de la paleta.
        # 0 = quieta, positivo = subiendo, negativo = bajando.
        self.change_y = 0

    def update(self, dt: float, config: GameConfig) -> None:
        """
        Actualiza el estado de la paleta en cada frame.
        """
        # Desplazamiento basado en 'dt' (Delta Time):
        # Multiplicar por 'dt * 60' normaliza la velocidad para que el juego corra
        # a la misma velocidad en monitores de 60Hz, 144Hz o superiores.
        self.center_y += self.change_y * dt * 60
        
        # REGLE DE DOMINIO: Limitar (Clamping) la paleta dentro de los límites de la pantalla.
        # Evita que la mitad superior o inferior de la paleta sobresalga de la ventana.
        half_height = self.height / 2
        
        # La función 'min' asegura que la paleta no suba más allá del borde superior (altura - mitad de paleta)
        # La función 'max' asegura que la paleta no baje más allá del borde inferior (mitad de paleta)
        self.center_y = max(half_height,
                            min(config.height - half_height, self.center_y))

    def draw(self) -> None:
        """
        Dibuja la paleta en la pantalla.
        """
        # La API 'arcade.draw_lbwh_rectangle_filled' requiere las coordenadas de la esquina
        # inferior izquierda (Left, Bottom) en lugar del centro (Center X, Center Y).
        # Hacemos la conversión matemática restando la mitad del ancho y de la altura.
        x = self.center_x - self.width / 2
        y = self.center_y - self.height / 2
        
        # Pintamos el rectángulo relleno con el color blanco de la paleta
        arcade.draw_lbwh_rectangle_filled(x, y, self.width, self.height, self.color)


class Ball(arcade.Sprite):
    """
    Clase que representa a la Pelota.
    Hereda de 'arcade.Sprite' y se encarga del movimiento de la bola,
    los rebotes en la parte superior e inferior, y su reposicionamiento (reset).
    """
    def __init__(self, config: GameConfig) -> None:
        super().__init__()
        
        # Usamos el tamaño definido en la configuración como el radio de nuestra circunferencia
        self.radius = config.ball_size
        
        # Posicionamos inicialmente la pelota en el centro exacto de la pantalla
        self.center_x = config.width / 2
        self.center_y = config.height / 2
        self.color = arcade.color.WHITE
        
        # 'dx' y 'dy' representan la velocidad de desplazamiento en los ejes X e Y por frame
        self.dx = config.ball_speed
        self.dy = config.ball_speed

    def reset(self, direction: Literal["left", "right"], config: GameConfig) -> None:
        """
        Reinicia la pelota al centro tras anotarse un punto,
        enviándola en dirección al jugador correspondiente para el saque.
        """
        self.center_x = config.width / 2
        self.center_y = config.height / 2
        
        # Si la dirección es hacia la derecha, 'dx' es positivo.
        # Si es hacia la izquierda, forzamos a que 'dx' sea negativo.
        self.dx = config.ball_speed if direction == "right" else -config.ball_speed
        
        # Restablecemos también la velocidad vertical hacia arriba por defecto
        self.dy = config.ball_speed

    def update(self, dt: float, config: GameConfig) -> None:
        """
        Actualiza la posición espacial de la pelota frame a frame.
        """
        # Desplazamos la pelota sumando la velocidad multiplicada por el Delta Time normalizado
        self.center_x += self.dx * dt * 60
        self.center_y += self.dy * dt * 60

        # REGLE DE DOMINIO: Rebote físico contra los bordes superior e inferior de la pantalla.
        # Si la pelota toca o intenta sobrepasar el suelo (y <= radio), forzamos a que su velocidad vertical (dy) sea positiva.
        if self.center_y <= self.radius:
            self.dy = abs(self.dy)  # Forzar dirección hacia arriba
            
        # Si toca o sobrepasa el techo (y >= altura_pantalla - radio), forzamos a que su velocidad vertical (dy) sea negativa.
        elif self.center_y >= config.height - self.radius:
            self.dy = -abs(self.dy)  # Forzar dirección hacia abajo

    def draw(self) -> None:
        """
        Dibuja la pelota como un círculo perfecto relleno.
        """
        # Dibujamos un círculo usando las coordenadas de su centro y su radio
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)