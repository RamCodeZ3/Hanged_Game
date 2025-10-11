from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
import utils.fuction as func
import os

PATH = "src/data/words.json"

words = func.generate_words(PATH)


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
            self.app.push_screen("game")

        elif event.button.id == "exit":
            self.app.exit()

    def on_mount(self) -> None:
        self.add_class("screen_menu")
