import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# load data
df_election_with_docs_gpt = pd.read_csv("intermediate/gpt/election_docs.csv")
df_election_with_docs_pattern_matching = pd.read_csv("intermediate/pattern_matching/election_docs.csv")

# define keywords
candidate_keywords = [
    'Bill Clinton', 'Hillary Clinton', 'Clinton', 
    'George W. Bush', 'George Bush', 'President Bush', 'Mr. Bush', 
    'Barack Obama', 'Obama', 
    'Joe Biden', 'Biden', 
    'John McCain', 'McCain', 
    'Mitt Romney', 'Romney', 
    'Donald Trump', 'Trump', 
    'Bernie Sanders', 'Kamala Harris', 'Al Gore'
]
election_keywords = [
    "vote", "votes", "voted", "voting", "voter", "voters", "candidate", "candidates", 
    "campaign", "campaigns", "campaigned", "campaigning", 
    "president", "presidents", "presidential", "administration", 
    "senate", "senator", "senators", "congress", "congressman", "congresswoman", "congressmen", "congresswomen", 
    "politic", "politics", "political", "politician", "politicians", "policy", "policies", 
    "elect", "elects", "elected", "electing", "election", "elections", 
    "nominate", "nominates", "nominated", "nominating", "nomination", "nominations", 
    "poll", "polls", "polling", "pollster", "ballot", "ballots", 
    "democracy", "democratic", "republic", "democrat", "democrats", "republican", "republicans", "independent"
]
election_keywords = sorted(election_keywords, key= len, reverse= True)
keywords = candidate_keywords + election_keywords

# helper functions for getting sentences
def protect_links(text):
    # replace URLs and emails with placeholders
    urls = re.findall(r'(https?://\S+|www\.\S+)', text)
    emails = re.findall(r'\S+@\S+\.\S+', text)
    
    for i, url in enumerate(urls):
        text = text.replace(url, f'__URL_{i}__')
    for j, email in enumerate(emails):
        text = text.replace(email, f'__EMAIL_{j}__')
        
    return text, urls, emails

def restore_links(text, urls, emails):
    # restore URLs and emails from placeholders
    for i, url in enumerate(urls):
        text = text.replace(f'__URL_{i}__', url)
    for j, email in enumerate(emails):
        text = text.replace(f'__EMAIL_{j}__', email)

    return text

def get_sentences(docs):
    all_sentences = []

    for doc in docs:
        # protect links, urls, and emails
        doc, urls, emails = protect_links(doc)
        # protect ellipsis
        doc = doc.replace('...', '__ELLIPSIS__')

        # get sentences
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', doc)
        sentences = [s.strip() for s in sentences if s.strip()]

        # restore links, urls, and emails in sentences
        sentences = [restore_links(s, urls, emails) for s in sentences]
        # restore ellipses in sentences
        sentences = [s.replace('__ELLIPSIS__', '...') for s in sentences]

        # add to list of all sentences
        all_sentences += sentences

    return all_sentences

# only interested in sentences that mention keywords
def clean_sentences(sentences, keywords):
    cleaned_sentences = []

    # pattern for detecting keyword
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b'

    for sentence in sentences:
        if re.search(pattern, sentence, flags= re.IGNORECASE):
            cleaned_sentences.append(sentence)
    
    return set(cleaned_sentences)

docs_gpt = df_election_with_docs_gpt['doc'].tolist()
sentences_gpt = get_sentences(docs_gpt)
sentences_gpt = clean_sentences(sentences_gpt, keywords)

docs_pattern_matching = df_election_with_docs_pattern_matching['doc'].tolist()
sentences_pattern_matching = get_sentences(docs_pattern_matching)
sentences_pattern_matching = clean_sentences(sentences_pattern_matching, keywords)

intersection = sentences_gpt & sentences_pattern_matching
overlap_gpt_in_pattern = len(intersection) / len(sentences_gpt)
overlap_pattern_in_gpt = len(intersection) / len(sentences_pattern_matching)
similarity_matrix = np.array([
    [1.0, overlap_gpt_in_pattern],
    [overlap_pattern_in_gpt, 1.0]
])

labels = ['GPT Sentences', 'Pattern Matching Sentences']
fig, ax = plt.subplots(figsize= (6,5))
im = ax.imshow(similarity_matrix, cmap= 'Purples', vmin= 0, vmax= 1)

for i in range(2):
    for j in range(2):
        ax.text(j, i, f"{similarity_matrix[i,j]:.2f}",
                ha= "center", va= "center", color= "black", fontsize= 12)

ax.set_xticks(np.arange(2))
ax.set_yticks(np.arange(2))
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)
plt.title("2×2 Sentence Overlap Between GPT and Pattern Matching")
plt.colorbar(im, fraction= 0.046, pad= 0.04)
plt.tight_layout()
plt.show()

print(f"Count (GPT): {len(sentences_gpt)}")
print(f"Overlap (GPT in Pattern Matching): {overlap_gpt_in_pattern:.2%}")
print(f"Count (Pattern Matching): {len(sentences_pattern_matching)}")
print(f"Overlap (Pattern Matching in GPT): {overlap_pattern_in_gpt:.2%}")
print(f"Total shared sentences: {len(intersection)} / {len(sentences_gpt | sentences_pattern_matching)}")