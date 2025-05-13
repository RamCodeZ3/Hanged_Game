
from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
import functions as func

class start(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Bievenido al ahorcado"),
            Button("Comenzar", id="Star"),
            Button("Salir", id="exit"),            
        )
        yield Footer()

class Game(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Palabra clave"),           
        )
        yield Footer()

class Myapp(App):
    SCREENS = {
        "Start": start(),
        "Game": Game()
    }

    def on_mount(self) -> None:
        self.push_screen("Start")

if __name__ == "__main__":
    App = Myapp()
    App.run() 
