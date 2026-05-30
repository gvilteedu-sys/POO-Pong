# src/main.py
"""
Este módulo es el punto de entrada principal del juego.
Define la ventana gráfica (GameWindow) que actúa como el "Controlador" principal,
coordinando la entrada de teclado, las colisiones, el puntaje y el dibujado.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import arcade

# Bloque defensivo de importación para garantizar que funcione tanto ejecutándolo
# directamente como importándolo como un módulo desde la carpeta raíz.
try:
    from .config import GameConfig
    from .models import Paddle, Ball, Score
except ImportError:
    from config import GameConfig
    from models import Paddle, Ball, Score


# Ruta para los recursos multimedia (imágenes, sonidos) que se deseen agregar en el futuro.
ASSETS_DIR = Path(__file__).parent / "assets"


class GameWindow(arcade.Window):
    """
    Controlador y Ventana principal del juego. Hereda de 'arcade.Window'.
    Contiene el bucle del ciclo de vida del juego (Game Loop) y sus eventos.
    """
    def __init__(self, config: Optional[GameConfig] = None) -> None:
        # Cargamos la configuración por defecto si no se inyecta una
        self.game_config = config or GameConfig()
        
        # Llamamos al inicializador de la ventana de arcade (ancho, alto, título)
        super().__init__(self.game_config.width, self.game_config.height, self.game_config.title)
        
        # Color de fondo negro para la ventana
        self.background_color = arcade.color.BLACK

        # Usamos un conjunto (set) para registrar las teclas físicas que están actualmente presionadas.
        # Esto soluciona la interferencia al presionar varias teclas a la vez (multijugador en 1 teclado).
        self.pressed_keys: set[int] = set()

        # Declaramos los atributos para las paletas, pelota y marcador
        self.left_paddle: Paddle
        self.right_paddle: Paddle
        self.ball: Ball
        self.score = Score()

        # Inicializamos el estado del juego
        self.setup()

    def setup(self) -> None:
        """
        Configura o reinicia los elementos iniciales de la partida.
        """
        # Margen horizontal en píxeles para separar las paletas de los bordes izquierdo/derecho
        margin = 40
        
        # Instanciamos la paleta izquierda (Jugador 1)
        self.left_paddle = Paddle(
            x=margin,
            y=self.game_config.height / 2,
            config=self.game_config,
        )
        
        # Instanciamos la paleta derecha (Jugador 2)
        self.right_paddle = Paddle(
            x=self.game_config.width - margin,
            y=self.game_config.height / 2,
            config=self.game_config,
        )
        
        # Instanciamos la pelota y hacemos un saque inicial hacia la derecha
        self.ball = Ball(self.game_config)
        self.ball.reset("right", self.game_config)

    def on_draw(self) -> None:
        """
        Evento del Game Loop: Se encarga de pintar la pantalla en cada frame.
        Se ejecuta de forma automática aproximadamente 60 veces por segundo.
        """
        # Limpiamos la pantalla con el color de fondo establecido
        self.clear()

        # Invocamos el método de dibujo personalizado de cada elemento
        self.left_paddle.draw()
        self.right_paddle.draw()
        self.ball.draw()

        # Dibujamos el texto del marcador actual en el centro superior
        score_text = f"{self.score.left} : {self.score.right}"
        arcade.draw_text(
            text=score_text,
            x=self.game_config.width / 2 - 30, # Ajuste horizontal para centrar el texto
            y=self.game_config.height - 40,    # Posición vertical cerca del borde superior
            color=arcade.color.WHITE,
            font_size=20,
        )

    def on_update(self, delta_time: float) -> None:
        """
        Evento del Game Loop: Se encarga de las actualizaciones de física y lógica.
        'delta_time' es el tiempo real transcurrido (en fracciones de segundo) desde el frame anterior.
        """
        # Actualizamos la física de movimiento de cada objeto
        self.left_paddle.update(delta_time, self.game_config)
        self.right_paddle.update(delta_time, self.game_config)
        self.ball.update(delta_time, self.game_config)

        # REGLE DE DOMINIO: Detección de colisiones Pelota-Paletas (Fórmula AABB simplificada).
        # Comparamos la distancia absoluta entre los centros de la pelota y la paleta en ambos ejes.
        # Si la distancia es menor o igual a la suma de sus mitades más el radio de la bola, colisionan.

        # 1. Colisión con Paleta Izquierda:
        if (abs(self.ball.center_x - self.left_paddle.center_x)
                <= (self.left_paddle.width / 2 + self.ball.radius)
            and abs(self.ball.center_y - self.left_paddle.center_y)
                <= (self.left_paddle.height / 2 + self.ball.radius)):
            # Forzamos a que la velocidad horizontal sea positiva (va hacia la derecha).
            # Esto evita que la pelota se quede rebotando repetidamente "dentro" de la paleta.
            self.ball.dx = abs(self.ball.dx)

        # 2. Colisión con Paleta Derecha:
        if (abs(self.ball.center_x - self.right_paddle.center_x)
                <= (self.right_paddle.width / 2 + self.ball.radius)
            and abs(self.ball.center_y - self.right_paddle.center_y)
                <= (self.right_paddle.height / 2 + self.ball.radius)):
            # Forzamos a que la velocidad horizontal sea negativa (va hacia la izquierda).
            self.ball.dx = -abs(self.ball.dx)

        # REGLE DE DOMINIO: Detección de Anotación de Puntos.
        # Si la pelota supera el borde izquierdo (X < 0), punto para el jugador derecho.
        if self.ball.center_x < 0:
            self.score.right += 1
            # Se reinicia la pelota y saca hacia la derecha
            self.ball.reset("right", self.game_config)
            
        # Si la pelota supera el borde derecho (X > ancho de pantalla), punto para el jugador izquierdo.
        elif self.ball.center_x > self.game_config.width:
            self.score.left += 1
            # Se reinicia la pelota y saca hacia la izquierda
            self.ball.reset("left", self.game_config)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Evento del motor: Se ejecuta cuando el usuario presiona una tecla.
        """
        # Añadimos la tecla al conjunto de teclas presionadas actualmente
        self.pressed_keys.add(key)
        
        # Recalculamos las velocidades en base a las teclas presionadas
        self.update_paddle_velocities()

    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        Evento del motor: Se ejecuta cuando el usuario suelta una tecla.
        """
        # Removemos de forma segura la tecla del conjunto
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            
        # Recalculamos las velocidades en base a las teclas que aún queden presionadas
        self.update_paddle_velocities()

    def update_paddle_velocities(self) -> None:
        """
        Determina y asigna las velocidades verticales de las paletas.
        Esto permite un control suave e independiza el movimiento de cada jugador.
        """
        # --- Paleta Izquierda (Jugador 1: controla con 'W' para subir y 'S' para bajar) ---
        if arcade.key.W in self.pressed_keys and arcade.key.S not in self.pressed_keys:
            self.left_paddle.change_y = self.left_paddle.speed
        elif arcade.key.S in self.pressed_keys and arcade.key.W not in self.pressed_keys:
            self.left_paddle.change_y = -self.left_paddle.speed
        else:
            # Si ambas teclas están presionadas o ninguna de ellas, la paleta se detiene
            self.left_paddle.change_y = 0

        # --- Paleta Derecha (Jugador 2: controla con flecha ARRIBA para subir y flecha ABAJO para bajar) ---
        if arcade.key.UP in self.pressed_keys and arcade.key.DOWN not in self.pressed_keys:
            self.right_paddle.change_y = self.right_paddle.speed
        elif arcade.key.DOWN in self.pressed_keys and arcade.key.UP not in self.pressed_keys:
            self.right_paddle.change_y = -self.right_paddle.speed
        else:
            # Si ambas teclas están presionadas o ninguna de ellas, la paleta se detiene
            self.right_paddle.change_y = 0


def main() -> None:
    """
    Función de entrada inicial.
    Instancia la ventana del juego e inicia el bucle infinito de eventos de Arcade.
    """
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()