import pandas as pd
import re

# import sermons data
df = pd.read_csv('input/sermons.csv')
# replace misspelling of Hillary Clinton and Barack
df['sermontext'] = df['sermontext'].str.replace(r'(?i)hilary clinton', 'Hillary Clinton', regex= True)
df['sermontext'] = df['sermontext'].str.replace(r'(?i)barak', 'Barack', regex= True)

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
    "politic", "politics", "political", "politically", "politician", "politicians",  
    "elect", "elects", "elected", "electing", "election", "elections", 
    "nominate", "nominates", "nominated", "nominating", "nomination", "nominations", 
    "poll", "polls", "polling", "pollster", "ballot", "ballots", 
    "democratic", "republic", "democrat", "democrats", "republican", "republicans"
]
election_keywords = sorted(election_keywords, key= len, reverse= True)
government_keywords = [
    "office", "govern", "government", "federal", "state", "states", 
    "nation", "democracy", "policy", "policies", "law", "laws", 
    "judicial", "court", "legislative", "legislation", 
    "constitution", "constitutional", "amendment", "amendments"
]
government_keywords = sorted(government_keywords, key= len, reverse= True)

# helper functions for counts 
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

def count_keywords(text, keywords):
    # pattern for detecting keyword
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b'

    # find all keyword matches in the text
    matches = re.findall(pattern, text, flags= re.IGNORECASE)

    return len(matches)

# write mention variables 
mask_has_text = df['sermontext'].notna()

df.loc[mask_has_text, 'election_mentions'] = df.loc[mask_has_text, 'sermontext'].apply(
    lambda text : count_keywords(str(text), election_keywords + candidate_keywords)
)
df.loc[mask_has_text, 'election_word_count'] = df.loc[mask_has_text, 'sermontext'].apply(
    lambda text : count_keywords(str(text), election_keywords)
)
df.loc[mask_has_text, 'candidate_mentions'] = df.loc[mask_has_text, 'sermontext'].apply(
    lambda text : count_keywords(str(text), candidate_keywords)
)
df.loc[mask_has_text, 'government_word_count'] = df.loc[mask_has_text, 'sermontext'].apply(
    lambda text : count_keywords(str(text), government_keywords)
)

# save results
df.to_csv('output/sermons.csv')
