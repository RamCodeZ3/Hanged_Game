from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
import functions as func

words = func.generate_words("words.json")


class Menu(Screen):
    def __init__(self):
        super().__init__()
        self.selected_word = None
        self.category = None
        self.signs = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Bienvenido al ahorcado", id="welcome_message"),
            Button("Comenzar", id="start"),
            Button("Salir", id="exit"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "start":
            if not words:
                welcome_message = self.query_one("#welcome_message", Static)
                welcome_message.update(
                    """No se encontraron palabras.
                    Verifica el archivo words.json"""
                )

            self.app.push_screen("game")

        elif event.button.id == "exit":
            self.app.exit()
