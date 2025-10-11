import json
import random

#funcion para la carga de las palabras
def generate_words(files):
    try:
        with open(files, "r", encoding="utf-8") as file:
            word = json.load(file)
            return word
    except FileNotFoundError:
        print(f"Error: El archivo {files} no se encontró")
    except Exception as e:
        print(f"Error inesperado: {e}")


# Funcion para elegir la palabra clave de manera aleatoria
def Select_Words(word_dict):
    if not word_dict:
        return None, None
    # Elegir una categoría aleatoria
    category = random.choice(list(word_dict.keys()))
    # Elegir una palabra aleatoria de esa categoría
    word = random.choice(word_dict[category])
    return category, word

file_json = "words.json"
words = generate_words(file_json)

# Funcion para la busqueda y confirmacion de la letras
def search_letter(word, letter):
    try:
        letter = letter.lower()
        word = word.lower()
        return [(i, word[i]) for i in range(len(word)) if word[i] == letter]
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []  # Devolver una lista vacía en caso de error
    
print(True == [])  # Ejemplo de uso de la función