import json
import sys
import os
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tag import pos_tag
import spacy
import copy

# Location of input files to look for color mentions in
data_folder = '../evil-probe/benchmark'
# Which of the files in the input folder to process
files_of_interest = {'ARO':['aro_attribute.jsonl'],
                     'COCO': ['coco_random.jsonl'],
                     'Flickr30k': ['flickr30k_random.jsonl'],
                     'EqBen_GEBC': ['EqBen_eqbengebc.jsonl'],
                     'EqBen_Kubric': ['EqBen_eqbenkubric_attr.jsonl', 'EqBen_eqbenkubric_cnt.jsonl', 'EqBen_eqbenkubric_loc.jsonl'],
                     'VL-Checklist_short': ['vl-checklist-attribute-vaw_color.jsonl',
                      'vl-checklist-attribute-vg_color.jsonl',
                      'vl-checklist-object-location_vg_obj_center.jsonl',
                      'vl-checklist-object-location_vg_obj_margin.jsonl',
                      'vl-checklist-object-location_vg_obj_mid.jsonl',
                      'vl-checklist-object-location_vg_subj_center.jsonl',
                      'vl-checklist-object-location_vg_subj_margin.jsonl',
                      'vl-checklist-object-location_vg_subj_mid.jsonl',
                      'vl-checklist-object-size_vg_obj_large.jsonl',
                      'vl-checklist-object-size_vg_obj_medium.jsonl',
                      'vl-checklist-object-size_vg_obj_small.jsonl',
                      'vl-checklist-object-size_vg_subj_large.jsonl',
                      'vl-checklist-object-size_vg_subj_medium.jsonl',
                      'vl-checklist-object-size_vg_subj_small.jsonl',
                      'vl-checklist-relation-vg_action.jsonl',
                      'vl-checklist-relation-vg_spatial.jsonl'],
                      'VL-Checklist_long': ['vl-checklist-attribute-vaw_color.jsonl',
                      'vl-checklist-attribute-vg_color.jsonl',
                      'vl-checklist-object-location_vg_obj_center.jsonl',
                      'vl-checklist-object-location_vg_obj_margin.jsonl',
                      'vl-checklist-object-location_vg_obj_mid.jsonl',
                      'vl-checklist-object-location_vg_subj_center.jsonl',
                      'vl-checklist-object-location_vg_subj_margin.jsonl',
                      'vl-checklist-object-location_vg_subj_mid.jsonl',
                      'vl-checklist-object-size_vg_obj_large.jsonl',
                      'vl-checklist-object-size_vg_obj_medium.jsonl',
                      'vl-checklist-object-size_vg_obj_small.jsonl',
                      'vl-checklist-object-size_vg_subj_large.jsonl',
                      'vl-checklist-object-size_vg_subj_medium.jsonl',
                      'vl-checklist-object-size_vg_subj_small.jsonl',
                      'vl-checklist-relation-vg_action.jsonl',
                      'vl-checklist-relation-vg_spatial.jsonl']
                      }

# Output folder
target_folder = 'benchmark'

# For sentence tokenization
nlp = spacy.load("en_core_web_sm")
# Refer to this field as _.normalized instead of .text (because this is editable)
spacy.tokens.token.Token.set_extension('normalized', default='')

