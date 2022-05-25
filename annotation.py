import spacy
import json
import string
import requests
import pylabeador
import string

#rhyme tagging for a stanza
def rhyme(lines):
    poem = ''.join(lines[1:])
    url = 'https://versologie.cz/rhymetagger/api'
    poem_text = poem.split('\xa0\n')
    rhyme_schemes = []
    for stanza in poem_text:
        stanza = stanza.split('\n')
        stanza = list(filter(None, stanza))
        text = json.dumps(stanza)
        params = {
        'text'      : text,      
        'lang'      : 'es',      
        'window'    : 5,        
        'probipa'   : 0.95,     
        'probngram' : 0.95,      
        'penalty'   : 0,         
        'format'    : 3          
        }
        x = requests.get(url, params=params)
        response = json.loads(x.text)
        if None not in response['rhymes']:
            rhyme_schemes.append(response['rhymes'])
    rhyme_schemes2 = []
    [rhyme_schemes2.append(scheme) for scheme in rhyme_schemes if scheme not in rhyme_schemes2]
    return rhyme_schemes2

#counts the number of syllables in a line
def number_of_syllables(line):
    vow = ('a', 'e', 'i', 'o', 'u', 'y', 'á', 'é', 'í', 'ó', 'ú', 'h')
    syllables = []
    syllables2 = []
    nlp = spacy.load("es_core_news_sm")
    line1 = nlp(line.replace('\n', ''))
    words = [token for token in line1]
    for word in words:
        if word.pos_ != 'PUNCT' and str(word) != '—' and str(word)!= '—':
            for s in pylabeador.syllabify(str(word)):
                syllables.append(s)
    for syll in syllables:
        if syllables.index(syll) != 0:
            prev = syllables[syllables.index(syll)-1]
            if syll[0].lower() in vow and prev[-1].lower() in vow:
                syllables2.append(prev + syll)
                del syllables2[-2]
            else:
                syllables2.append(syll)
        else:
            syllables2.append(syll)
    return len(syllables2)


#creating a json-file
def tsa_json(txt_file):
    
    text_dic = {}
    
    file_name = txt_file
    author = file_name.split('_')[0]
    json_name = file_name.lower().replace(' ', '_')
    json_name = json_name.replace('txt', 'json')
    
    with open(txt_file, encoding='utf-8') as txt:
        lines = txt.readlines()
    text_dic['meta'] = {}
    text_dic['meta']['filename'] = json_name
    text_dic['meta']['title'] = lines[0].rstrip()
    text_dic['meta']['author'] = author
    body = lines[1:]


    text = []
    num_of_stanzas = 1
    for line in body:
        if line == '\xa0\n':
            num_of_stanzas += 1
            continue
        nlp = spacy.load("es_core_news_sm")
        line1 = nlp(line.replace('\n', ''))
        words = [token for token in line1]
        line_dict = {}
        line_dict['text'] = str(line1)
        wcnt = 0
        start = 0
        end = 0
        words_array = []
        meta = number_of_syllables(line)
        for word in words:
            word_dict = {}
            word_dict['wf'] = str(word)
            if word.pos_ == 'PUNCT' or str(word) == '—':
                word_dict['wtype'] = 'punct'
            else:
                word_dict['wtype'] = 'word'
            if wcnt==0:
                start = 0
                end = start+len(word)
            if wcnt!=0:
                start = end+1
                end = start+len(word)
            word_dict['off_start'] = start
            word_dict['off_end'] = end
            word_dict['sentence_index'] = wcnt
            wcnt += 1
            word_dict['next_word'] = wcnt
            
            word_dict['sentence_index_neg'] = len(words)-words.index(word)
            
            if word_dict['wtype'] == 'word':
                ana = []
                ana_dict = {}
                ana_dict['lex'] = str(word.lemma_)
                ana_dict['gr.pos'] = str(word.pos_)
                if word.morph.get("Number")!= []:
                    ana_dict['gr.number'] = str(word.morph.get("Number")[0])
                if word.morph.get("Case")!= []:
                    ana_dict['gr.case'] = str(word.morph.get("Case")[0])
                if word.morph.get("PronType")!= []:
                    ana_dict['gr.proType'] = str(word.morph.get("PronType")[0])
                if word.morph.get("Gender")!= []:
                    ana_dict['gr.gen'] = str(word.morph.get("Gender")[0])
                if word.morph.get("Person")!= []:
                    ana_dict['gr.pers'] = str(word.morph.get("Person")[0])
                if word.morph.get("Mood")!= []:
                    ana_dict['gr.mood'] = str(word.morph.get("Mood")[0])
                if word.morph.get("Tense")!= []:
                    ana_dict['gr.tense'] = str(word.morph.get("Tense")[0])
                if word.morph.get("VerbForm")!= []:
                    ana_dict['gr.verbform'] = str(word.morph.get("VerbForm")[0])
                if word.morph.get("Definite")!= []:
                    ana_dict['gr.definite'] = str(word.morph.get("Definite")[0])
                if word.morph.get("Voice")!= []:
                    ana_dict['gr.voice'] = str(word.morph.get("Voice")[0])
                if word.morph.get("Polarity")!= []:
                    ana_dict['gr.polarity'] = str(word.morph.get("Polarity")[0])
                
                word_dict['ana'] = ana_dict
            words_array.append(word_dict)
        line_dict['words'] = words_array
        line_dict['lang'] = 1
        line_dict['meta'] = meta
        text.append(line_dict)
    text_dic['sentences'] = text
    text_dic['meta']['number_of_stanzas'] = str(num_of_stanzas)
    if rhyme(lines) != []:
        text_dic['meta']['rhyme_scheme'] = rhyme(lines)
    else:
        text_dic['meta']['rhyme_scheme'] = 'None'
        
    with open(json_name, 'w') as fp:
        json.dump(text_dic, fp, indent=4)
        
tsa_json('Ángela Figuera Aymerich_Bombardeo.txt')
