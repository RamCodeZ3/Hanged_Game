from textual.app import App
from Screen.menu import Menu
from Screen.game import Game
from Screen.game_over import Game_over


class MyApp(App):

    SCREENS = {
        "menu": Menu,
        "over": Game_over,
        "game": Game,
    }

    def on_mount(self) -> None:
        self.push_screen("menu")


if __name__ == "__main__":

    app = MyApp()
    app.run()
