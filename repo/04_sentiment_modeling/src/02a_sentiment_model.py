import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# set progress configurations
tqdm.pandas()
pd.set_option('display.max_colwidth', None)

# load model and tokenizer
model_name = 'finiteautomata/bertweet-base-sentiment-analysis'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# load sentiment pipeline
sentiment_pipe = pipeline('sentiment-analysis', model= model, tokenizer= tokenizer, device= -1, truncation= True)

# load the data
df = pd.read_csv('intermediate/candidate_mentions.csv')
df_unique = pd.read_csv('intermediate/candidate_mentions_unique.csv')

# define label mapping
label_map = {
    'NEG': 'neg',
    'NEU': 'neu',
    'POS': 'pos'
}

# get sentiment labels
def get_sentiment_label(text):
    result = sentiment_pipe(text[:512])[0]
    label = label_map[result['label']]
    score = result['score']

    return label, score

df[['label', 'score']] = pd.DataFrame(df['text'].progress_apply(get_sentiment_label).tolist(), index= df.index)
df_unique[['label', 'score']] = pd.DataFrame(df_unique['text'].progress_apply(get_sentiment_label).tolist(), index= df_unique.index)

# save sentiments
df.to_csv('intermediate/neutral/main/sentiments.csv', index= False)
df_unique.to_csv('intermediate/neutral/unique/sentiments.csv', index= False)