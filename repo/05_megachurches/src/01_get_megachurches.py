import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

url = "https://hirr.hartfordinternational.edu/research/megachurch-database/megachurches-by-state/"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

rows = []

for i in range(1,68):
    url = f'https://hirr.hartfordinternational.edu/research/megachurch-database/megachurches-by-state/?sf_paged={i}'
    response = requests.get(url)
    table = BeautifulSoup(response.text, 'html.parser').find('table')

    skip_header = True if i > 1 else False

    for tr in table.find_all('tr'):
        if skip_header:
            skip_header = False
            continue

        cells = tr.find_all(['td', 'th'])
        row = [cell.get_text(strip= True) for cell in cells]
        rows.append(row)

df = pd.DataFrame(rows[1:], columns= rows[0])
df['City'] = df.apply(lambda row : row['City'][:re.search(r'\d', row['City']).start() - len(row['State'])], axis= 1)
df.to_csv('output/megachurches.csv', index= False)
