from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
import functions as func


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
            words = func.generate_words("words.json")
            if not words:
                raise ValueError(
                    "No se encontraron palabras en el archivo words.json"
                )

            new_category, new_word = func.Select_Words(words)
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

                self.app.push_screen(
                    "game",
                    (new_word,
                     new_category,
                     ["❌"] * len(new_word), 0)
                )
        except Exception as e:
            self.notify(
                f"Error al intentar reiniciar el juego: {str(e)}",
                severity="error"
            )

    def on_mount(self) -> None:
        self.add_class("screen_game_won")
