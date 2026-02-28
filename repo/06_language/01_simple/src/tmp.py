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

def count_syllables(word):
    word = word.lower()
    syllables = 0
    discard = 0

    exception_add = ['serious', 'crucial']
    exception_del = ['fortunately', 'unfortunately']

    if len(word) <= 3:
        return 1

    # ed / es endings 
    if word.endswith(("es", "ed")):
        if len(re.findall(r'[aeiouy]{2}', word)) > 1 or len(re.findall(r'[aeiouy][^aeiouy]', word)) > 1:
            if not word.endswith(("ted", "tes", "ses", "ied", "ies")):
                discard += 1

    # silent trailing e
    le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
    if word.endswith("e"):
        if not (word.endswith("le") and word not in le_except):
            discard += 1

    # vowel groups
    discard += len(re.findall(r'[aeiouy]{2}', word))
    discard += len(re.findall(r'[aeiouy]{3}', word))

    numVowels = len(re.findall(r'[aeiouy]', word))

    # mc
    if word.startswith("mc"):
        syllables += 1

    # trailing y
    if len(word) > 1 and word.endswith("y") and word[-2] not in "aeiou":
        syllables += 1

    # internal y
    for i, c in enumerate(word):
        if c == "y" and 0 < i < len(word)-1:
            if word[i-1] not in "aeiou" and word[i+1] not in "aeiou":
                syllables += 1

    # tri / bi
    if len(word) > 3 and word.startswith("tri") and word[3] in "aeiou":
        syllables += 1
    if len(word) > 2 and word.startswith("bi") and word[2] in "aeiou":
        syllables += 1

    # ian
    if word.endswith("ian") and not word.endswith(("cian", "tian")):
        syllables += 1

    # co
    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']
    if len(word) > 2 and word.startswith("co") and word[2] in 'aeiou':
        if any(word.startswith(x) for x in co_two):
            syllables += 1
        elif any(word.startswith(x) for x in co_one):
            pass
        else:
            syllables += 1

    # pre
    pre_one = ['preach']
    if len(word) > 3 and word.startswith("pre") and word[3] in 'aeiou':
        if not any(word.startswith(x) for x in pre_one):
            syllables += 1

    # n't
    negative = ["doesn't","isn't","shouldn't","couldn't","wouldn't"]
    if word.endswith("n't") and word in negative:
        syllables += 1

    # exceptions
    if word in exception_del:
        discard += 1
    if word in exception_add:
        syllables += 1

    count = numVowels - discard + syllables

    return max(1, count)

def avg_chars_per_word(words):
    return sum(len(w) for w in words) / len(words) if words else 0

def get_words_with_at_least_x_chars(words, x):
    return [w for w in words if len(w) >= x]

def avg_syllables_per_word(words):
    return sum(count_syllables(w) for w in words) / len(words) if words else 0

def get_words_with_at_least_x_syllables(words, x):
    return [w for w in words if count_syllables(w) >= x]

def get_words_with_less_than_x_syllables(words, x):
    return [w for w in words if count_syllables(w) < x]

def get_words_with_x_syllables(words, x):
    return [w for w in words if count_syllables(w) == x]


for text in df.head(1)['sermontext']:
    print(avg_syllables_per_word(get_words_from_text(text)))
