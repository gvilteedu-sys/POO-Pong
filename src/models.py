from __future__ import unicode_literals
from dataclasses import dataclass
from typing import Literal

import arcade

try:
    from .config import GamgeConfig
except ImportError:
    from config import GamgeConfig

@dataclass
class Score:
    """Class to keep track of the score."""
    left: int = 0
    right: int = 0

class Paddle(arcade.Sprite):
    """Class representing a paddle in the game."""
    def __init__(self, x: float, y: float, config: GamgeConfig)-> None:
        super().__init__()
        self.width = config.paddle_width
        self.height = config.paddle_height
        self.center_x = x
        self.center_y = y
        self.speed = config.paddle_speed
        self.color = arcade.color.WHITE
        self.change_y = 0

    def update(self, dt: float, config: GameConfig) -> None:
        self.center_y += self.change_y * dt * 60  # ajustar por FPS
        # limitar dentro de la pantalla
        half_height = self.height / 2
        self.center_y = max(half_height,
                            min(config.height - half_height, self.center_y))
    def draw(self) -> None:
        # convertir centro + ancho/alto a (x, y, width, height)
        # x, y son la esquina inferior izquierda en draw_xywh_rectangle_filled
        x = self.center_x - self.width / 2
        y = self.center_y - self.height / 2
        arcade.draw_lbwh_rectangle_filled(x, y, self.width, self.height, self.color)




class Ball(arcade.Sprite):
    def __init__(self, config: GameConfig) -> None:
        super().__init__()
        self.radius = config.ball_size  # antes: self.size
        self.center_x = config.width / 2
        self.center_y = config.height / 2
        self.color = arcade.color.WHITE
        self.dx = config.ball_speed
        self.dy = config.ball_speed

    def reset(self, direction: Literal["left", "right"], config: GameConfig) -> None:
        self.center_x = config.width / 2
        self.center_y = config.height / 2
        self.dx = config.ball_speed if direction == "right" else -config.ball_speed
        self.dy = config.ball_speed


    def update(self, dt: float, config: GameConfig) -> None:
        self.center_x += self.dx * dt * 60
        self.center_y += self.dy * dt * 60

        # rebote con bordes superior/inferior
        if self.center_y <= self.radius:
            self.dy = abs(self.dy)
        elif self.center_y >= config.height - self.radius:
            self.dy = -abs(self.dy)

    def draw(self) -> None:
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)
