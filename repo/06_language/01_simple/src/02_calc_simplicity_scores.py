import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import torch
from transformers import pipeline
from itertools import combinations
import random
import matplotlib.pyplot as plt


# load sermons
df_sermons = pd.read_csv("intermediate/sermonscopy.csv")

# define metrics
wordLengthMetrics = ['avgWordChars', 'perW7C', 'perW6C', 'avgWordSylls', 'perWgeq3Sy', 'perWlt3Sy', 'perW2Sy', 'perW1Sy']
sentenceLengthMetrics = ['avgSentenceChars', 'avgSentenceWords', 'avgSentenceSylls', 'prSentenceChar']
wordRarityMetrics = ['perDaleChall', 'freqBrown', 'freqWordfreq']
posMetrics = ['prNoun', 'prPropN', 'prAdj', 'prVerb', 'prAdv']

metrics = wordLengthMetrics + sentenceLengthMetrics + wordRarityMetrics + posMetrics
simpleWhenScoreHigh = [
    'perWlt3Sy', 'perW1Sy', 
    'perDaleChall', 'freqBrown', 'freqWordfreq', 
    'prNoun', 'prAdj', 'prVerb', 'prAdv'
]

# normalize metrics
df = df_sermons.dropna(subset= metrics).copy().reset_index(drop= True)

scaler = StandardScaler()
df[metrics] = scaler.fit_transform(df[metrics])

# flip metrics for consistency
for metric in simpleWhenScoreHigh:
    df[metric] = -df[metric]

# calculate scores for each metric group
df['word_length_score'] = df[wordLengthMetrics].mean(axis= 1)
df['sentence_length_score'] = df[sentenceLengthMetrics].mean(axis= 1)
df['word_rarity_score'] = df[wordRarityMetrics].mean(axis= 1)
df['pos_score'] = df[posMetrics].mean(axis= 1)
metricScores = ['word_length_score', 'sentence_length_score', 'word_rarity_score', 'pos_score']

weights = [4, 2, 2, 1]
df['complexity'] = df[metricScores].dot(weights)
df['simplicity'] = -df['complexity']


# --- PCA --- #

# perform PCA on metrics
pca = PCA(n_components= 4)
pcs = pca.fit_transform(df[metrics])

# analyze metrics effect on variance across sermon texts
loadings = pd.DataFrame(pca.components_, columns= metrics, index= ['PC1','PC2','PC3','PC4'])
print(pca.explained_variance_ratio_)
print(loadings.T)
print()


# --- get initial simplicity scores --- #

random.seed(100)
bart = pipeline('zero-shot-classification', model= 'facebook/bart-large-mnli')

def subtext(text, max_chars= 1000):
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(' ', 1)[0]

def write_prompt(a, text_a, b, text_b):
    return {
        'A': a,
        'B': b,
        'prompt': f"Text A: {subtext(text_a)} Text B: {subtext(text_b)} Easier:"
    }

def get_pair_prompts(df, n_pairs):
    prompts = []
    seen = set()

    while len(prompts) < n_pairs:
        i, j = sorted(random.sample(range(len(df)), 2))
        if (i,j) in seen:
            continue
        seen.add((i,j))
        text_i = df.loc[i, 'sermontext']
        text_j = df.loc[j, 'sermontext']
        prompts.append(write_prompt(i, text_i, j, text_j))

    return prompts

def get_pairwise_simplicity_scores(pairPrompts, bart):
    batch_size = 32
    scores = []

    for start in range(0, len(pairPrompts), batch_size):
        batch = pairPrompts[start:start+batch_size]

        results = bart(
            [pair['prompt'] for pair in batch], 
            candidate_labels= ["Text A", "Text B"], 
            batch_size= batch_size
        )

        for pair, res in zip(batch, results):
            label_scores = dict(zip(res['labels'], res['scores']))
            score = label_scores["Text A"] - label_scores["Text B"]
            
            scores.append({
                'A': pair['A'],
                'B': pair['B'],
                'score': score
            })
        
        if start % 320 == 0:
            print(f"{start}/{len(pairPrompts)}")
    
    return scores

pairPrompts = get_pair_prompts(df, 4)
initialScores = get_pairwise_simplicity_scores(pairPrompts, bart)

for score in initialScores:
    print(score)
    print(f"Simplicity score A: {df.iloc[score['A']]['simplicity']}")
    print(f"Simplicity score B: {df.iloc[score['B']]['simplicity']}")
    print()
    print()
    print()
