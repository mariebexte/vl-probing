import pandas as pd
import json



file = 'benchmark/EqBen_eqbensd.jsonl'
COLORS = set(['blue', 'black', 'red', 'brown'])
NOUNS = set(['shark', 'fish', 'dolphin', 'whale', 'cattle', 'horse', 'lion', 'pig', 'deer', 'goat', 'elephant', 'zebra', 'duck', 'chicken', 'frog', 'camel', 'dog', 'crab', 'wolf', 'rabbit', 'tiger', 'bear', 'cat', 'hat', 'cowboy', 'crown', 'cap', 'dove', 'bird', 'rat', 'squirrel', 'koala', 'panda', 'monkey', 'fox', 'shrimp', 'eagle'])
IMG_TYPE = set(['real', 'a', 'an', 'image', 'pencil', 'sketch', 'oil', 'painting', 'post-impressionism', 'Gogh', 'Van'])

color = []
noun = []
img_type = []
specificity = []
skip = []

with open(file, 'r') as data:

    for line in data:

        example = json.loads(line)
        # print(example)

        if example['sent_1'] in example['sent_2']:

            example['ds_aspect'] = 'eqbensd_skip'
            skip.append(example)
            # print("Drop:")
            pass
        
        elif example['sent_2'] in example['sent_1']:


            example['ds_aspect'] = 'eqbensd_specificity'
            specificity.append(example)
            # print("Specificity:")
            pass
        
        else:

            tokens_1 = set(example['sent_1'].split(" "))
            tokens_2 = set(example['sent_2'].split(" "))
            t1 = tokens_1.difference(tokens_2)
            t2 = tokens_2.difference(tokens_1)

            if t1.issubset(COLORS) and t2.issubset(COLORS):
                
                example['ds_aspect'] = 'eqbensd_color'
                color.append(example)
                # print('Colors:')
                pass
            
            elif t1.issubset(NOUNS) and t2.issubset(NOUNS):

                example['ds_aspect'] = 'eqbensd_noun'
                noun.append(example)
                # print('NOUNS:')
                pass
        
            elif t1.issubset(IMG_TYPE) and t2.issubset(IMG_TYPE):
                
                example['ds_aspect'] = 'eqbensd_img_type'
                img_type.append(example)
                # print('IMG TYPE:')
                pass
            
            else:

                print(tokens_1.difference(tokens_2), tokens_2.difference(tokens_1))
                # print(tokens_1.intersection(tokens_2))
                print(example['sent_1'], example['sent_2'])



for subset in [(color, 'color'), (img_type, 'img_type'), (specificity, 'specificity'), (noun, 'noun')]:

    aspect = subset[1]
    with open('benchmark/EqBen_eqbensd_' + str(aspect) + '.jsonl', 'w') as out:

        for ex in subset[0]:

            out.write(json.dumps(ex) + "\n")