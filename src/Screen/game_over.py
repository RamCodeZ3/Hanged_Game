from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
import functions as func


class Game_over(Screen):
    def __init__(self, word_category, score_wordcompleted):
        super().__init__()
        self.correct_word, self.category = word_category
        self.score, self.word_complete = score_wordcompleted
        self.word_max = 100

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(
                "Juego terminado la palabra correcta era:",
                id="game_over_message"
            ),
            Static(f"{self.correct_word}", id="correct_word"),
            Static(f"Puntuación final: {self.score}", id="final_score"),
            Static(
                f"Palabras completadas: {self.word_complete}/{self.word_max}",
                id="words_completed"
            ),
            Button("Volver al inicio", id="restart"),
            Button("Reintentar", id="retry"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "restart":
            while len(self.app.screen_stack) > 1:
                self.app.pop_screen()
            self.app.push_screen("menu")

        elif event.button.id == "retry":
            while len(self.app.screen_stack) > 1:
                self.app.pop_screen()
            self.app.push_screen("game")

    def on_mount(self) -> None:
        self.add_class("screen_game_over")
