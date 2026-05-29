# src/main.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

import arcade

try:
    from .config import GameConfig
    from .models import Paddle, Ball, Score
except ImportError:
    from config import GameConfig
    from models import Paddle, Ball, Score

ASSETS_DIR = Path(__file__).parent / "assets"  # por si luego agregas sonidos/imágenes

class GameWindows(arcade.Windows):
    def __init__(self, config: Optional[GameConfig] = None) -> None:
        self.game_config = config or GameConfig()
        super().__init__(self.game_config.width, self.game_config.height, self.game_config.title)
        self.background_color = arcade.color.BLACK

        # Teclas presionadas para evitar interferencia en controles
        self.pressed_keys: set[int] = set()

        # Entidades del juego
        self.left_paddle: Paddle
        self.right_paddle: Paddle
        self.ball: Ball
        self.score = Score()

        self.setup()

    def setup(self) -> None:
        margin = 40
        self.left_paddle = Paddle(
            x=margin,
            y=self.game_config.height / 2,
            config=self.game_config,
        )
        self.right_paddle = Paddle(
            x=self.game_config.width - margin,
            y=self.game_config.height / 2,
            config=self.game_config,
        )
        self.ball = Ball(self.game_config)
        self.ball.reset("right", self.game_config)


    def on_draw(self) -> None:
        self.clear()

        # Dibujar paletas y pelota
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.ball.draw()

        # Dibujar marcador
        score_text = f"{self.score.left} : {self.score.right}"
        arcade.draw_text(
            score_text,
            self.game_config.width / 2 - 30,
            self.game_config.height - 40,
            arcade.color.WHITE,
            20,
        )

    def on_update(self, delta_time: float) -> None:
        self.left_paddle.update(delta_time, self.game_config)
        self.right_paddle.update(delta_time, self.game_config)
        self.ball.update(delta_time, self.game_config)

        # Colisiones con paletas (muy simple)
        if (abs(self.ball.center_x - self.left_paddle.center_x)
                <= (self.left_paddle.width / 2 + self.ball.radius)
            and abs(self.ball.center_y - self.left_paddle.center_y)
                <= (self.left_paddle.height / 2 + self.ball.radius)):
            self.ball.dx = abs(self.ball.dx)

        if (abs(self.ball.center_x - self.right_paddle.center_x)
                <= (self.right_paddle.width / 2 + self.ball.radius)
            and abs(self.ball.center_y - self.right_paddle.center_y)
                <= (self.right_paddle.height / 2 + self.ball.radius)):
            self.ball.dx = -abs(self.ball.dx)

        # Detectar punto
        if self.ball.center_x < 0:
            self.score.right += 1
            self.ball.reset("right", self.game_config)
        elif self.ball.center_x > self.game_config.width:
            self.score.left += 1
            self.ball.reset("left", self.game_config)

    def on_key_press(self, key: int, modifiers: int) -> None:
        self.pressed_keys.add(key)
        self.update_paddle_velocities()

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        self.update_paddle_velocities()

    def update_paddle_velocities(self) -> None:
        # Paleta izquierda (W sube, S baja)
        if arcade.key.W in self.pressed_keys and arcade.key.S not in self.pressed_keys:
            self.left_paddle.change_y = self.left_paddle.speed
        elif arcade.key.S in self.pressed_keys and arcade.key.W not in self.pressed_keys:
            self.left_paddle.change_y = -self.left_paddle.speed
        else:
            self.left_paddle.change_y = 0

        # Paleta derecha (UP sube, DOWN baja)
        if arcade.key.UP in self.pressed_keys and arcade.key.DOWN not in self.pressed_keys:
            self.right_paddle.change_y = self.right_paddle.speed
        elif arcade.key.DOWN in self.pressed_keys and arcade.key.UP not in self.pressed_keys:
            self.right_paddle.change_y = -self.right_paddle.speed
        else:
            self.right_paddle.change_y = 0


def main() -> None:
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()