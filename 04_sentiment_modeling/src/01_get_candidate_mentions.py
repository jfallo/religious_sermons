import pandas as pd
import re, csv

# helper functions for scanning texts
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

# load sermon texts
df = pd.read_csv('input/sermons.csv')
# only keep sermons within 4 week window
df = df[(df['weeks_to_nearest_election'] >= -4) & (df['weeks_to_nearest_election'] <= 4)]
# only keep these features
df = df[['index', 'sermontext']]
# drop mentions of Dr. Robert Clinton and Dr. Timothy Clinton
df = df[~df['sermontext'].str.contains(r'Dr\. Robert Clinton | Dr\. Timothy Clinton | Dr\. Clinton', case= False, na= False)]
# drop sermon grabbed from 'trumpet'
df = df[~df['sermontext'].str.contains(r'trumpet', case= False, na= False)]

# define candidate keywords
candidate_keywords = [
    'Bill Clinton', 'Hillary Clinton', 'Clinton', 
    'George W. Bush', 'George Bush', 'President Bush', 'Mr. Bush', 
    'Barack Obama', 'Obama', 
    'Joe Biden', 'Biden', 
    'John McCain', 'McCain', 
    'Mitt Romney', 'Romney', 
    'Donald Trump', 'Trump'
]
candidate_keywords_ext = candidate_keywords + ['Bush']
candidate_map = {
    'clinton': 'clinton',
    'bill clinton': 'bill clinton',
    'hillary clinton': 'hillary clinton',
    'kerry': 'kerry',
    'john kerry': 'kerry',
    'obama': 'obama',
    'barack obama': 'obama',
    'biden': 'biden',
    'joe biden': 'biden',
    'bush': 'bush',
    'george w. bush': 'bush',
    'george bush': 'bush',
    'president bush': 'bush',
    'mr. bush': 'bush',
    'mccain': 'mccain',
    'john mccain': 'mccain',
    'romney': 'romney',
    'mitt romney': 'romney',
    'trump': 'trump',
    'donald trump': 'trump',
    'sanders': 'sanders',
    'bernie sanders': 'sanders'
}

# extract sentences with candidate mentions
candidate_mentions = []
# extract sentences with exactly one candidate mentioned
candidate_mentions_unique = []
# pattern for detecting candidate keyword
pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in candidate_keywords) + r')\b'
pattern_unique = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in candidate_keywords_ext) + r')\b'

for text in df['sermontext']:
    text = str(text)

    # protect links, urls, and emails
    text, urls, emails = protect_links(text)
    # protect ellipsis
    text = text.replace('...', '__ELLIPSIS__')

    # get sentences
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    sentences = [s.replace('\t', ' ').strip() for s in sentences if s.strip()]

    # restore links, urls, and emails in sentences
    sentences = [restore_links(s, urls, emails) for s in sentences]
    # restore ellipses in sentences
    sentences = [s.replace('__ELLIPSIS__', '...') for s in sentences]

    # capture sentence containing candidate keyword and its surrounding sentences
    prev_sentence = ""
    cur_sentence = ""
    
    for next_sentence in sentences:
        if re.search(pattern, cur_sentence, flags= re.IGNORECASE):
            candidate_mentions.append(prev_sentence + ". " + cur_sentence + ". " + next_sentence + ".")
            candidates_mentioned = set(re.findall(pattern_unique, prev_sentence + ". " + cur_sentence + ". " + next_sentence + ".", flags= re.IGNORECASE))
            candidates_mentioned = set(candidate_map[candidate.lower()] for candidate in candidates_mentioned)
            
            if len(candidates_mentioned) == 1:
                candidate_mentions_unique.append(prev_sentence + ". " + cur_sentence + ". " + next_sentence + ".")
            if candidates_mentioned == {'clinton', 'bill clinton'}:
                candidate_mentions_unique.append(prev_sentence + ". " + cur_sentence + ". " + next_sentence + ".")
            if candidates_mentioned == {'clinton', 'hillary clinton'}:
                candidate_mentions_unique.append(prev_sentence + ". " + cur_sentence + ". " + next_sentence + ".")

        prev_sentence = cur_sentence
        cur_sentence = next_sentence

    if re.search(pattern, cur_sentence, flags= re.IGNORECASE):
        candidate_mentions.append(prev_sentence + ". " + cur_sentence + ".")
        candidates_mentioned = set(re.findall(pattern_unique, prev_sentence + ". " + cur_sentence + ".", flags= re.IGNORECASE))
        candidates_mentioned = set(candidate_map[candidate.lower()] for candidate in candidates_mentioned)
            
        if len(candidates_mentioned) == 1:
            candidate_mentions_unique.append(prev_sentence + ". " + cur_sentence + ".")
        if candidates_mentioned == {'clinton', 'hillary clinton'}:
            candidate_mentions_unique.append(prev_sentence + ". " + cur_sentence + ".")
        if candidates_mentioned == {'clinton', 'bill clinton'}:
            candidate_mentions_unique.append(prev_sentence + ". " + cur_sentence + ".")

# convert to dataframe
df = pd.DataFrame(candidate_mentions, columns= ['text'])
df_unique = pd.DataFrame(candidate_mentions_unique, columns= ['text'])
# save candidate mentions data
df.to_csv('intermediate/candidate_mentions.csv', quoting= csv.QUOTE_ALL, index= False)
df_unique.to_csv('intermediate/candidate_mentions_unique.csv', quoting= csv.QUOTE_ALL, index= False)