import pandas as pd
import re, csv
from nltk.corpus import brown
from collections import Counter
from wordfreq import word_frequency
import spacy
nlp = spacy.load('en_core_web_sm')

# load sermon texts
df = pd.read_csv("input/sermons.csv")

# word length helper functions
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

    exceptionAdd = ['serious', 'crucial']
    exceptionDel = ['fortunately', 'unfortunately']

    if len(word) <= 3:
        return 1

    # ed / es endings 
    if word.endswith(('es', 'ed')):
        if len(re.findall(r'[aeiouy]{2}', word)) > 1 or len(re.findall(r'[aeiouy][^aeiouy]', word)) > 1:
            if not word.endswith(('ted', 'tes', 'ses', 'ied', 'ies')):
                discard += 1

    # silent trailing e
    leException = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
    if word.endswith('e'):
        if not (word.endswith('le') and word not in leException):
            discard += 1

    # vowel groups
    discard += len(re.findall(r'[aeiouy]{2}', word))
    discard += len(re.findall(r'[aeiouy]{3}', word))

    numVowels = len(re.findall(r'[aeiouy]', word))

    # mc
    if word.startswith('mc'):
        syllables += 1

    # trailing y
    if len(word) > 1 and word.endswith('y') and word[-2] not in 'aeiou':
        syllables += 1

    # internal y
    for i, c in enumerate(word):
        if c == 'y' and 0 < i < len(word)-1:
            if word[i-1] not in 'aeiou' and word[i+1] not in 'aeiou':
                syllables += 1

    # tri / bi
    if len(word) > 3 and word.startswith('tri') and word[3] in 'aeiou':
        syllables += 1
    if len(word) > 2 and word.startswith('bi') and word[2] in 'aeiou':
        syllables += 1

    # ian
    if word.endswith('ian') and not word.endswith(('cian', 'tian')):
        syllables += 1

    # co
    co1 = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co2 = ['coapt','coed','coinci']
    if len(word) > 2 and word.startswith('co') and word[2] in 'aeiou':
        if any(word.startswith(x) for x in co2):
            syllables += 1
        elif any(word.startswith(x) for x in co1):
            pass
        else:
            syllables += 1

    # pre
    pre1 = ['preach']
    if len(word) > 3 and word.startswith('pre') and word[3] in 'aeiou':
        if not any(word.startswith(x) for x in pre1):
            syllables += 1

    # n't
    negative = ["doesn't","isn't","shouldn't","couldn't","wouldn't"]
    if word.endswith("n't") and word in negative:
        syllables += 1

    # exceptions
    if word in exceptionDel:
        discard += 1
    if word in exceptionAdd:
        syllables += 1

    count = numVowels - discard + syllables

    return max(1, count)

def get_words_with_at_least_x_chars(words, x):
    return [w for w in words if len(w) >= x]
def get_words_with_at_least_x_syllables(words, x):
    return [w for w in words if count_syllables(w) >= x]
def get_words_with_less_than_x_syllables(words, x):
    return [w for w in words if count_syllables(w) < x]
def get_words_with_x_syllables(words, x):
    return [w for w in words if count_syllables(w) == x]

def get_word_length_metrics(text):
    words = get_words_from_text(text)

    # avg chars per word
    avgWordChars = sum(len(w) for w in words) / len(words) if words else 0
    # percent of words with at least 7, 6 characters
    W7C = len(get_words_with_at_least_x_chars(words, 7)) / len(words) if words else 0
    W6C = len(get_words_with_at_least_x_chars(words, 6)) / len(words) if words else 0
    # avg syllables per word
    avgWordSylls = sum(count_syllables(w) for w in words) / len(words) if words else 0
    # percent of words with at least 3 syllables
    Wgeq3Sy = len(get_words_with_at_least_x_syllables(words, 3)) / len(words) if words else 0
    # percent of words with less than 3 syllables
    Wlt3Sy = len(get_words_with_less_than_x_syllables(words, 3)) / len(words) if words else 0
    # percent of words with 2, 1 syllable(s)
    W2Sy = len(get_words_with_x_syllables(words, 2)) / len(words) if words else 0
    W1Sy = len(get_words_with_x_syllables(words, 1)) / len(words) if words else 0

    return avgWordChars, W7C, W6C, avgWordSylls, Wgeq3Sy, Wlt3Sy, W2Sy, W1Sy


# sentence length helper functions
BULLET_PATTERN = re.compile(r'^\s*(?:[ivxlcdm]+|[a-z]|\d+)\.\s*$', re.IGNORECASE)

