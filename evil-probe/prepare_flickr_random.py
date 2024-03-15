import pandas as pd
import json
import utils
import os
import copy
import random


if not os.path.exists(utils.TARGET_PATH):
    os.mkdir(utils.TARGET_PATH)

random.seed(1334)

def prepare_split(split):

    # Randomly shuffle each caption to make it a match once, a mismatch the other time

    out_path = os.path.join(utils.TARGET_PATH, 'flickr30k_random.jsonl')
    # Karpathy split
    in_file = '../source_datasets/Flickr30k/dataset_flickr30k.json'

    flickr_random_examples = {}

    test_examples = {}

    with open(in_file, 'r') as flickr_data:
        flickr = json.load(flickr_data)

        for example in flickr['images']:

            # Only need to grab those that are testing answers
            if example['split'] == split:

                image = example['filename']
                sentences = example['sentences']

                for sentence in sentences:
                    test_examples[sentence['sentid']] = {'id': sentence['sentid'], 'image': image, 'sentence': sentence['raw']}

    test_examples_drawpool = copy.deepcopy(test_examples)

    # Pair each caption with a randomly drawn caption from a different image
    for caption in test_examples.values():

        rand_capt_image = -1
        while (rand_capt_image == -1) or (rand_capt_image == caption['image']):

            rand_capt_id = random.choice(list(test_examples_drawpool.keys()))
            rand_capt_image = test_examples_drawpool[rand_capt_id]['image']

        rand_capt = test_examples_drawpool.pop(rand_capt_id)

        pair_id = str(caption['id']) + '_' + str(rand_capt['id'])
        flickr_random_examples[pair_id] = {
            utils.COL_NAMES['id_col']: 'example_' + pair_id,
            utils.COL_NAMES['image_id_col']: caption['image'],
            utils.COL_NAMES['image_ds_col']: 'Flickr30k',
            utils.COL_NAMES['sent_1_col']: caption['sentence'],
            utils.COL_NAMES['sent_1_label_col']: True,
            utils.COL_NAMES['sent_2_col']: rand_capt['sentence'],
            utils.COL_NAMES['sent_2_label_col']: False,
            utils.COL_NAMES['ds_col']: 'Flickr30k',
            utils.COL_NAMES['ds_aspect_col']: 'random'
        }

    with open(out_path, 'w') as out_file:
        for example in flickr_random_examples.values():
            out_file.write(json.dumps(example) + '\n')
     

prepare_split('test')
# prepare_split('train')
# prepare_split('val')