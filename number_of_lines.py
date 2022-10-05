import os
import json
from collections import Counter

#counts how many times each number of lines occurs
def number_of_lines(name):
    l = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('json') and filename.startswith(name):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        l.append(len(data['sentences']))
    return Counter(l)


