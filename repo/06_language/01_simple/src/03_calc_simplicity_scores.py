import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import textstat
import os, random
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import choix


# load sermons
df_sermons = pd.read_csv("01_simple/intermediate/sermons.csv")

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

# plot each metric over time before normalizing
df = df_sermons.dropna(subset= metrics).copy().reset_index(drop= True)

# flip metrics for consistency
for metric in simpleWhenScoreHigh:
    df[metric] = -df[metric]

for metric in metrics:
    # yearly aggregation
    avgByYear = df.groupby('year')[metric].mean().sort_index()
    years = avgByYear.index.values.reshape(-1,1)
    metric_score = avgByYear.values
    # sermon-level regression for metric
    slope, intercept, r, p, se = stats.linregress(df['year'], df[metric])
    preds = slope * years.flatten() + intercept

    # save plot
    plt.figure()
    plt.scatter(years, metric_score)
    plt.plot(years, preds, color= 'red', linestyle= '--', label= 'Regression Line')
    plt.xlabel('Year')
    plt.ylabel('Mean Value')
    plt.title(f'{metric} Over Time')
    plt.grid(True, linestyle= '--', alpha= 0.5)
    plt.text(
        0.05, 0.95,
        f"Slope: {slope:.4f}\nR²: {r**2:.3f}\np={p:.3f}",
        transform=plt.gca().transAxes,
        verticalalignment= 'top',
        bbox= dict(facecolor= 'white', alpha= 0.8)
    )
    plt.savefig("01_simple/output/figs/" + f"{metric}_over_time.png")
    plt.close()

# normalize metrics
scaler = StandardScaler()
df[metrics] = scaler.fit_transform(df[metrics])


# --- PCA --- #

# perform PCA on metrics
pca = PCA(n_components= 4)
pcs = pca.fit_transform(df[metrics])

# analyze metrics effect on variance across sermon texts
loadings = pd.DataFrame(pca.components_, columns= metrics, index= ['PC1','PC2','PC3','PC4'])
print(pca.explained_variance_ratio_)
print(loadings.T)
print()
print()


# --- simplicity score from metrics --- #

# calculate scores for each metric group
df['word_length_score'] = df[wordLengthMetrics].mean(axis= 1)
df['sentence_length_score'] = df[sentenceLengthMetrics].mean(axis= 1)
df['word_rarity_score'] = df[wordRarityMetrics].mean(axis= 1)
df['pos_score'] = df[posMetrics].mean(axis= 1)
scores = ['word_length_score', 'sentence_length_score', 'word_rarity_score', 'pos_score']

weights = pca.explained_variance_ratio_
df['complexity'] = df[scores].dot(weights) / sum(weights)
df['simplicity'] = -df['complexity']

# yearly aggregation
avgSimplicityByYear = df.groupby('year')['simplicity'].mean().sort_index()
years = avgSimplicityByYear.index.values.reshape(-1,1)
simplicity = avgSimplicityByYear.values
# sermon-level regression for simplicity score
slope, intercept, r, p, se = stats.linregress(df['year'], df['simplicity'])
preds = slope * years.flatten() + intercept
# sermon counts
sermon_counts = df.groupby('year').size()

# plot simplicity over time and sermons per year
fig, axes = plt.subplots(1, 2, figsize= (14,5))
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
plt.savefig("01_simple/output/figs/avgSimplicityScore_over_time.png")
plt.close()

# sermon-level regression for Flesch Kincaid score (robustness check)
fk_cache = "01_simple/intermediate/flesch_kincaid.csv"
if os.path.exists(fk_cache):
    df['flesch_kincaid'] = pd.read_csv(fk_cache)['flesch_kincaid']
else:
    df['flesch_kincaid'] = df['sermontext'].apply(textstat.flesch_kincaid_grade)
    df[['flesch_kincaid']].to_csv(fk_cache, index= False)

# display sermon-level regression statistics
print(f"{'Metric':<25} {'Slope':>10} {'r':>8} {'p':>8}")
print("-" * 55)

for metric in metrics + scores + ['simplicity', 'flesch_kincaid']:
    slope, intercept, r, p, se = stats.linregress(df['year'], df[metric])
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    print(f"{metric:<25} {slope:>10.4f} {r:>8.3f} {p:>8.3f} {sig}")
print()
print()


# --- get bart sermon text simplicity scores --- #

if torch.backends.mps.is_available():
    device = torch.device('mps')
elif torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
print(f"Using device: {device}")

random.seed(100)
tokenizer = BartTokenizer.from_pretrained("01_simple/bart-simplicity")
model = BartForConditionalGeneration.from_pretrained("01_simple/bart-simplicity")
model.to(device)

def subtext(text, max_length= 1000):
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0]

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

def get_pairwise_simplicity_rankings(pairPrompts, model, tokenizer, device):
    batch_size = 32
    scores = []

    for start in range(0, len(pairPrompts), batch_size):
        batch = pairPrompts[start:start+batch_size]

        inputs = tokenizer(
            [pair['prompt'] for pair in batch],
            return_tensors= 'pt',
            truncation= True,
            max_length= 512,
            padding= True
        ).to(device)

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens= 10)

        decoded = tokenizer.batch_decode(outputs, skip_special_tokens= True)

        for pair, pred in zip(batch, decoded):
            pred = pred.strip()
            if pred == 'Text A':
                score = 1
            elif pred == 'Text B':
                score = -1
            else:
                score = 0   # unexpected output
                print(f"Unexpected prediction: '{pred}'")

            scores.append({
                'A': pair['A'],
                'B': pair['B'],
                'score': score
            })

        if start % 320 == 0:
            print(f"{start}/{len(pairPrompts)}")

    return scores

samples = (
    df.groupby('year')
      .apply(lambda x : x.sample(min(len(x), 500), random_state= 42))
      .index.get_level_values(1)
)
df_sample = df.loc[samples].reset_index(drop= True)

pairPrompts = get_pair_prompts(df_sample, 20 * len(df_sample))
bartRankings = get_pairwise_simplicity_rankings(pairPrompts, model, tokenizer, device)

BT_data = []
for pair in bartRankings:
    if pair['score'] == 1:
        BT_data.append((pair['A'], pair['B']))
    elif pair['score'] == -1:
        BT_data.append((pair['B'], pair['A']))

metric = 'bart_BT_score'
df_sample[metric] = choix.ilsr_pairwise(len(df_sample), BT_data, alpha= 0.01)

# yearly aggregation
avgByYear = df_sample.groupby('year')[metric].mean().sort_index()
years = avgByYear.index.values.reshape(-1,1)
metric_score = avgByYear.values
# sermon-level regression for metric
slope, intercept, r, p, se = stats.linregress(df_sample['year'], df_sample[metric])
sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
print(f"{metric:<25} {slope:>10.4f} {r:>8.3f} {p:>8.3f} {sig}")
# get predictions
preds = slope * years.flatten() + intercept

# save plot
plt.figure()
plt.scatter(years, metric_score)
plt.plot(years, preds, color= 'red', linestyle= '--', label= 'Regression Line')
plt.xlabel('Year')
plt.ylabel('Mean Value')
plt.title(f'{metric} Over Time')
plt.grid(True, linestyle= '--', alpha= 0.5)
plt.text(
    0.05, 0.95,
    f"Slope: {slope:.4f}\nR²: {r**2:.3f}\np={p:.3f}",
    transform=plt.gca().transAxes,
    verticalalignment= 'top',
    bbox= dict(facecolor= 'white', alpha= 0.8)
)
plt.savefig("01_simple/output/figs/" + f"{metric}_over_time.png")
plt.close()


for _, row in df_sample.nlargest(3, 'simplicity')[['sermontext', 'simplicity', 'year']].iterrows():
    print(row['year'], row['simplicity'])
    print(row['sermontext'][:1000])
print()
for _, row in df_sample.nsmallest(3, 'simplicity')[['sermontext', 'simplicity', 'year']].iterrows():
    print(row['year'], row['simplicity'])
    print(row['sermontext'][:1000])
print()

for _, row in df_sample.nlargest(3, 'bart_BT_score')[['sermontext', 'bart_BT_score', 'year']].iterrows():
    print(row['year'], row['bart_BT_score'])
    print(row['sermontext'][:1000])
print()
for _, row in df_sample.nsmallest(3, 'bart_BT_score')[['sermontext', 'bart_BT_score', 'year']].iterrows():
    print(row['year'], row['bart_BT_score'])
    print(row['sermontext'][:1000])
print()
