from textual.app import ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
from textual.events import Key
import functions as func
from Screen.game_over import Game_over

words = func.generate_words("words.json")
result = func.Select_Words(words)


class Game(Screen):
    def __init__(self, score: int = 0):
        super().__init__()
        self.category, self.selected_word = result
        self.selected_word = self.selected_word.lower()
        self.signs = ["❌"] * len(self.selected_word)
        self.chance = 6
        self.Letter_used = set()
        self.score = score
        self.word_complete = 0
        self.word_max = 100

    async def continue_game(
         self,
         selected_word: str,
         category: str,
         signs: list
    ) -> None:

        if hasattr(self, '_continuing') and self._continuing:
            return
        self._continuing = True

        try:
            self.selected_word = selected_word.lower()
            self.category = category
            self.signs = signs
            self.chance = 6
            self.Letter_used.clear()
            self.query_one("#category", Static).update(
                 f"Categoría: {self.category}"
            )
            self.query_one("#word_Secret", Static).update("".join(self.signs))
            self.query_one("#game_message", Static).update("Hora de jugar!")
            self.query_one("#life", Static).update("#" * self.chance)
            self.query_one("#letters_user", Static).update("Letras usadas:")
            self.query_one("#game_title", Static).update(
                f"Adivina la palabra: {self.selected_word}"
            )

        finally:
            self._continuing = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(
                f"Adivina la palabra: {self.selected_word}", id="game_title"
            ),
            Static(f"Categoría: {self.category}", id="category"),
            Static("".join(self.signs), id="word_Secret"),
            Static("Hora de jugar!", id="game_message"),
            Static(f"Puntuación: {self.score}", id="score"),
            Static("#" * self.chance, id="life"),
            Static("Letras usadas:", id="letters_user"),
            Button("Volver", id="go_back"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_back":
            self.app.pop_screen()

    async def on_key(self, event: Key) -> None:
        words = func.generate_words("words.json")
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
            coincidencias = func.search_letter(self.selected_word, letter)

            if coincidencias:
                for indice, _ in coincidencias:
                    self.signs[indice] = letter.lower()
                self.query_one(
                    "#word_Secret", Static).update("".join(self.signs))
                self.score += 5
                self.query_one("#score", Static).update(
                    f"Puntuación: {self.score}"
                )

                if self.signs == list(self.selected_word):
                    self.query_one("#game_message", Static).update("¡Ganaste!")
                    self.score += 25
                    self.word_complete += 1
                    self.query_one("#score", Static).update(
                        f"Puntuación: {self.score}"
                    )
                    new_word = func.Select_Words(words)
                    if not new_word or not isinstance(
                         new_word,
                         tuple) or len(new_word) != 2:

                        self.query_one("#game_message", Static).update(
                            "Error: No se pudo seleccionar una nueva palabra"
                        )
                        return
                    category, word = new_word
                    self.set_timer(
                        1.5,
                        lambda: self.continue_game(
                            word, category, ['❌'] * len(word)
                        )
                    )

            else:
                print(f"No se encontró la letra '{letter}' en la palabra.")
                self.chance -= 1
                self.query_one("#life", Static).update("#" * self.chance)
                self.query_one("#game_message", Static).update(
                    f"No se encontró la letra '{letter}'. Intenta de nuevo."
                )
                self.score -= 3
                self.query_one("#score", Static).update(
                    f"Puntuación: {self.score}"
                )

                if self.chance == 0:
                    word_category = (self.selected_word, self.category)
                    score_wordcompleted = (self.score, self.word_complete)
                    self.app.push_screen(
                        Game_over(word_category, score_wordcompleted)
                    )

        else:
            self.query_one("#game_message", Static).update("""Por favor,
                 ingresa una letra válida (una sola letra del alfabeto).""")
