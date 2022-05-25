import requests
from bs4 import BeautifulSoup
import re
import html5lib
import html.parser
import wikipediaapi
import urllib.request

#creating .txt files with poems for a poet
def get_poems(poet_name):
    url = 'https://www.poeticous.com/' + poet_name
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent':user_agent})
    soup = BeautifulSoup(response.text, 'html5lib')
    text = soup.get_text('\n', strip='True')
    poems = []
    for poem in re.findall('\/'+poet_name+'\/[a-zA-Z0-9%-]+', text):
        if poem not in poems:
            poems.append(poem)
    if poems != []:
        for poem in poems:
            poemurl = 'https://www.poeticous.com' + poem
            poempage = urllib.request.Request(poemurl, headers={'User-Agent':user_agent})
            poemsauce = urllib.request.urlopen(poempage).read()
            poemsoup = BeautifulSoup(poemsauce, 'html5lib')
            poemtitle = poemsoup.find('h2')
            poetname = poemsoup.find('h3')
            if poemtitle:
                filename = re.sub(r'[/:*?"|<>\n]','',poemtitle.text.strip())
                poetname = re.sub(r'[/:*?"|<>\n]','',poetname.text.strip())
                fileout = poetname+'_'+filename + ".txt"
                output = open(fileout, 'w', encoding='utf-8')
                checktext=re.sub('\xe9','e\'',html.unescape(poemtitle.text).strip())
                print(checktext, file=output)
                poemContent = poemsoup.find('div', {'class': 'merri-font p-poem'})
                poemLines = poemContent.findAll('div')
                for line in poemLines:
                    text = html.unescape(line.text)
                    print(text, file=output)

#removing diacritics
def removeAccents(word):
    repl = {'á': 'a',
            'é': 'e',
            'í': 'i', 'ï': 'i',
            'ó': 'o',
            'ú': 'u',}
    new_word = ''.join([repl[c] if c in repl else c for c in word])
    return new_word

#getting names from wikipedia
def get_poets():
    a = []
    wiki_wiki = wikipediaapi.Wikipedia('en')
    cat = wiki_wiki.page("Category:20th-century_Spanish_poets").categorymembers
    for c in cat.values():
        if not c.title.startswith('Category:'):
            a.append(c.title)
    poets =[]
    for i in a:
        poett = re.sub(r' \([\w ]*\)', '', i)
        poets.append(removeAccents(poett.lower().replace(' ', '-')))
    return poets


for poet in get_poets():
    get_poems(poet)

#removing extra empty lines
for filename in os.listdir(os.getcwd()):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        old_data = f.readlines()
        new_data = ''
        for line in old_data:
            if line != '\n':
                new_data += line
        with open (filename, 'w') as f:
            f.write(new_data)
