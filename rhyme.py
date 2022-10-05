import os
import json
from collections import Counter

#counts how many times each rhyme scheme occurs
def rhyme():
    l = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('json'):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            if data['meta']['rhyme_scheme'] != 'None':
                for scheme in data['meta']['rhyme_scheme']:
                    l.append(tuple(scheme))
            else:
                l.append(data['meta']['rhyme_scheme'])
    return Counter(l)
