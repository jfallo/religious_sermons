import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import textstat


# load sermons
df_sermons = pd.read_csv("intermediate/sermons.csv")

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
scores = ['word_length_score', 'sentence_length_score', 'word_rarity_score', 'pos_score']

weights = [1, 1, 1, 1]
df['complexity'] = df[scores].dot(weights)
df['simplicity'] = -df['complexity']


# sermon-level regression for each metric and composite score
for metric in metrics + scores:
    slope, intercept, r, p, se = stats.linregress(df['year'], df[metric])
    print(f"{metric}: slope={slope:.4f}, r={r:.3f}, p={p:.3f}")

# yearly aggregation
avgSimplicityByYear = df.groupby('year')['simplicity'].mean().sort_index()
years = avgSimplicityByYear.index.values.reshape(-1,1)
simplicity = avgSimplicityByYear.values
# sermon-level regression for simplicity score
slope, intercept, r, p, se = stats.linregress(df['year'], df['simplicity'])
print(f"simplicity_score_pred: slope={slope:.4f}, r={r:.3f}, p={p:.3f}")
preds = slope * years.flatten() + intercept
# sermon counts
sermon_counts = df.groupby('year').size()

# plot simplicity over time and sermons per year
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(years, simplicity)
axes[0].plot(years, preds, color= 'red', linestyle= '--', label= 'Regression Line')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Mean Simplicity Score')
axes[0].set_title('Sermon Simplicity Over Time')
axes[0].grid(True, linestyle= '--', alpha= 0.5)
axes[0].text(
    0.05, 0.95,
    f"Slope: {slope:.4f}\nR²: {r**2:.3f}\np={p:.3f}",
    transform= axes[0].transAxes,
    verticalalignment= 'top',
    bbox= dict(facecolor= 'white', alpha= 0.8)
)
axes[1].bar(sermon_counts.index, sermon_counts.values, color= 'steelblue', alpha= 0.7)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Number of Sermons')
axes[1].set_title('Sermons Per Year')
axes[1].grid(True, linestyle= '--', alpha= 0.5)
plt.tight_layout()
plt.show()

# sermon-level regression for Flesch Kincaid score (robustness check)
df['flesch_kincaid'] = df['sermontext'].apply(textstat.flesch_kincaid_grade)
slope, intercept, r, p, se = stats.linregress(df['year'], df['flesch_kincaid'])
print(f"flesch_kincaid: slope={slope:.4f}, r={r:.3f}, p={p:.3f}")


# --- PCA --- #

# perform PCA on metrics
pca = PCA(n_components= 4)
pcs = pca.fit_transform(df[metrics])

# analyze metrics effect on variance across sermon texts
loadings = pd.DataFrame(pca.components_, columns= metrics, index= ['PC1','PC2','PC3','PC4'])
print(pca.explained_variance_ratio_)
print(loadings.T)