# Substrings that mark mentions where 'orange' is meant as a fruit :)
# This will also discard 'an orange and OTHER_COLOR' but we want to get rid of those anyway
orange_exceptions = ['a slice of an orange', 'an orange from', 'a slice of orange', 'orange cut in half', 'and a orange, ', 'an orange on', 'an orange with', ', orange, ', 'blood orange', 'orange juice', 'orange slice', 'orange marmalade', 'orange tree', 'an orange and', 'the round orange and', 'ripe orange', 'the round orange and', 'Offerings of a bamboo plant and orange sitting', 'a sliced orange', 'an orange on', 'the cut orange', 'the rough orange and', 'the orange orange', 'green orange', 'orange orange', 'orange oranges', 'white orange', 'orange has black smiley face', 'yellow orange', 'green orange', 'orange beside green pear', 'orange in brown basket', 'orange in white bowl', 'orange on brown floor', 'orange hanging on brown tree', 'wrench to help squeeze orange', 'pile has orange', 'orange in crate', 'orange hanging on tree', 'orange in bin', 'orange in basket', 'orange inside box', 'orange on ground', 'orange showing segment', 'display has orange', 'orange has eyebrows', 'orange on table', 'orange on counter', 'sticker on orange', 'lots of orange in tree', 'orange in drink', 'orange in basket', 'speck on orange', 'orange has smiley face', 'orange on plate', 'orange on table', 'orange inside box', 'slice of orange', 'orange peel', 'orange in scene', 'dividers in orange', 'orange and a remote', 'orange in bowl', 'purse with orange', 'eye on orange', 'orange in front of orange', 'orange on floor', 'orange on bowl', 'orange wearing hat', 'bowl of orange', 'tassle on orange', 'orange has stem', 'orange in tree', 'orange beside pear', 'orange next to keyboard', 'orange on desk', 'whole orange near fruit', 'skin of orange', 'navel orange are in bowl', 'orange in wicker basket', 'smile on orange', 'orange hanging on a tree', 'orange next to orange', 'shadow cast by orange', 'apple on top of orange', 'stem on orange', 'flesh of orange', 'orange rind', 'orange on a plate', 'orange in fruit market']
orange_exceptions_end = ['an orange.', 'an orange', 'the orange', 'the large orange', 'the unpeeled orange', 'the round orange', 'the connected orange']


# To collect sentences from an input json file into set of (img_path, sentence) tuples
def get_sentences(file):

    # print(file)
    df_file = pd.read_json(file, lines=True)
    sentences = set()

    for _, row in df_file.iterrows():
        image_file = os.path.join(row['img_ds'], row['img_id'])
        sentences.add((image_file, row['sent_1']))

    return sentences


# To collect sentences from an input json file into set of (img_path, sentence) tuples
def get_sentences_vl_checklist(file, two_tokens=True):

    # print(file)
    df_file = pd.read_json(file, lines=True)
    sentences = set()

    for _, row in df_file.iterrows():
        image_file = os.path.join(row['img_ds'], row['img_id'])

        doc = nlp(row['sent_1'])

        # Looking only for two-token descriptions (but also include red fire hydrant, i.e. three-token descriptions)
        if two_tokens:
            if len(doc) <= 3:
                sentences.add((image_file, row['sent_1']))
        # Looking only for longer descriptions
        else:
            if len(doc) > 3:
                sentences.add((image_file, row['sent_1']))

    return sentences


# Identify mentions of provided list of colors in an input sentence
# Return tokenized sentence and map of which token index was found to mention which color
# (necessary for replacement and to skip oranges that are fruits)
def find_colors_in_sentence(sentence, colors):

    num_oranges = 0
    has_tasty_oranges = []

    doc = nlp(sentence)
    # To point from index to color identified at this index
    found_colors = {}
    
    for i in range(len(doc)):

        token = doc[i]
        # Inizitalize token strings
        token._.normalized = token.text

        for color in colors:

            if token._.normalized.lower() == color:

                # if color == 'orange':
                #     print(sentence)

                keep = True

                # Treat oranges with caution
                # Have to determine if it is a fruit orange
                if token._.normalized.lower() == 'orange':

                    # Mend determiner error in original sentence for consistency
                    if i > 0 and doc[i-1]._.normalized.lower() == 'a':
                        doc[i-1]._.normalized = 'an'
                        # print('FIXED!', doc[i-1]._.normalized, sentence)

                    num_oranges += 1

                    # If any of the fruit orange substrings are present: Do not treat as color
                    for orange_exception in orange_exceptions:
                        
                        if orange_exception in sentence:
                            keep=False
                            
                    for orange_exception in orange_exceptions_end:
                        
                        if sentence.endswith(orange_exception):
                            keep=False

                    
                if keep:

                    # Normalize grey to gray
                    if color == 'grey':
                        color = 'gray'
                        doc[i]._.normalized = 'gray'

                    found_colors[i] = color
                
                else:

                    has_tasty_oranges.append(sentence)
                    # print(' +++ Tasty orange! +++')

    # For debugging, but did not find critical instances 
    if num_oranges > 1:
        # print('MORE THAN TWO ORANGES', num_oranges, sentence)
        # sys.exit(0)
        pass

    # Ensure first token is in title case
    doc[0]._.normalized = doc[0]._.normalized.title()
    return found_colors, doc, has_tasty_oranges


