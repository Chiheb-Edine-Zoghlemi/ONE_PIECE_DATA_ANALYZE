import requests
from bs4 import BeautifulSoup as Bs
import re 
import csv
data = []

pools_dates = [1999,2002,2006,2009,2015,2017,2021]
important_cast = ['Monkey D. Luffy','Roronoa Zoro','Nami','Usopp','Sanji','Tony Tony Chopper','Nico Robin','Franky','Brook','Jinbe']
response = requests.get('https://onepiece.fandom.com/wiki/Popularity_Polls')
if response.status_code == 200:
    content = Bs(response.text, 'html.parser')
    table = content.find("table", class_='wikitable sortable')
    rows = table.tbody.find_all('tr')
    total_data = [c.text.strip() for c in rows[-1].find_all('td') ]
    for r in rows[1:-1]: 
        colums = r.find_all('td')
        row_data = [c.text.strip() for c in colums ]
        if row_data[0] in important_cast:
            for i,d in enumerate(pools_dates):
                if row_data[i+1] :
                    val = re.findall(r"\d+", row_data[i+1])
                    rank = val[0] if  len(val)> 0 else 0
                    votes = val[1] if len(val)> 1 else 0
                    data.append([row_data[0],int(rank),int(votes),d,int(total_data[i+1].replace('+',''))])
                else : 
                    data.append([row_data[0],0,0,d,int(total_data[i+1].replace('+',''))])

header = ['Character', 'Rank', 'Votes','Pool year', 'Total nomber of votes']           
with open('..\Datasets\Popularity.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    


