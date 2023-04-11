import json
from nltk.probability import FreqDist
import os
import utils

file_path = "./datasets/orig/Predicate-Noun/eval_set.json"
target_path = "./datasets/prepared/predicate-noun.json"

def write_replacement_frequencies_and_filenames(data, target_path):

    object_list = []
    subject_list = []

    with open(os.path.join(target_path, 'open_images_required.txt'), 'w') as required_images:

        # id, filename, sentence_target, sentence_distractor, sentence_target_alt, sentence_distractor_alt
        for example in data:

            if example['pos'] == 'subject':
                subject_list.append(example['word_target']+" "+example['word_distractor'])
            
            elif example['pos'] == 'object':
                object_list.append(example['word_target'] + " " + example['word_distractor'])
            
            else:
                print('Unknown pos')
            
            required_images.write(example['open_images_split']+"/"+example['img_filename'][:-4]+"\n")
    
    objects = FreqDist(object_list)
    subjects = FreqDist(subject_list)

    for key in objects:
        print(key, objects[key])
    
    for key in subjects:
        print(key, subjects[key])

    for pair in (('objects', objects), ('subjects', subjects)):
        with open(os.path.join(target_path, pair[0]+'_replacement_counts.txt'), 'w') as target_file:
            for key in pair[1]:
                target_file.write(str(pair[1][key])+"\t"+key+"\n")


with open(file_path, 'r') as file:

    data = json.load(file)
    dataset_dict = {}

    # Write statistic on how often what is replaced with what
    # And which image files are referenced in this datasets (to not have to download the entire 500G)
    # write_replacement_frequencies_and_filenames(data, os.path.dirname(file_path))

    for example in data:

        # print(example)

        example_dict = {}
        example_dict[utils.COL_NAMES['image_id_col']] = example['img_filename']
        example_dict[utils.COL_NAMES['image_ds_col']] = 'open_images'
        example_dict[utils.COL_NAMES['sent_1_col']] = example['sentence_target']
        example_dict[utils.COL_NAMES['sent_1_label_col']] = True
        example_dict[utils.COL_NAMES['sent_2_col']] = example['sentence_distractor']
        example_dict[utils.COL_NAMES['sent_2_label_col']] = False
        example_dict[utils.COL_NAMES['ds_col']] = 'pred-noun'
        example_dict[utils.COL_NAMES['ds_aspect_col']] = example['pos']

        dataset_dict[example['id']] = example_dict

    with open(target_path, 'w') as target_file:

        json.dump(dataset_dict, target_file)
