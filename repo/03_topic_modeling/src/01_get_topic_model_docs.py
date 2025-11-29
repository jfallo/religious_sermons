import pandas as pd
from openai import OpenAI
import re, csv, ast

# load sermon texts
df = pd.read_csv("input/sermons.csv")
# df where all sermons are within 4 week window to an election tuesday
df_tuesday = df.copy().dropna(subset= ['weeks_to_nearest_tuesday'])
df_tuesday = df_tuesday[(df_tuesday['weeks_to_nearest_tuesday'] >= -4) & (df_tuesday['weeks_to_nearest_tuesday'] <= 4)]
# df where all sermons are within 4 week window to an election
df_election = df_tuesday.copy().dropna(subset= ['weeks_to_nearest_election'])
df_election = df_election[(df_election['weeks_to_nearest_election'] >= -4) & (df_election['weeks_to_nearest_election'] <= 4)]

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

# helper functions for getting docs for topic modeling
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

def get_docs_manual(df, label, keywords):
    # pattern for detecting keyword
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b'

    # extract sentences with keywords
    docs = []

    for index, date, tuesday, weeks, text in zip(df['index'], df['date'], df['weeks_to_nearest_tuesday'], df['weeks_to_nearest_election'], df['sermontext']):
        doc = str(text)

        # protect links, urls, and emails
        doc, urls, emails = protect_links(doc)
        # protect ellipsis
        doc = doc.replace('...', '__ELLIPSIS__')

        # get sentences
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', doc)
        sentences = [s.replace('\t', ' ').strip() for s in sentences if s.strip()]

        # restore links, urls, and emails in sentences
        sentences = [restore_links(s, urls, emails) for s in sentences]
        # restore ellipses in sentences
        sentences = [s.replace('__ELLIPSIS__', '...') for s in sentences]

        # capture sentence blocks containing a keyword
        prev_sentence = ""
        cur_sentence = ""
        
        for next_sentence in sentences:
            if re.search(pattern, cur_sentence, flags= re.IGNORECASE):
                if re.search(pattern, next_sentence, flags= re.IGNORECASE):
                    prev_sentence = prev_sentence + ". " + cur_sentence
                    cur_sentence = next_sentence
                else:
                    docs.append([index, date, tuesday, weeks, prev_sentence + ". " + cur_sentence + ". " + next_sentence + ".", text])

                    prev_sentence = cur_sentence
                    cur_sentence = next_sentence
            else:
                prev_sentence = cur_sentence
                cur_sentence = next_sentence

        if re.search(pattern, cur_sentence, flags= re.IGNORECASE):
            docs.append([index, date, tuesday, weeks, prev_sentence + ". " + cur_sentence + ".", text])

    # convert to dataframe
    df_with_docs = pd.DataFrame(docs, columns= ['index', 'date', 'weeks_to_nearest_tuesday', 'weeks_to_nearest_election', 'doc', 'sermontext'])
    df_with_docs = df_with_docs.dropna().drop_duplicates()
    df_with_docs.to_csv(f"intermediate/pattern_matching/{label}_docs.csv", index= False, quoting= csv.QUOTE_ALL)

    return df_with_docs

def get_docs_from_gpt(df, label):
    docs = []

    client = OpenAI()

    for index, date, tuesday, weeks, text in zip(df['index'], df['date'], df['weeks_to_nearest_tuesday'], df['weeks_to_nearest_election'], df['sermontext']):
        doc = str(text)

        prompt = (
            "You are an expert at identifying discussion of United States politics.\n"
            "\n"
            "OUTPUT FORMAT (CRITICAL):\n"
            "- Return only a valid Python list of strings.\n"
            "- The list must be directly parsable by ast.literal_eval in Python.\n"
            "- No extra text, no explanations, no markdown formatting.\n"
            "- Each string must contain one or more complete sentences.\n"
            "\n"
            "TASK:\n"
            "- Carefully analyse the input text and extract all discussion about American presidential elections, presidential candidates, and voting motivations "
            "(e.g. environmental, social, economic, financial factors; a candidate or political party's ideologies; law and policy).\n"
            "- Group consecutive sentences together into a single string if they discuss the same topic or are an ongoing thought.\n"
            "- If no sentences are relevant, return an empty list: [].\n"
            "- Carefully analyse the text, do not miss any potential discussion.\n"
            "\n"
            "EXAMPLES:\n"
            "Input: 'A lot of topics were discussed. The pastor mentioned the 2020 election. He said to vote for Trump. "
            "He also talked about prayer. He said they must be pro-life to save the unborn.'\n"
            "Output: ['The pastor mentioned the 2020 election. He said to vote for Trump.', "
            "'He said they must be pro-life to save the unborn.']\n"
            "\n"
            "Input: 'The pastor spoke only about prayer and thanksgiving.'\n"
            "Output: []\n"
        )
        response = client.chat.completions.create(
            model= "gpt-4o",
            messages= [
                {"role": "system", "content": prompt},
                {"role": "user", "content": doc}
            ],
            temperature= 0.3
        )
        content = response.choices[0].message.content.strip()

        try:
            sentences = ast.literal_eval(content)

            if isinstance(sentences, list):
                for sentence in sentences:
                    docs.append([index, date, tuesday, weeks, sentence, text])
        except Exception:
            docs.extend([])

    df_with_docs = pd.DataFrame(docs, columns= ['index', 'date', 'weeks_to_nearest_tuesday', 'weeks_to_nearest_election', 'doc', 'sermontext'])
    df_with_docs = df_with_docs.dropna().drop_duplicates()
    df_with_docs.to_csv(f"intermediate/gpt/{label}_docs.csv", index= False, quoting= csv.QUOTE_ALL)

    return df_with_docs

get_docs_manual(df, 'all', candidate_keywords + election_keywords)
get_docs_manual(df_tuesday, 'tuesday', candidate_keywords + election_keywords)
get_docs_manual(df_election, 'election', candidate_keywords + election_keywords)
