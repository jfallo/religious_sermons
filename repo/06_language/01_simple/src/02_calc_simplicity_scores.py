import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression


# load sermons
df_sermons = pd.read_csv("intermediate/sermons copy.csv")

# define metrics
wordLengthMetrics = ['avgWordChars', 'perW7C', 'perW6C', 'avgWordSylls', 'perWgeq3Sy', 'perWlt3Sy', 'perW2Sy', 'perW1Sy']
sentenceLengthMetrics = ['avgSentenceChars', 'avgSentenceWords', 'avgSentenceSylls', 'prSentenceChar']
wordRarityMetrics = ['perDaleChall', 'freqBrown', 'freqWordfreq']
posMetrics = ['prNoun', 'prPropN', 'prAdj', 'prVerb', 'prAdv']

metrics = wordLengthMetrics + sentenceLengthMetrics + wordRarityMetrics + posMetrics
simpleWhenScoreHigh = ['perWlt3Sy', 'perW1Sy', 'perDaleChall', 'freqBrown', 'freqWordfreq']

# normalize metrics
df = df_sermons.dropna(subset= metrics).copy()

scaler = StandardScaler()
df[metrics] = scaler.fit_transform(df[metrics])

# calculate scores for each metric group
df['word_length_score'] = df[wordLengthMetrics].mean(axis= 1)
df['sentence_length_score'] = df[sentenceLengthMetrics].mean(axis= 1)
df['word_rarity_score'] = df[wordRarityMetrics].mean(axis= 1)
df['pos_score'] = df[posMetrics].mean(axis= 1)
scores = ['word_length_score', 'sentence_length_score', 'word_rarity_score', 'pos_score']


# --- PCA --- #

# flip metrics for consistency
for metric in simpleWhenScoreHigh:
    df[metric] = -df[metric]

# perform PCA on metrics
pca = PCA(n_components= 4)
pcs = pca.fit_transform(df[metrics])

# analyze metrics effect on variance across sermon texts
loadings = pd.DataFrame(pca.components_, columns= metrics, index= ['PC1','PC2','PC3','PC4'])
print(pca.explained_variance_ratio_)
print(loadings.T)


# --- get simplicity score --- #

df['simplicity'] = ...

# analyze simplicity over time
avgSimplicityByYear = df.groupby('year')['simplicity'].mean().sort_index()
years = avgSimplicityByYear.index.values.reshape(-1,1)
simplicity = avgSimplicityByYear.values

reg = LinearRegression()
reg.fit(years, simplicity)
m, b = reg.coef_[0], reg.intercept_
r2 = reg.score(years, simplicity)
preds = reg.predict(years)

plt.scatter(years, simplicity)
plt.plot(years, preds, color='red', linestyle='--', label='Regression Line')
plt.xlabel('Year')
plt.ylabel('Mean Simplicity Score')
plt.title('Sermon Text Simplicity Scores Over Time')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.text(
    0.05, 0.95,
    f"Slope: {m:.4f}\nR²: {r2:.3f}",
    transform=plt.gca().transAxes,
    verticalalignment='top',
    bbox=dict(facecolor='white', alpha=0.8)
)