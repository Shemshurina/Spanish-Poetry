import os
import json
from collections import Counter

#counts how many times each line length occurs
def line_length():
    l = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('json'):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        c = 0
        while c < len(data['sentences']):
            l.append(data['sentences'][a]['meta'])
            c+=1
    return Counter(l)
        
