import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import csv, os


metrics = [
    {
        'name': 'complexity',
        'labels': [
            "complex academic or theological language, abstract concepts, dense sentence structure, sophisticated vocabulary",
            "simple plain language, narrative storytelling, conversational tone, easy-to-follow sentences"
        ]
    },
    {
        'name': 'polarization',
        'labels': [
            "polarized us-vs-them language, condemning outsiders, culture-war framing, moral blame",
            "inclusive language, welcoming, emphasizing unity, shared dignity, openness to all people"
        ]
    },
    {
        'name': 'confidence',
        'labels': [
            "high-confidence language, moral certainty, definitive truth claims, authoritative tone",
            "low-confidence language, hedging and uncertainty, cautious speculation, tentative interpretation"
        ]
    },
    {
        'name': 'scope',
        'labels': [
            "universalist language emphasizing all people, global inclusion, everyone belongs",
            "communal language addressing a local group, congregation-focused, shared community identity"
        ]
    },
    {
        'name': 'emotion',
        'labels': [
            "emotional language, engaging, relatable storytelling, expressing fear, grief, joy, pain, personal vulnerability",
            "emotionally neutral analytical language, detached explanation, academic or informational tone"
        ]
    },
    {
        'name': 'reasoning',
        'labels': [
            "evidence-based reasoning citing scripture, facts, history, statistics, or textual proof",
            "intuitive reasoning based on personal experience, spiritual feeling, impression, or common sense"
        ]
    }
]


if not os.path.exists("output/sermons_deberta.csv"):
    df = pd.read_csv("input/sermons.csv")
    df = df.dropna(subset= ['sermontext']).reset_index(drop= True)
    df = df[df['sermontext'].str.len() >= 1500].reset_index(drop= True)

    samples = (
        df.groupby('year')
        .apply(lambda x : x.sample(min(len(x), 200), random_state= 42))
        .index.get_level_values(1)
    )
    df_sample = df.loc[samples].reset_index(drop= True)


    tqdm.pandas()
    classifier = pipeline('zero-shot-classification', model= 'MoritzLaurer/deberta-v3-large-zeroshot-v2.0')


    def get_score(text, labels):
        tokenizer = classifier.tokenizer
        tokens = tokenizer.encode(text, add_special_tokens= False)
        chunk_size = 768
        chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens), chunk_size)]
        chunk_texts = [
            tokenizer.decode(chunk, skip_special_tokens= True, clean_up_tokenization_spaces= True)
            for chunk in chunks
        ]
        results = classifier(chunk_texts, candidate_labels= labels, truncation= True, max_length= 1024, batch_size= 8)
        scores = [result['scores'][result['labels'].index(labels[0])] for result in results]
            
        return sum(scores) / len(scores)
    
    for metric in metrics:
        if metric['name'] == 'polarization':
            print(f"Running {metric['name']} classification...")
            df_sample[metric['name'] + '_score'] = df_sample['sermontext'].progress_apply(get_score, args= ([metric['labels'][0], metric['labels'][1]],))
            df_sample.to_csv("output/sermons_deberta.csv", index= False, quoting= csv.QUOTE_ALL)
