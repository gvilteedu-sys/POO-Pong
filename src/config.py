from dataclasses import dataclass

@dataclass
class GamgeConfig:
    """Configuration for the game."""
    width: int = 800
    height: int = 600
    title: str = "  Pong Game"
    background_color: tuple[int, int, int] = (0, 0, 0) 
    paddle_width: float = 10
    paddle_height: float = 100
    paddle_speed: float = 8
    ball_speed: float = 5
    ball_size: int = 10