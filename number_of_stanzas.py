import os
import json
from collections import Counter

#counts how many times each number of stanzas occurs
def number_of_stanzas():
    l = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('json'):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            l.append(data['meta']['number_of_stanzas'])
    return Counter(l)
print(number_of_stanzas())
