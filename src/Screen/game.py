from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical, Horizontal, Center
from textual.screen import Screen
from textual.events import Key
import utils.fuction as func
from Screen.game_over import Game_over


class Game(Screen):
    """Pantalla principal del juego del ahorcado"""

    def __init__(self):
        super().__init__()
        self.score = 0
        self.word_complete = 0
        self.word_max = 10
        self.category = ""
        self.selected_word = ""
        self.signs = []
        self.chance = 6
        self.Letter_used = set()

    def reset_data(self):
        category, word = func.Select_Words()
        self.category = category
        self.selected_word = word.lower()
        self.signs = ["❌"] * len(self.selected_word)
        self.chance = 6
        self.Letter_used.clear()
        self.word_complete = 0
        self.score = 0

        self.query_one("#category", Static).update(f"Categoría: {self.category}")
        self.query_one("#word_secret", Static).update(" ".join(self.signs))
        self.query_one("#game_message", Static).update("¡Presiona una letra para comenzar!")
        self.query_one("#score", Static).update(f"Puntuación: {self.score}")
        self.query_one("#life", Static).update("❤️ " * self.chance)
        self.query_one("#letters_user", Static).update("Letras usadas:")

    async def continue_game(self, selected_word: str, category: str, signs: list) -> None:
        """Continuar el juego con una nueva palabra"""
        if hasattr(self, '_continuing') and self._continuing:
            return
        self._continuing = True

        try:
            self.selected_word = selected_word.lower()
            self.category = category
            self.signs = signs
            self.chance = 6
            self.Letter_used.clear()
            self.query_one("#category", Static).update(f"Categoría: {self.category}")
            self.query_one("#word_secret", Static).update(" ".join(self.signs))
            self.query_one("#game_message", Static).update("¡Nueva palabra! ¡Suerte!")
            self.query_one("#life", Static).update("❤️ " * self.chance)
            self.query_one("#letters_user", Static).update("Letras usadas:")
        
        finally:
            self._continuing = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield Center(
            Vertical(
                Vertical(
                    Static("Puntuación: 0", id="score"),
                    Static("❤️ ❤️ ❤️ ❤️ ❤️ ❤️", id="life"),
                    id="hud",
                    classes="justify-between",
                ),
                Static("Categoría: ", id="category", classes="category"),
                Static("❌ ❌ ❌ ❌ ❌ ❌", id="word_secret", classes="word"),
                Static("¡Presiona una letra para comenzar!", id="game_message", classes="message"),
                Static("Letras usadas:", id="letters_user", classes="used"),
                Button("Volver al menú", id="go_back", variant="warning"),
                id="game_container",
                classes="vertical-center",
            )
        )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_back":
            self.reset_data()
            self.app.pop_screen()
            self.app.push_screen("menu")

    async def on_key(self, event: Key) -> None:
        letter = event.key

        if letter.isalpha() and len(letter) == 1 and self.chance > 0:
            if letter.lower() in self.Letter_used:
                self.query_one("#game_message", Static).update(
                    f"Ya intentaste la letra '{letter}'."
                )
                return

            self.Letter_used.add(letter.lower())
            self.query_one("#letters_user", Static).update(
                f"Letras usadas: {', '.join(sorted(self.Letter_used))}"
            )

            coincidences = func.search_letter(self.selected_word, letter)

            if coincidences:
                for indice, _ in coincidences:
                    self.signs[indice] = letter.lower()
                self.query_one("#word_secret", Static).update(" ".join(self.signs))
                self.score += 5
                self.query_one("#score", Static).update(f"Puntuación: {self.score}")

                if self.signs == list(self.selected_word):
                    self.query_one("#game_message", Static).update("🎉 ¡Ganaste esta ronda!")
                    self.score += 25
                    self.word_complete += 1
                    self.query_one("#score", Static).update(f"Puntuación: {self.score}")

                    if self.word_complete == self.word_max:
                        category, word = func.Select_Words()
                        self.set_timer(
                            0.5,
                            lambda: self.continue_game(word, category, ["❌"] * len(word)),
                        )
                        self.reset_data()
                        self.app.pop_screen()
                        self.app.push_screen("won")
                        return

                    category, word = func.Select_Words()
                    self.set_timer(
                        1.5,
                        lambda: self.continue_game(word, category, ["❌"] * len(word)),
                    )

            else:
                self.chance -= 1
                self.query_one("#life", Static).update("❤️ " * self.chance)
                self.query_one("#game_message", Static).update(
                    f"No se encontró la letra '{letter}'. ¡Intenta de nuevo!"
                )
                self.score -= 3
                self.query_one("#score", Static).update(f"Puntuación: {self.score}")

                if self.chance == 0:
                    word_category = (self.selected_word, self.category)
                    score_wordcompleted = (self.score, self.word_complete)
                    self.reset_data()
                    self.app.push_screen(Game_over(word_category, score_wordcompleted))
        else:
            self.query_one("#game_message", Static).update(
                "Por favor ingresa una letra válida (una sola letra del alfabeto)."
            )

    def on_mount(self) -> None:
        self.reset_data()
        self.add_class("screen_game")
