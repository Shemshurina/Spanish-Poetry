import json
import os
import ast


for filename in os.listdir(os.getcwd()):
    if filename.endswith('json'):
        with open(filename) as f:
            data = json.load(f)
        name = 'not specified'
        accuracy = '-'
         
        if set(ast.literal_eval(data['meta']['versos'])) == {2}:
            name = 'pareado'
            accuracy = 'inaccurate'

        if set(ast.literal_eval(data['meta']['versos'])) == {2} and data['meta']['rhyme_scheme']=="[[1, 1]]":
            name = 'pareado'
            accuracy = 'accurate'
            
        if set(ast.literal_eval(data['meta']['versos'])) == {3}:
            name = 'terceto / tercerilla / soleá'
            accuracy = 'inaccurate'
            
        if set(ast.literal_eval(data['meta']['versos'])) == {4}:
            name = 'cuarteto / redondilla / serventesio / cuarteta / copla / seguidilla'
            accuracy = 'inaccurate'

        if set(ast.literal_eval(data['meta']['versos'])) == {4} and data['meta']['rhyme_scheme']=="[[1, 2, 1, 2]]":
            name = 'serventesio / cuarteta'
            accuracy = 'inaccurate'

        if set(ast.literal_eval(data['meta']['versos'])) == {4} and data['meta']['rhyme_scheme']=="[[1, 2, 2, 1]]":
            name = 'cuarteto / redondilla'
            accuracy = 'inaccurate'

        if set(ast.literal_eval(data['meta']['versos'])) == {5}:
            files += 1
            name = 'quintilla / quinteto / lira'
            accuracy = 'inaccurate'

        if set(ast.literal_eval(data['meta']['versos'])) == {6}:
            files += 1
            name = 'sextilla / sexteto'
            accuracy = 'inaccurate'

        if set(ast.literal_eval(data['meta']['versos'])) == {8}:
            files += 1
            name = 'octava real'
            accuracy = 'inaccurate'

        if set(ast.literal_eval(data['meta']['versos'])) == {10}:
            name = 'décima (espinela)'
            accuracy = 'inaccurate'
            
        if set(ast.literal_eval(data['meta']['versos'])) == {10} and data['meta']['rhyme_scheme']=="[[1, 2, 2, 1, 1, 3, 3, 4, 4, 3]]":
            name = 'décima (espinela)'
            accuracy = 'accurate'
            
        if data['meta']['versos']=="[4, 4, 3, 3]" or data['meta']['versos']=="[14]":
            name = 'soneto'
            if data['meta']['rhyme_scheme']!= "None":
                accuracy = 'accurate'
            if data['meta']['rhyme_scheme']== "None":
                accuracy = 'inaccurate'
            
        data['meta']['form_name'] = name
        data['meta']['accuracy'] = accuracy


        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
