import pandas as pd
import re

# load sermon texts
df = pd.read_csv("input/sermons.csv")

# helper functions
def get_words_from_text(text):
    words = re.findall(r"\b\w+(?:['-]\w+)*\b", text.lower())

    filtered = []
    for w in words:
        if w.replace(',', '').replace('-', '').replace('.', '').replace(':', '').isdigit():
            continue
        if len(w) == 1 and w not in ('a', 'i'):
            continue
        filtered.append(w)

    return filtered

def avg_chars_per_word(words):
    return

def get_words_with_at_least_7_chars(words):
    return

def get_words_with_at_least_6_chars(words):
    return

def avg_syllables_per_word(words):
    return

def get_words_with_at_least_3_syllables(words):
    return

def get_words_with_less_than_3_syllables(words):
    return

def get_words_with_2_syllables(words):
    return

def get_words_with_1_syllable(words):
    return