if not os.path.exists(target_folder):
    os.mkdir(target_folder)


# for file in os.listdir(data_folder):
#     files = [file]

for name, files in files_of_interest.items():

    print(files)

    target_dir = os.path.join(target_folder, name)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    # To store the two sets of probes
    matrix_probes = {}
    swapped_probes = {}
    # Both sets share the same index
    probes_index = 0

    # In case there were color strings, but as (part of proper) noun, i.e. fruit oranges
    dropped_noun = []
    # In case there was a substring of the format 'c1 and c2'
    dropped_and = []
    # In case there was a substring of the format 'c1 and c2'
    dropped_sequence = []
    # EqBen has sentences where sth is 'not in the scene' - drop those
    dropped_negative = []

    num_sentences = 0
    num_examples = 0
    num_tokens_examples = 0

    # For statistics on how often which color occurs, ...
    color_list = []
    # ... how often which number of color occurs in a single sentence
    num_color_list = []
    # ... and how often which color pair occurs
    color_pair_list = []

    
    # Collect sentences of all input files into a set
    sentences = set()
    for subfile in files:
        if name == 'VL-Checklist_short':
            sentences = sentences.union(get_sentences_vl_checklist(os.path.join(data_folder, subfile), two_tokens=True))
        elif name == 'VL-Checklist_long':
            sentences = sentences.union(get_sentences_vl_checklist(os.path.join(data_folder, subfile), two_tokens=False))
        else:
            sentences = sentences.union(get_sentences(os.path.join(data_folder, subfile)))
        
    # Previously determined set of colors of interest
    # colors = get_colors()
    colors = ['white', 'brown', 'blue', 'black', 'green', 'gray', 'grey', 'red', 'yellow', 'orange', 'pink', 'purple']

    # Sentence is a tuple (image_path, sentence_text)
    for sentence in sentences:
        use_sentence = True

        found_colors, processed_sentence, tasty_oranges = find_colors_in_sentence(sentence[1], colors)

        # Add noun mentions of oranges to list for later inspection
        dropped_noun += tasty_oranges

        # Remove descriptions of things that are NOT in the image
        if (len(found_colors) > 0) and ('not in the scene' in sentence[1]):
            dropped_negative.append(sentence[1])
            use_sentence = False

        # Remove if 'A and B' is in sentence - swapping would not create semantic change
        # And it might be part of a longer list, i.e. the black, blue and brown car
        if use_sentence:
            for color_A in found_colors.values():
                for color_B in found_colors.values():

                    if (color_A + ' and ' + color_B in sentence[1].lower()):
                        dropped_and.append(sentence[1])
                        use_sentence = False

        # Remove if there is a sequence of colors
        if use_sentence and len(found_colors) > 1:

            color_indexes = list(found_colors.keys())
            color_indexes.sort()
            for index in range(len(color_indexes)-1):
                if color_indexes[index]+1 == color_indexes[index+1]:
                    use_sentence = False
                    dropped_sequence.append(sentence[1])

        
        if use_sentence and len(found_colors) > 0:

            num_sentences += 1
            num_examples += len(found_colors)
            num_tokens = 0
            for token in processed_sentence:
                if not token.pos_ == 'PUNCT':
                    num_tokens += 1
            num_tokens_examples += num_tokens * len(found_colors)

            color_list = color_list + list(found_colors.values())
            num_color_list.append(len(found_colors))

            img_info = sentence[0].split('/')
            img_id = img_info[-1]
            img_ds = img_info[:-1]
            if len(img_info) > 1:
                img_ds = '/'.join(img_ds)
            else:
                img_ds = img_ds[0]

            ## Always: Replace any color with all other colors
            for token_index, color in found_colors.items():

                other_colors = copy.deepcopy(colors)
                other_colors.remove(color)

                for other_color in other_colors:

                    new_sent_tokens = []
                    orig_sent_tokens = []

                    # Build original sentence and derived sentence, where target color is replaced
                    for i in range(len(processed_sentence)):

                        # Original sentence always gets original token
                        orig_sent_tokens.append(processed_sentence[i]._.normalized)

                        # If we encounter position of the target color word: Insert it
                        if i == token_index:
                            if i == 0:
                                # Capitalize at beginning
                                new_sent_tokens.append(other_color.title())
                            else:
                                new_sent_tokens.append(other_color)

                        else:
                            # For orange: Pay attention to determiner

                            # ORANGE AS REPLACEMENT
                            # If we are looking at the word before orange and this word is 'a': Use 'an' instead
                            if other_color == 'orange' and i == token_index - 1 and token_index > 0 and processed_sentence[token_index-1]._.normalized == 'a':
                                new_sent_tokens.append('an')
                            elif other_color == 'orange' and i == token_index - 1 and token_index > 0 and processed_sentence[token_index-1]._.normalized == 'A':
                                new_sent_tokens.append('An')

                            # ORANGE IN ORIGINAL TEXT
                            # If we are looking at the word before orange, and this word is 'an': Use 'a' instead
                            elif color == 'orange' and i == token_index - 1 and token_index > 0 and processed_sentence[token_index-1]._.normalized == 'an':
                                new_sent_tokens.append('a')
                            elif color == 'orange' and i == token_index - 1 and token_index > 0 and processed_sentence[token_index-1]._.normalized == 'An':
                                new_sent_tokens.append('A')

                            else:
                                new_sent_tokens.append(processed_sentence[i]._.normalized)
                    
                    sent_1 = ' '.join(orig_sent_tokens)
                    sent_2 = ' '.join(new_sent_tokens)

                    matrix_probes[str(probes_index) + '_matrix_' + color + '_' + other_color] = {
                        'example_id': str(probes_index) + '_matrix_' + color + '_' + other_color,
                        'img_ds': img_ds,
                        'img_id': img_id,
                        'sent_1': sent_1,
                        'sent_2': sent_2,
                        'sent_1_label': True,
                        'sent_2_label': False,
                        'ds_aspect': 'color_' + color + '_' + other_color,
                        'sent_ds': files,
                        'sent_1_color': color,
                        'sent_2_color': other_color,
                    }   

            ## If there are exactly two (different from each other) colors: Swap them
            if len(found_colors) == 2 and len(set(found_colors.values())) == 2:

                color_pair = list(found_colors.values())
                color_pair.sort()
                color_pair_list.append('-'.join(color_pair))
                
                new_sent_tokens = []
                orig_sent_tokens = []

                # Build map to loop up color swap
                color_replacement_map = {}
                color_sequence = []
                for key, value in found_colors.items():
                    color_sequence.append(value)
                    replacement_colors = list(found_colors.values())
                    replacement_colors.remove(value)
                    color_replacement_map[key] = replacement_colors[0]

                for i in range(len(processed_sentence)):

                    # Build original sentence as-is
                    orig_sent_tokens.append(processed_sentence[i]._.normalized)

                    # If respective token is not to be replaced: Copy token from original sentence,
                    # BUT treat orange with caution:
                    if color_replacement_map.get(i, None) == None:
                        
                        # If the next token in original text is 'orange' and the current one is 'an': Change to 'a'
                        if i < len(processed_sentence) - 1 and found_colors.get(i + 1, '') == 'orange' and processed_sentence[i]._.normalized == 'an':
                            new_sent_tokens.append('a')
                        elif i < len(processed_sentence) - 1 and found_colors.get(i + 1, '') == 'orange' and processed_sentence[i]._.normalized == 'An':
                            new_sent_tokens.append('A')

                        # If the next token will be 'orange' and the current one is 'a': Change to 'an'
                        elif i < len(processed_sentence) - 1 and color_replacement_map.get(i + 1, '') == 'orange' and processed_sentence[i]._.normalized == 'a':
                            new_sent_tokens.append('an')
                        elif i < len(processed_sentence) - 1 and color_replacement_map.get(i + 1, '') == 'orange' and processed_sentence[i]._.normalized == 'A':
                            new_sent_tokens.append('An')

                        else:
                            new_sent_tokens.append(processed_sentence[i]._.normalized)

                    else:
                        if i == 0:
                            new_sent_tokens.append(color_replacement_map[i].title())
                        else:
                            new_sent_tokens.append(color_replacement_map[i])

                sent_1 = ' '.join(orig_sent_tokens)
                sent_2 = ' '.join(new_sent_tokens)

                swapped_probes[str(probes_index) + '_swapped'] = {
                    'example_id': str(probes_index) + '_swapped',
                    'img_ds': img_ds,
                    'img_id': img_id,
                    'sent_1': sent_1,
                    'sent_2': sent_2,
                    'sent_1_label': True,
                    'sent_2_label': False,
                    'ds_aspect': 'swap_color',
                    'sent_ds': files,
                    'sent_1_color': color_sequence[0],
                    'sent_2_color': color_sequence[1],
                }

            probes_index += 1

    # Create data files
    with open(os.path.join(target_folder, 'color_matrix_' + name + '.jsonl'), 'w') as matrix_file:
        for example in matrix_probes.values():
            matrix_file.write(json.dumps(example) + '\n')

    with open(os.path.join(target_folder, 'color_swaps_' + name + '.jsonl'), 'w') as swap_file:
        for example in swapped_probes.values():
            swap_file.write(json.dumps(example) + '\n')

    # Write what was skipped
    with open(os.path.join(target_dir, 'skipped_noun.txt'), 'w') as skipped_noun:
        for example in dropped_noun:
            skipped_noun.write(example + '\n')

    with open(os.path.join(target_dir, 'skipped_and.txt'), 'w') as skipped_and:
        for example in dropped_and:
            skipped_and.write(example + '\n')

    with open(os.path.join(target_dir, 'skipped_sequence.txt'), 'w') as skipped_sequence:
        for example in dropped_sequence:
            skipped_sequence.write(example + '\n')

    with open(os.path.join(target_dir, 'skipped_negative.txt'), 'w') as skipped_negative:
        for example in dropped_negative:
            skipped_negative.write(example + '\n')

    fd_color = FreqDist(color_list)
    fd_color_pairs = FreqDist(color_pair_list)
    fd_num_color = FreqDist(num_color_list)
    
    # Write stats
    with open(os.path.join(target_dir, 'stats.txt'), 'w') as stats:
        stats.write('number of sentences:\t' + str(num_sentences) + '\n')
        stats.write('number of examples:\t' + str(num_examples) + '\n')
        stats.write('number of tokens:\t' + str(num_tokens_examples) + '\n')
        stats.write('avg. number of tokens:\t' + str(num_tokens_examples/num_examples) + '\n')
        stats.write('number of skipped due to noun:\t' + str(len(dropped_noun)) + '\n')
        stats.write('number of skipped due to and:\t' + str(len(dropped_and)) + '\n\n')
        stats.write('number of skipped because negative:\t' + str(len(dropped_negative)) + '\n\n')
        stats.write('color counts:\n')
        for (color, count) in fd_color.most_common():
            stats.write(color + '\t' + str(count) + '\n')
        
        stats.write('\n\nnum color pairs:\n')
        for (color, count) in fd_color_pairs.most_common():
            stats.write(str(color) + '\t' + str(count) + '\n')

        stats.write('\n\nnum colors counts:\n')
        for (color, count) in fd_num_color.most_common():
            stats.write(str(color) + '\t' + str(count) + '\n')
            