def get_sentences_from_text(text):
    sentences = re.findall(r'[^.!?]+[.!?]|[^.!?]+$', text)
    
    filtered = []
    for s in sentences:
        s = s.strip()
        
        if not s:
            continue
        if BULLET_PATTERN.match(s):
            continue
        if all(c in '.!?,' for c in s):
            continue
        
        filtered.append(s)

    return filtered

def get_sentence_length_metrics(text):
    sentences = get_sentences_from_text(text)

    # avg chars per sentence
    avgSentenceChars = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
    # avg words per sentence
    avgSentenceWords = sum(len(get_words_from_text(s)) for s in sentences) / len(sentences) if sentences else 0
    # avg syllables per sentence
    avgSentenceSylls = sum(sum(count_syllables(w) for w in get_words_from_text(s)) for s in sentences) / len(sentences) if sentences else 0
    # proportion of sentences to characters in text
    prSentencesChars = len(sentences) / len(text) if text else 0

    return avgSentenceChars, avgSentenceWords, avgSentenceSylls, prSentencesChars


# rare word helper functions
with open('input/dale-chall-words.txt') as f:
    wordsDaleChall = f.read().strip().lower().split(' ')
wordsBrown = [w.lower() for w in brown.words()] # need to run nltk.download('brown')
countsBrown = Counter(wordsBrown)

def get_word_rarity_metrics(text):
    words = get_words_from_text(text)

    # percentage of words that are Dale-Chall words
    percentDaleChall = sum(1 for w in words if w in wordsDaleChall) / len(words) if words else 0
    # avg freq of words relative to freq of "the" in Brown corpus
    theFreqBrown = countsBrown['the']
    freqsBrown = [countsBrown.get(w, 0)/theFreqBrown for w in words if w in countsBrown]
    freqBrown = sum(freqsBrown)/len(freqsBrown) if freqsBrown else 0
    # avg freq of words relative to freq of "the" in Google Books corpus
    theFreqWordfreq = word_frequency('the', 'en')
    freqsWordfreq = [word_frequency(w, 'en')/theFreqWordfreq for w in words]
    freqWordfreq = sum(freqsWordfreq)/len(freqsWordfreq) if freqsWordfreq else 0

    return percentDaleChall, freqBrown, freqWordfreq


# parts of speech metrics
def get_pos_words_from_text(text):
    doc = nlp(text)
    nouns = []
    propNs = []
    adjs = []
    verbs = []
    advs = []

    for token in doc:
        if token.pos_ == "NOUN":
            nouns.append(token.text.lower())
        elif token.pos_ == "PROPN":
            propNs.append(token.text.lower())
        elif token.pos_ == "ADJ":
            adjs.append(token.text.lower())
        elif token.pos_ == "VERB":
            verbs.append(token.text.lower())
        elif token.pos_ == "ADV":
            advs.append(token.text.lower())

    return nouns, propNs, adjs, verbs, advs

def get_pos_metrics(text):
    nouns, propNs, adjs, verbs, advs = get_pos_words_from_text(text)
    totalWords = len(nouns) + len(propNs) + len(adjs) + len(verbs) + len(advs)

    if totalWords == 0:
        return 0, 0, 0, 0, 0

    # proportion of parts of speech to total words
    prNoun = len(nouns)/totalWords
    prPropN = len(propNs)/totalWords
    prAdj = len(adjs)/totalWords
    prVerb = len(verbs)/totalWords
    prAdv = len(advs)/totalWords

    return prNoun, prPropN, prAdj, prVerb, prAdv


df[['avgWordChars', 'W7C', 'W6C', 'avgWordSylls', 'Wgeq3Sy', 'Wlt3Sy', 'W2Sy', 'W1Sy']] = df['sermontext'].apply(
    lambda text : get_word_length_metrics(text) if pd.notna(text) else [None] * 8
).tolist()
df[['avgSentenceChars', 'avgSentenceWords', 'avgSentenceSylls', 'prSentencesChars']] = df['sermontext'].apply(
    lambda text : get_sentence_length_metrics(text) if pd.notna(text) else [None] * 4
).tolist()
df[['percentDaleChall', 'freqBrown', 'freqWordFreq']] = df['sermontext'].apply(
    lambda text : get_word_rarity_metrics(text) if pd.notna(text) else [None] * 3
).tolist()
df[['prNoun', 'prPropN', 'prAdj', 'prVerb', 'prAdv']] = df['sermontext'].apply(
    lambda text : get_pos_metrics(text) if pd.notna(text) else [None] * 5
).tolist()
df.to_csv("intermediate/sermons.csv", index= False, quoting= csv.QUOTE_ALL)
