import json
import os
import html.parser
import re
import requests
from bs4 import BeautifulSoup

def get_years(filename):
    with open(filename) as f:
        data = json.load(f)
    author = data["meta"]["author"].replace(' ', '_')
    title = data["meta"]["title"]
    repl = {'á': 'a',
            'é': 'e',
            'í': 'i', 'ï': 'i',
            'ó': 'o',
            'ú': 'u',}
    author = ''.join([repl[c] if c in repl else c for c in author])
    if author == "Antonio_Gala_Velasco":
        author = "Antonio_Gala"
    if author == "Juan_Luis_Panero_Blanc":
        author = "Juan_Luis_Panero"
    url = 'https://www.poesi.as/' + author + '.htm'
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent':user_agent})
    soup = BeautifulSoup(response.text, 'html5lib')
    base = soup.find('body')
    for link in BeautifulSoup(str(base), "html.parser").findAll("a"):
        if 'href' in link.attrs:
            text = html.unescape(link.text)
            if text.lower() == title.lower():
                poemlink = link['href']
                url2 = 'https://www.poesi.as/' + poemlink
                response2 = requests.get(url2, headers={'User-Agent':user_agent})
                soup2 = BeautifulSoup(response2.text, 'html5lib')
                lines = soup2.findAll('small')
                poeminfo = ''
                for l in lines:
                    poeminfo += html.unescape(l.text)
                poeminfo = poeminfo.replace(" \xa0 ", "")[1:]
                years = re.search(r"\d+\-\d+", poeminfo)
                year = ''
                book = ''
                if years:
                    year = years.group(0)
                    if re.search(r"\(\d+\-\d+\)", poeminfo):
                        book = poeminfo.replace(" ("+years.group(0)+")", "")
                    if re.search(r"\[\d+\-\d+\]", poeminfo):
                        book = poeminfo.replace(" ["+years.group(0)+"]", "")
                    if re.search(r"\s\d+\-\d+", poeminfo):
                        book = poeminfo.replace(" "+years.group(0), "")      
                elif len(re.findall(r"\d+", poeminfo))==1 and len(re.findall(r"\d+", poeminfo)[0])==4:
                    year = re.findall(r"\d+", poeminfo)[0]
                    book = poeminfo
                else:
                    year = "None"
                    book = poeminfo
                if len(year) == 4:
                    data["meta"]["year_from"] = year
                    data["meta"]["year_to"] = year
                else:
                    data["meta"]["year_from"] = year.split("-")[0]
                    data["meta"]["year_to"] = year.split("-")[1]
                data["meta"]["book_of_poems"] = book
            if "year_from" not in data["meta"].keys():
                data["meta"]["year_from"] = 0
                data["meta"]["year_to"] = 0
                data["meta"]["book_of_poems"] = "-"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

for filename in os.listdir(os.getcwd()):
    if filename.endswith('json'):
        get_years(filename)

