import requests
from bs4 import BeautifulSoup as Bs
import csv
import re 
data = []

response = requests.get('https://onepiece.fandom.com/wiki/List_of_Canon_Characters')
if response.status_code == 200:
    content = Bs(response.text, 'html.parser')
    tables = content.find_all("table", class_='wikitable sortable')
    for t in tables[:2]:
        rows = t.tbody.find_all('tr')
        for r in rows: 
            colums = r.find_all('td')
            if colums:
                row_data = [c.text.strip() for c in colums ]
                # only charachters in the anime 
                if row_data[3]:
                    
                    if "(" in row_data[1].lower() :
                        val = re.findall(r".+?(?=\()", row_data[1].lower())
                        data.append(val[0])
                    else:
                        data.append(row_data[1].lower())


header = ['episode'] + data   
print(len(data)) 
with open('../Datasets/Canon_Charachters.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)


