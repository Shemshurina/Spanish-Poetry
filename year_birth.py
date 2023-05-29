import html.parser
import re
import requests
from bs4 import BeautifulSoup
import os
import json


for filename in os.listdir(os.getcwd()):
    if filename.endswith('json'):
        with open(filename) as f:
            data = json.load(f)
            poet = data['meta']['author'].replace(' ', '_')

        url = 'https://en.wikipedia.org/wiki/' + poet
        user_agent = 'Mozilla/5.0'
        response = requests.get(url, headers={'User-Agent':user_agent})
        soup = BeautifulSoup(response.text, 'html5lib')

        poetContent = soup.find('div', {'class': 'mw-normal-catlinks'})
        data["meta"]["year_birth"] = None
        if poetContent != None:
            poetLines = poetContent.findAll('li')
            for line in poetLines:
                text = html.unescape(line.text)
                if 'births' in text and len(text) == 11:
                    data["meta"]["year_birth"] = re.findall("\d+", text)[0] 
  
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


