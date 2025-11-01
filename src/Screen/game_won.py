from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
import utils.fuction as func


class Game_won(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static('Felicitaciones, lograste adivinar todas las palabras'),
            Button("Reintentar", id="retry"),
            Button("Volver al inicio", id="restart"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        try:

            new_category, new_word = func.Select_Words()
            if not new_word or not new_category:
                raise ValueError(
                    "No se pudo seleccionar una palabra o categoría válida"
                )

            if event.button.id == "restart":
                while len(self.app.screen_stack) > 1:
                    self.app.pop_screen()
                self.app.push_screen("menu")

            elif event.button.id == "retry":
                while len(self.app.screen_stack) > 1:
                    self.app.pop_screen()

                self.app.push_screen("game")
        except Exception as e:
            self.notify(
                f"Error al intentar reiniciar el juego: {str(e)}",
                severity="error"
            )

    def on_mount(self) -> None:
        self.add_class("screen_game_won")
