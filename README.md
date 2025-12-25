# Hanged Game

**Hanged Game** es un juego del ahorcado desarrollado con **[Textual](https://textual.textualize.io/)**, un framework para crear interfaces de usuario en la terminal con Python.  
El juego desafía al jugador a adivinar palabras dentro de una categoría determinada, gestionando vidas, puntuación y progreso de manera visual y dinámica.

---

## 🚀 Características

- ✅ Interfaz visual en la terminal usando **Textual**.  
- ✅ Sistema de **puntuación** y **vidas**.  
- ✅ Palabras obtenidas desde un archivo **JSON** (`words.json`).  
- ✅ Categorías de palabras aleatorias.  
- ✅ Detección automática de letras correctas e incorrectas.  
- ✅ Pantallas separadas para **menú**, **juego**, **victoria** y **derrota**.  
- ✅ Código modular y limpio mediante clases y funciones reutilizables.  

---

## 🕹️ Cómo jugar

1. Inicia el juego.  
2. Se mostrará una categoría y una palabra oculta representada por símbolos ❌.  
3. Escribe una letra del teclado:  
   - Si aciertas, la letra se revelará.  
   - Si fallas, perderás una vida ❤️.  
4. Gana puntos por cada acierto y ronda completada.  
5. El juego termina cuando adivinas todas las palabras o pierdes todas las vidas.  

---

## 📂 Estructura del proyecto

📦 **Hanged Game**  
┣ 📂 **src**  
┃ ┣ 📂 **data**  
┃ ┃ ┗ 📜 `words.json` — Contiene las palabras y categorías.  
┃ ┣ 📂 **Screen**  
┃ ┃ ┣ 📜 `menu.py` — Pantalla de inicio del juego.  
┃ ┃ ┣ 📜 `game.py` — Lógica principal del juego del ahorcado.  
┃ ┃ ┣ 📜 `game_won.py` — Pantalla de victoria.  
┃ ┃ ┗ 📜 `game_over.py` — Pantalla de derrota.  
┃ ┣ 📂 **styles**  
┃ ┃ ┗ 📜 `styles.tcss` — Estilos visuales de la interfaz.  
┃ ┣ 📂 **utils**  
┃ ┃ ┗ 📜 `fuction.py` — Funciones auxiliares (selección de palabras, búsqueda de letras, etc.).  
┃ ┗ 📜 `main.py` — Punto de entrada principal del programa.  
┣ 📜 `.gitignore`  
┣ 📜 `requirements.txt`  
┣ 📜 `.pre-commit-config.yaml`  
┗ 📜 `README.md`  

---

## 🛠️ Instalación y ejecución

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tuusuario/hanged-game.git
   cd hanged-game
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno**
   - En **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - En **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecuta el juego**
   ```bash
   python src/main.py
   ```

---

## 🧩 Tecnologías utilizadas

- 🐍 **Python 3.10+**  
- 💠 **Textual** (interfaz TUI en terminal)  
- 📜 **JSON** (almacenamiento de palabras y categorías)
- TCSS (Para los estilos)

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**, lo que significa que puedes usarlo, modificarlo y distribuirlo libremente, siempre que se mantenga el crédito correspondiente.
