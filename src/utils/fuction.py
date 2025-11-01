import os
import json
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, "data", "words.json")

def Select_Words():
    try:
        with open(PATH, "r", encoding="utf-8") as file:
            word = json.load(file)
    
    except FileNotFoundError:
        print(f"Error: El archivo {PATH} no se encontró ❌")
        return None
    
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

    if not word:
        return None, None
    category = random.choice(list(word.keys()))
    word = random.choice(word[category])
    return category, word


def search_letter(word, letter):
    try:
        letter = letter.lower()
        word = word.lower()
        return [(i, word[i]) for i in range(len(word)) if word[i] == letter]
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []
