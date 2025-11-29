import pandas as pd
import csv
import matplotlib.pyplot as plt

# load data (replace all '/main' with '/unique' to change)
df = pd.read_csv('intermediate/neutral/unique/sentiments.csv')
df_neg = df[df['label'] == 'neg']
df_neu = df[df['label'] == 'neu']
df_pos = df[df['label'] == 'pos']

# define candidate names and associated political party
party_map = {
    'Clinton': 'Democrat',
    'Bill Clinton': 'Democrat',
    'Kerry': 'Democrat',
    'Obama': 'Democrat',
    'Hillary Clinton': 'Democrat',
    'Biden': 'Democrat',
    'Bush': 'Republican',
    'McCain': 'Republican',
    'Romney': 'Republican',
    'Trump': 'Republican'
}
candidate_names = list(party_map.keys())
dems = [name for name in candidate_names if party_map.get(name, '') == 'Democrat']
reps = [name for name in candidate_names if party_map.get(name, '') == 'Republican']

# define object containing sentiment data for each candidate
sentiment_data = [
    {
        'name': name,
        'party': party_map.get(name, ''),
        'mentions': 1e-8,
        'pos_mentions': 1e-8,
        'neu_mentions': 1e-8,
        'neg_mentions': 1e-8,
        'pos_percentage': 1e-8,
        'neu_percentage': 1e-8,
        'neg_percentage': 1e-8
    }
    for name in candidate_names
]

sentiments_by_name = []

# get sentiment data for each candidate
for entry in sentiment_data:
    name = entry['name']

    # total mentions
    for text, label, score in zip(df['text'], df['label'], df['score']):
        if name.lower() in text.lower():
            entry['mentions'] += 1
            sentiments_by_name.append([name, text, label, score])

    # mentions with positive sentiment
    for text, score in zip(df_pos['text'], df_pos['score']):
        if name.lower() in text.lower():
            entry['pos_mentions'] += 1
    entry['pos_percentage'] = round(100 * entry['pos_mentions'] / entry['mentions'], 2)

    # mentions with neutral sentiment
    for text in df_neu['text']:
        if name.lower() in text.lower():
            entry['neu_mentions'] += 1
    entry['neu_percentage'] = round(100 * entry['neu_mentions'] / entry['mentions'], 2)

    # mentions with negative sentiment
    for text, score in zip(df_neg['text'], df_neg['score']):
        if name.lower() in text.lower():
            entry['neg_mentions'] += 1
    entry['neg_percentage'] = round(100 * entry['neg_mentions'] / entry['mentions'], 2)

df_sentiments_by_name = pd.DataFrame(sentiments_by_name, columns= ['name', 'text', 'sentiment', 'score'])

# rankings
rankings = [[item['name'], item['party'], int(item['mentions']), int(item['neu_mentions']), int(item['pos_mentions']), int(item['neg_mentions']), item['neu_percentage'], item['pos_percentage'], item['neg_percentage'], round(item['pos_percentage'] - item['neg_percentage'], 2)] for item in sentiment_data]
rankings = sorted(rankings, key= lambda x : x[9], reverse= True)
for i in range(len(rankings)):
    rankings[i] = [i+1] + rankings[i]

df_rankings = pd.DataFrame(rankings, columns= ['Ranks', 'Name', 'Party', 'Total Mentions', 'Neu Mentions', 'Pos Mentions', 'Neg Mentions', 'Neu Mentions %', 'Pos Mentions %', 'Neg Mentions %', 'Pos - Neg %'])
df_rankings.to_csv('output/neutral/unique/rankings.csv', index= False)

# most negative and most positive mentions for each candidate
top_mentions = []
# random negative and random positive mentions for each candidate
rand_mentions = []

for name in candidate_names:
    df_name = df_sentiments_by_name[df_sentiments_by_name['name'] == name]
    
    for sentiment in ['pos', 'neu', 'neg']:
        df_sentiment = df_name[df_name['sentiment'] == sentiment]
        top_5 = df_sentiment.nlargest(5, 'score')
        rand_5 = df_sentiment.sample(n= 5, random_state= 42) if len(df_sentiment) >= 5 else df_sentiment
        
        top_mentions.append(top_5)
        rand_mentions.append(rand_5)

df_top_mentions = pd.concat(top_mentions)
cols = [col for col in df_top_mentions.columns if col != 'text'] + ['text']
df_top_mentions = df_top_mentions[cols]
df_top_mentions = df_top_mentions.sort_values(by= ['name', 'sentiment', 'score'], ascending= [True, True, False])
df_top_mentions.to_csv('output/neutral/unique/top_mentions.csv', quoting= csv.QUOTE_ALL, index= False)

df_rand_mentions = pd.concat(rand_mentions)
cols = [col for col in df_rand_mentions.columns if col != 'text'] + ['text']
df_rand_mentions = df_rand_mentions[cols]
df_rand_mentions = df_rand_mentions.sort_values(by= ['name', 'sentiment'], ascending= [True, True])
df_rand_mentions.to_csv('output/neutral/unique/rand_mentions.csv', quoting= csv.QUOTE_ALL, index= False)

# make plots
pos_counts = [entry['pos_mentions'] for entry in sentiment_data]
neg_counts = [entry['neg_mentions'] for entry in sentiment_data]
neu_counts = [entry['neu_mentions'] for entry in sentiment_data]

fig, ax = plt.subplots(figsize= (12, 6))

ax.bar(candidate_names, pos_counts, color= 'skyblue', label= 'Positive')
ax.bar(candidate_names, neu_counts, bottom= pos_counts, color= 'lightgray', label= 'Neutral')
ax.bar(candidate_names, neg_counts, bottom= [p + n for p, n in zip(pos_counts, neu_counts)], color= 'salmon', label= 'Negative')

ax.axvline(x= len(dems) - 0.5, color= 'black', linestyle= '--', linewidth= 1)
ax.text(
    x= (len(dems) - 1) / 2, y= -0.15, s= 'Democrats',
    transform= ax.get_xaxis_transform(),
    ha= 'center', va= 'top', fontsize= 10, fontweight= 'bold'
)
ax.text(
    x= (len(dems) + len(dems) + len(reps) - 1) / 2, y= -0.15, s= 'Republicans',
    transform= ax.get_xaxis_transform(),
    ha= 'center', va= 'top', fontsize= 10, fontweight= 'bold'
)

ax.set_title('Sentiment Counts by Candidate')
ax.set_xlabel('Candidate')
ax.set_ylabel('Mentions')
ax.legend()
plt.xticks(rotation= 45)
plt.tight_layout()
plt.savefig('output/neutral/unique/figs/counts.png', dpi= 300)
plt.close()