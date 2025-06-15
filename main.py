from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
from textual.events import Key
import functions as func

words = func.generate_words("words.json")

class Game_room(Screen):
    def __init__(self):
        super().__init__()
        self.selected_word = None  # Almacena la palabra seleccionada
        self.category = None
        self.signs = None  # Almacena los signos (*)

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
                welcome_message.update("No se encontraron palabras. Verifica el archivo words.json")
                return
            result = func.Select_Words(words)
            if not result or not isinstance(result, tuple) or len(result) != 2:
                welcome_message = self.query_one("#welcome_message", Static)
                welcome_message.update("Error: No se pudo seleccionar una palabra válida")
                return
            self.category, self.selected_word = result
            self.selected_word = self.selected_word.lower()  # Normalizar a minúsculas
            if not self.selected_word or not isinstance(self.selected_word, str) or \
               not self.category or not isinstance(self.category, str):
                welcome_message = self.query_one("#welcome_message", Static)
                welcome_message.update("Error: Palabra o categoría no válida")
                return
            self.signs = ["❌"] * len(self.selected_word)
            self.app.push_screen(Game(self.selected_word, self.category, self.signs))
        elif event.button.id == "exit":
            self.app.exit()

class Game(Screen):
    def __init__(self, selected_word: str, category: str, signs: list, score: int = 0):
        super().__init__()
        self.selected_word = selected_word.lower()  # Almacena la palabra seleccionada
        self.category = category            # Almacena la categoría
        self.signs = signs                  # Almacena los signos (lista de asteriscos)
        self.chance = 6                     # Contador de intentos fallidos
        self.Letter_used = set()          # Letras ya intentadas
        self.score = score                      # Puntuación inicial
        self.word_complete = 0              # cantidad de palabras completadas
        self.word_max = 100                 # cantidad de palabras a completar para ganar

 # selecionar una nueva palabra y continuar el juego hasta que se complete o se pierda
    async def continue_game(self, selected_word: str, category: str, signs: list) -> None:
        if hasattr(self, '_continuing') and self._continuing:
         return
        self._continuing = True
        try:
            self.selected_word = selected_word.lower()
            self.category = category
            self.signs = signs
            self.chance = 6  # Reinicia el contador de intentos fallidos
            self.Letter_used.clear()  # Limpia las letras usadas
            self.query_one("#category", Static).update(f"Categoría: {self.category}")
            self.query_one("#word_Secret", Static).update("".join(self.signs))
            self.query_one("#game_message", Static).update("Hora de jugar!")
            self.query_one("#life", Static).update(f"{"❤️" * self.chance}")
            self.query_one("#letters_user", Static).update("Letras usadas:")
            self.query_one("#game_title", Static).update(f"Adivina la palabra: {self.selected_word}")
        finally: 
            self._continuing = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(f"Adivina la palabra: {self.selected_word}", id="game_title"),
            Static(f"Categoría: {self.category}", id="category"),
            Static("".join(self.signs), id="word_Secret"),
            Static("Hora de jugar!", id="game_message"),
            Static(f"Puntuación: {self.score}", id="score"), 
            Static(f"{"❤️" * self.chance}", id="life"),
            Static("Letras usadas:", id="letters_user"),
            Button("Volver", id="go_back"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_back":
            self.app.pop_screen()

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
         coincidencias = func.search_letter(self.selected_word, letter)
         if  coincidencias:
            for indice, _ in coincidencias:
                self.signs[indice] = letter.lower()
            self.query_one("#word_Secret", Static).update("".join(self.signs))
            self.score += 5
            self.query_one("#score", Static).update(f"Puntuación: {self.score}")
            # Verificar si la palabra está completa
            if self.signs == list(self.selected_word):
                self.query_one("#game_message", Static).update("¡Ganaste!")
                self.score += 25
                self.word_complete += 1
                self.query_one("#score", Static).update(f"Puntuación: {self.score}")
                
                new_word = func.Select_Words(words)
                if not new_word or not isinstance(new_word, tuple) or len(new_word) != 2:
                    self.query_one("#game_message", Static).update("Error: No se pudo seleccionar una nueva palabra")
                    return
                category, word = new_word
                self.set_timer(1.5, lambda: self.continue_game(word, category, ['❌'] * len(word)))
         else:
             print(f"No se encontró la letra '{letter}' en la palabra.")
             self.chance -= 1
             self.query_one("#life", Static).update(f"{"❤️" * self.chance}")
             self.query_one("#game_message", Static).update(
                 f"No se encontró la letra '{letter}'. Intenta de nuevo."
             )
             self.score -= 3 # Decrementa la puntuación por un intento fallido
             self.query_one("#score", Static).update(f"Puntuación: {self.score}")
             # Verifica si el jugador ha perdido
             if self.chance == 0:
              self.app.push_screen(Game_over(self.selected_word, self.category,  self.score, self.word_complete))
        else:
            self.query_one("#game_message", Static).update("Por favor, ingresa una letra válida (una sola letra del alfabeto).")

class Game_over(Screen):
    def __init__(self, selected_word: str,category:str, score: int, word_complete: int):
        super().__init__()
        self.correct_word = selected_word
        self.category = category
        self.score = score
        self.word_complete = word_complete
        self.word_max = 100                 # cantidad de palabras a completar para ganar

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Juego terminado la palabra correcta era:", id="game_over_message"),
            Static(f"{self.correct_word}", id="correct_word"),  # Aquí se actualizará la palabra correcta
            Static(f"Puntuación final: {self.score}", id="final_score"),
            Static(f"Palabras completadas: {self.word_complete}/{self.word_max}", id="words_completed"),
            Button("Volver al inicio", id="restart"),
            Button("Reintentar", id="retry"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "restart":
            while len(self.app.screen_stack) > 1:
             self.app.pop_screen()
            self.app.push_screen("room")

        elif event.button.id == "retry":
            while len(self.app.screen_stack) > 1:
             self.app.pop_screen()
             new_category, new_word= func.Select_Words(words)
            self.app.push_screen(Game(new_word, new_category, ["❌"] * len(self.correct_word), 0))

class MyApp(App):
    SCREENS = {
        "room": Game_room,
        "over": Game_over,
        "game": Game,
    }

    def on_mount(self) -> None:
        self.push_screen("room")

if __name__ == "__main__":
    app = MyApp()
    app.run()