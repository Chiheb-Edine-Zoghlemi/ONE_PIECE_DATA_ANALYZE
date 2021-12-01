from pandas.io.formats import style
import requests
from bs4 import BeautifulSoup as Bs
import csv
import pandas as pd
import re
data = []
charachters = []
charachters = pd.read_csv('../Datasets/Canon_Charachters.csv').columns.tolist()
for  i in range(1,1001):
    print(f'[ PARSING EPISODE {i} ]')
    response = requests.get(f'https://onepiece.fandom.com/wiki/Episode_{i}')
    items = []
    if response.status_code == 200:
        content = Bs(response.text, 'html.parser')
        tags = content.find_all(True)
        for x,tag in enumerate(tags):
            if  tag.text.strip() == "Characters in Order of Appearance" :
                if tags[x+1].name.strip() == 'ul':
                    items = tags[x+1].find_all('a')
                    break
        
        if items:
            rw_data = [0 for i in range(len(charachters))]
            rw_data[0]=i
            print(f'[ Number of characters is {len(items)} ]')
            for item in items:
                charachter = item.text.strip().lower()
                if "(" in charachter :
                        val = re.findall(r".+?(?=\()", charachter)
                        charachter =val[0]
                if charachter in charachters:
                    j=charachters.index(charachter)
                    rw_data[j]=1
            data.append(rw_data)
        else:
            tags = content.find('div',{'style':'width:auto; height:230px; overflow:auto; margin-bottom:3px; padding-left:0.5em; border:1px solid #AAAAAA; -moz-border-radius-topleft:0.5em; -webkit-border-top-left-radius:0.5em; border-top-left-radius:0.5em;'})
            ul = tags.find('ul')
            items = ul.find_all('a')
            rw_data = [0 for i in range(len(charachters))]
            rw_data[0]=i
            print(f'[ Number of characters is {len(items)} ]')
            if items:
                for item in items:
                    charachter = item.text.strip().lower()
                    if "(" in charachter :
                        val = re.findall(r".+?(?=\()", charachter)
                        charachter =val[0]
                    if charachter in charachters:
                        j=charachters.index(charachter)
                        rw_data[j]=1
                data.append(rw_data)
    else:
        print(f'[ Fail to request ep {i}]')
    
        


with open('../Datasets/Canon_Charachters.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(charachters)
        writer.writerows(data)


