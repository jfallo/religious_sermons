import pandas as pd
import re, csv

# import sermons data
df = pd.read_stata('intermediate/sermons.dta')


# --- write time variables --- #

# define election dates in datetime format
election_dates = {
    1972: pd.to_datetime('1972-11-07'),
    1976: pd.to_datetime('1976-11-02'),
    1980: pd.to_datetime('1980-11-04'),
    1984: pd.to_datetime('1984-11-06'),
    1988: pd.to_datetime('1988-11-08'),
    1992: pd.to_datetime('1992-11-03'),
    1996: pd.to_datetime('1996-11-05'),
    2000: pd.to_datetime('2000-11-07'),
    2004: pd.to_datetime('2004-11-02'),
    2008: pd.to_datetime('2008-11-04'),
    2012: pd.to_datetime('2012-11-06'),
    2016: pd.to_datetime('2016-11-08'),
    2020: pd.to_datetime('2020-11-03'),
    2024: pd.to_datetime('2024-11-05')
}
election_months = [
    '1972-11', 
    '1976-11', 
    '1980-11', 
    '1984-11', 
    '1988-11', 
    '1992-11', 
    '1996-11', 
    '2000-11', 
    '2004-11', 
    '2008-11', 
    '2012-11', 
    '2016-11', 
    '2020-11', 
    '2024-11']
election_months = pd.to_datetime(election_months)
election_years = [1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020]

# convert contribution monthly to datetime format
df['contribution_monthly'] = pd.to_datetime(df['contribution_monthly'], errors= 'coerce')

# helper functions for time calculations
def times_to_election(sermon, election_dates, year= None):
    election_date = election_dates.get(year)

    if election_date is None:
        return pd.NA, pd.NA
    
    days = (election_date - sermon['date']).days
    weeks = (election_date - sermon['date']).days // 7
    
    return days, weeks 

def times_to_nearest_election(sermon, election_dates):
    nearest_election = None
    min_diff = float('inf')

    for year, date in election_dates.items():
        days_diff = (date - sermon['date']).days

        if abs(days_diff) < abs(min_diff):
            nearest_election = year
            min_diff = days_diff
            weeks_diff = days_diff // 7
            months_diff = int(12 * (sermon['date'].year - date.year) + (sermon['date'].month - date.month))
    
    if nearest_election is None:
        return pd.NA, pd.NA, pd.NA, pd.NA

    return min_diff, weeks_diff, months_diff, nearest_election

def get_election_tuesday_date(year):
    start_date = pd.to_datetime(f'{year}-11-02')
    end_date = pd.to_datetime(f'{year}-11-08')

    for day in range((end_date - start_date).days + 1):
        cur_date = start_date + pd.Timedelta(days= day)
        
        if cur_date.weekday() == 1:
            return cur_date

def times_to_nearest_election_tuesday(sermon):
    prev_year_tuesday = get_election_tuesday_date(sermon['date'].year - 1)
    cur_year_tuesday = get_election_tuesday_date(sermon['date'].year)

    prev_year_diff = (prev_year_tuesday - sermon['date']).days
    cur_year_diff = (cur_year_tuesday - sermon['date']).days

    if abs(prev_year_diff) < abs(cur_year_diff):
        return prev_year_diff, prev_year_diff // 7
    
    return cur_year_diff, cur_year_diff // 7

# write time variables
df['date'] = pd.to_datetime(df['date'], errors= 'coerce')

df[[
    'days_to_nearest_election', 
    'weeks_to_nearest_election', 
    'months_to_nearest_election', 
    'nearest_election'
]] = df.apply(times_to_nearest_election, axis= 1, election_dates= election_dates, result_type= 'expand')

df[[
    'days_to_nearest_tuesday', 
    'weeks_to_nearest_tuesday'
]] = df.apply(times_to_nearest_election_tuesday, axis= 1, result_type= 'expand')

for year, election_date in election_dates.items():
    df[[
        f'days_to_{year}_election', 
        f'weeks_to_{year}_election'
    ]] = df.apply(times_to_election, axis= 1, election_dates= election_dates, year= year, result_type= 'expand')


# --- clean sermon texts --- # 

# helper functions for cleaning texts
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

def clean_text(text):
    # ignore empty and non-strings
    if not isinstance(text, str) or text.strip() == '':
        return text
    
    # protect links, urls, and emails
    text, urls, emails = protect_links(text)
    # protect ellipsis
    text = text.replace('...', '__ELLIPSIS__')

    # replace • with ,
    text = re.sub('•', ',', text)
    # replace ’ with '
    text = re.sub('’', "'", text)
    # replace all characters except alphanumeric and . , : ; ? ! ' _ @ / - with space
    text = re.sub(r"[^a-zA-Z0-9.,:;?!'_@\/\-]", ' ', text)

    # fix spacing (only single space)
    text = re.sub(r'([!?])([A-Z])', r'\1 \2', text)
    text = re.sub(r'\s{2,}', ' ', text)

    # add space after punctuation if missing
    text = re.sub(r'([^\s.?!])', r'\1', text)

    # restore links, urls, and emails
    text = restore_links(text, urls, emails)
    # restore ellipses
    text = text.replace('__ELLIPSIS__', '...')

    # trim whitespace around lines and collapse 3+ newlines to 2
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

# clean texts
df['sermontext'] = df['sermontext'].where(df['sermontext'].isna(), df['sermontext'].astype(str).apply(clean_text))
# clean column names
df.columns = df.columns.str.strip()
# clean string columns
df = df.apply(lambda x : x.str.strip() if x.dtype == 'object' else x)
# save sermons data
df.to_csv('output/sermons.csv', encoding= 'utf-8', index= True, quoting= csv.QUOTE_ALL)