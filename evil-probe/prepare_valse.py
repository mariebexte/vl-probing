import json
import os
import utils
from nltk.tokenize import sent_tokenize
import sys


valse_path = "../source_datasets/VALSE"
target_path = os.path.join(utils.TARGET_PATH)

if not os.path.exists(target_path):
    os.mkdir(target_path)

def get_question_answer(coreference_input):
    sentences = sent_tokenize(coreference_input)
    sentences.pop(0)
    return " ".join(sentences)


# For each instrument
for file in os.listdir(valse_path):

    # print(file)

    # For each instrument
    with open(os.path.join(valse_path, file), 'r') as instrument_file:

        instrument = json.load(instrument_file)
        instrument_dict = {}

        example_id = 0

        # dataset, dataset_idx, image_file, phenomena, caption, answer, classes, split, original_split, classes_foil, mturk (foil)
        for id, example in instrument.items():

            # print(id, example)
            example_dict = {}

            # Adapt path to our data structure
            dataset = example['dataset']
            if dataset == 'VisDial_v1.0':
                dataset = 'VisualDialog/val2018'
                if 'COCO_train2014' in example['image_file']:
                    dataset = 'MS_COCO/train2014'
                if 'COCO_val2014' in example['image_file']:
                    dataset = 'MS_COCO/val2014'

            elif dataset == 'FOIL dataset':
                dataset = 'MS_COCO/val2014'
            elif dataset == 'coco_2017' or dataset == 'coco2017':
                dataset = 'MS_COCO/val2017'

            example_dict[utils.COL_NAMES['id_col']] = 'example_' + str(example_id)
            example_dict[utils.COL_NAMES['image_id_col']] = example['image_file']
            example_dict[utils.COL_NAMES['image_ds_col']] = dataset
            example_dict[utils.COL_NAMES['sent_1_col']] = example['caption']
            example_dict[utils.COL_NAMES['sent_1_label_col']] = True
            example_dict[utils.COL_NAMES['sent_2_col']] = example['foil']
            example_dict[utils.COL_NAMES['sent_2_label_col']] = False
            example_dict[utils.COL_NAMES['ds_col']] = "VALSE"
            example_dict[utils.COL_NAMES['ds_aspect_col']] = example['linguistic_phenomena']

            instrument_dict[example_id] = example_dict

            example_id += 1

        if not os.path.exists(target_path):
            os.makedirs(target_path)
    
        with open(os.path.join(target_path, "VALSE-"+file+'l'), 'w') as target_file:
            for element in instrument_dict.values():
                target_file.write(json.dumps(element) + '\n')
        
        # Create question-only files
        if 'coreference' in file:
            for key, value in instrument_dict.items():
                sent_1 = value[utils.COL_NAMES['sent_1_col']]
                sent_2 = value[utils.COL_NAMES['sent_2_col']]
                sent_1 = get_question_answer(sent_1)
                sent_2 = get_question_answer(sent_2)
                value[utils.COL_NAMES['sent_1_col']] = sent_1
                value[utils.COL_NAMES['sent_2_col']] = sent_2

            with open(os.path.join(target_path, "VALSE-"+file[:file.index('.')]+'_question-only.jsonl'), 'w') as target_file:
                for element in instrument_dict.values():
                    target_file.write(json.dumps(element) + '\n')






                

