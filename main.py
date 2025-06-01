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
            # Selecciona una palabra aleatoria
            result = func.Select_Words(words)
            # Verifica que el resultado sea una tupla válida
            if not result or not isinstance(result, tuple) or len(result) != 2:
                welcome_message = self.query_one("#welcome_message", Static)
                welcome_message.update("Error: No se pudo seleccionar una palabra válida")
                return
            self.category, self.selected_word = result
            # Verifica que self.selected_word y self.category sean strings válidos
            if not self.selected_word or not isinstance(self.selected_word, str) or \
               not self.category or not isinstance(self.category, str):
                welcome_message = self.query_one("#welcome_message", Static)
                welcome_message.update("Error: Palabra o categoría no válida")
                return
            # Crea una lista de asteriscos basada en la longitud de la palabra
            self.signs = ["❌"] * len(self.selected_word)
            # Pasa la palabra seleccionada, la categoría y los signos a la pantalla Game
            self.app.push_screen(Game(self.selected_word, self.category, self.signs))
        
        elif event.button.id == "exit":
            self.app.exit()

class Game(Screen):
    def __init__(self, selected_word: str, category: str, signs: list):
        super().__init__()
        self.selected_word = selected_word  # Almacena la palabra seleccionada
        self.category = category            # Almacena la categoría
        self.signs = signs                  # Almacena los signos (lista de asteriscos)
        self.chance = 6                     # Contador de intentos fallidos
        self.letras_usadas = set()          # Letras ya intentadas

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Adivina la palabra"),
            Static(f"Categoría: {self.category}", id="category"),
            Static("".join(self.signs), id="word_Secret"),
            Static("Hora de jugar!", id="game_message"), 
            Static(f"{"❤️" * self.chance}", id="life"),
            Static("Letras usadas:", id="letters_user"),
            Button("Volver", id="go_back"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_back":
            self.app.pop_screen()

    def on_key(self, event: Key) -> None:
        letter = event.key
        # Verifica si la tecla es una letra válida (a-z) y si el juego no ha terminado
        if letter.isalpha() and len(letter) == 1 and self.chance > 0:
            # Verifica si la letra ya fue usada
            if letter.lower() in self.letras_usadas:
                self.query_one("#game_message", Static).update(
                    f"Ya intentaste la letra '{letter}'."
                )
                return
            # Agrega la letra a las usadas y actualiza el Static
            self.letras_usadas.add(letter.lower())
            self.query_one("#letters_user", Static).update(
                f"Letras usadas: {', '.join(sorted(self.letras_usadas))}"
            )
            # Busca la letra en self.selected_word
            coincidencias = func.search_letter(self.selected_word, letter)
            if coincidencias:
                # Actualiza self.signs con las letras encontradas
                for indice, _ in coincidencias:
                    self.signs[indice] = letter.lower()
                # Actualiza el Static con la nueva palabra secreta
                self.query_one("#word_Secret", Static).update("".join(self.signs))
                # Verifica si el jugador ha ganado
                if self.signs == list(self.selected_word.lower()):
                    self.query_one("#game_message", Static).update("¡Ganaste!")
            else:
                # Incrementa el contador de life
                self.chance -= 1
                self.query_one("#life", Static).update(f"{"❤️" * self.chance}")
                self.query_one("#game_message", Static).update(
                    f"No se encontró la letra '{letter}'. Intenta de nuevo."
                )
                # Verifica si el jugador ha perdido
                if self.chance == 0:
                   self.app.push_screen(Game_over(self.selected_word))

class Game_over(Screen):
    def __init__(self, selected_word: str):
        super().__init__()
        self.correct_word = selected_word

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Juego terminado la palabra correcta era:", id="game_over_message"),
            Static(f"{self.correct_word}", id="correct_word"),  # Aquí se actualizará la palabra correcta
            Button("Volver al inicio", id="restart"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "restart":
            while len(self.app.screen_stack) > 1:
             self.app.pop_screen()
            self.app.push_screen("room")

class MyApp(App):
    SCREENS = {
        "room": Game_room,
        "over": Game_over,
    }

    def on_mount(self) -> None:
        self.push_screen("room")

if __name__ == "__main__":
    app = MyApp()
    app.run()