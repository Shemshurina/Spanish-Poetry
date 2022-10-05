import os
import json
from collections import Counter

#counts how many poems of a certain number of syllables among the poems of one author
def line_length(name):
    l2 = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('json') and filename.startswith(name):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        c = 0
        l = []
        while c < len(data['sentences']):
            l.append(data['sentences'][a]['meta'])
            c+=1
        l_counted = Counter(l)
        most_common_element = l_counted.most_common(1)
        if most_common_element[0][1] / len(data['sentences']) >= 0.75:
            l2.append(most_common_element[0][0])
        else:
            l2.append('неодинаковое')
    
    return Counter(l2)

        
