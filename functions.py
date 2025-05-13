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
        print(f"Error inesperado:  {e}")     


# Funcion para elegir la palabra clave de manera aleatoria
def Select_Words(words):
    if not words: 
        return None
    letters_quantity = len(words)
    return random.choice(words)

file_json = "words.json"
words = generate_words(file_json)

# Funcion para la busqueda y confirmacion de la letras
def search_letter(array, e):
    result = any(x == e for x in array)
    return result

Select_Words(words)