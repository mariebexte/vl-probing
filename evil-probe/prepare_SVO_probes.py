import pandas as pd
import numpy as np
import json
import utils
import sys
import ast
import requests
import urllib.request
import shutil
import os
from requests.exceptions import SSLError, ConnectionError, TooManyRedirects
from PIL import Image


if not os.path.exists(utils.TARGET_PATH):
    os.mkdir(utils.TARGET_PATH)

data_path = '../source_datasets/SVO-Probes/svo_probes.csv'
target_path = os.path.join(utils.TARGET_PATH, 'SVO_probes')
image_target_dir = '../images/SVO_Probes'

if not os.path.exists(image_target_dir):
    os.makedirs(image_target_dir)

probes = pd.read_csv(data_path)
# print(probes.columns)
      
data_dict_subject = {}
data_dict_verb = {}
data_dict_object = {}

def find_image_ids(probes):

    image_ids = {}

    for _, row in probes.iterrows():

        image_ids[row['pos_image_id']] = row['pos_url']
        image_ids[row['neg_image_id']] = row['neg_url']


    for img_id in image_ids:

        grab = False

        if not os.path.exists(os.path.join(image_target_dir, str(img_id)+".jpg")):
            grab = True
        else:
            try:
                im = Image.open(os.path.join(image_target_dir, str(img_id)+".jpg"))
            except IOError:
                print('Found corrupted image file:', img_id, image_ids[img_id])
                grab = True
        
        # Is an empty image
        if img_id == 11156:
            grab = False

        # Only need to grab those that aren't already there
        if grab:

            # print(row)

            try:
                res = requests.get(image_ids[img_id], stream=True)
            except SSLError:
                print('Image couldn\'t be retrieved (SSLError):', img_id)
            except ConnectionError:
                print('Image couldn\'t be retrieved (ConnectionError):', img_id)
            except TooManyRedirects:
                print('Image couldn\'t be retrieved (TooManyRedirects):', img_id)
                

            if res.status_code == 200:
                try:
                    size = int(res.headers['Content-length'])
                except KeyError:
                    size=1

                if size > 0:
                    res.raw.decode_content = True
                    with open(os.path.join(image_target_dir, str(img_id)+".jpg"),'wb') as f:
                        shutil.copyfileobj(res.raw, f)
                        print(img_id, size, image_ids[img_id])
            else:
                print('Image couldn\'t be retrieved (status != 200):', img_id)
    
    # TODO Remove those that are corrupt
    # try:
    #             im = Image.open(os.path.join(image_target_dir, str(img_id)+".jpg"))
    #         except IOError:
    #             print('Found corrupted image file:', img_id, image_ids[img_id])
    #             grab = True


def get_gold_descriptions(probes):

    image_descs = {}

    for _, row in probes.iterrows():

        descriptions = image_descs.get(str(row['pos_image_id'])+row['pos_triplet'], [])

        # Only need to append if it is a new one
        if not row['sentence'] in descriptions:
            descriptions.append(row['sentence'])
            image_descs[str(row['pos_image_id'])+row['pos_triplet']] = descriptions
        
    return image_descs


## No need to parse negative triplets and create misaligned sentence via replacing:
## Use gold descriptions instead (not a perfect match but still triplet-based)
def parse_neg_triplets(neg_triplet):

    if neg_triplet == '[]':
        # print('Negative triplet is empty!')
        return ""

    # Sometimes there are multiple alternatives (and sometimes one, but still in a list)
    if ('[' in neg_triplet):
        neg_triplets = ast.literal_eval(neg_triplet)

        for i in range(len(neg_triplets)):
            neg_triplets[i] = neg_triplets[i].split(',')

        return neg_triplets

    # Other times the triple is just comma-separated words
    else:
        neg_triplet = neg_triplet.split(",")
        return [neg_triplet]

# Have to replace word in original caption to obtain negative caption
def get_neg_sentences(orig, orig_triplet, neg_triplet_string):

    neg_triplets = parse_neg_triplets(neg_triplet_string)
    orig_triplet = orig_triplet.split(",")
    # print(orig_triplet, neg_triplets)

    neg_sents = []

    for neg_triplet in neg_triplets:

        target_index = -1

        for i in range(len(orig_triplet)):

            if orig_triplet[i] != neg_triplet[i]:
                
                if target_index == -1:
                    # print(i, orig_triplet[i], neg_triplet[i])
                    target_index = i
                    
                else:
                    print('Seem to have found two mismatches along the same triples')
            
        if target_index == -1:

            print("Did not find a single change between the following two triples:")
            print(orig_triplet, neg_triplet)
        
        neg_sents.append(orig.replace(orig_triplet[target_index], neg_triplet[target_index]))

    # print(neg_sents)
    return neg_sents

def get_aspect(subject, verb, object):

    values = np.array([subject, verb, object])
    if values.sum() != 1:
        print('None or more than one of SVO were manipulated!')

    if subject:
        return 'subject'
    elif verb:
        return 'verb'
    elif object:
        return 'object'
    else:
        print("None of SVO was manipulated!")
        return ""
    
#find_image_ids(probes)
gold_descriptions = get_gold_descriptions(probes)
# print(gold_descriptions)
# sys.exit(0)

with_neg = 0
without_neg = 0
without_neg_but_also_without_image = 0

dropped_no_image = 0

for idx, row in probes.iterrows():
    
    # neg_sents = get_neg_sentences(row['sentence'], row['pos_triplet'], row['neg_triplet'])
    aspect = get_aspect(subject=row['subj_neg'], verb=row['verb_neg'], object=row['obj_neg'])

    pos_descriptions = gold_descriptions.get(str(row['pos_image_id'])+row['pos_triplet'], [])
    neg_triplets = parse_neg_triplets(row['neg_triplet'])
    neg_descriptions = []
    for neg_triplet in neg_triplets:
        neg_triplet = ",".join(neg_triplet)
        neg_descriptions = neg_descriptions + (gold_descriptions.get(str(row['neg_image_id'])+neg_triplet, []))

    if(len(pos_descriptions)<1):
        print("no pos sentences:", row['pos_image_id'])
    
    if(len(neg_descriptions)<1):
        # print("no neg sentences:", row['neg_image_id'])
        without_neg += 1
        neg_sentences = get_neg_sentences(row['sentence'], row['pos_triplet'], row['neg_triplet'])
        # print(row['sentence'], neg_sentences)
        if not os.path.exists(os.path.join(image_target_dir, str(row['neg_image_id']) + ".jpg")):
            # print("Missing, but image not there anyways!")
            without_neg_but_also_without_image += 1

    else:
        with_neg += 1

    num_pos_sent = 0

    for pos_desc in pos_descriptions:
                                      
        num_neg_sent = 0

        for neg_desc in neg_descriptions:

            if aspect == 'subject':
                data_dict = data_dict_subject
            elif aspect == 'object':
                data_dict = data_dict_object
            elif aspect == 'verb':
                data_dict = data_dict_verb
            else:
                print('Unknown aspect:', aspect)

            if (os.path.exists(os.path.join(image_target_dir, str(row['pos_image_id'])+".jpg"))):

                data_dict[str(idx)+"_0"+"_"+str(num_pos_sent)] = {
                    utils.COL_NAMES['id_col']: "example_" + str(idx)+"_0"+"_"+str(num_pos_sent),
                    utils.COL_NAMES['image_id_col']:str(row['pos_image_id'])+'.jpg',
                    utils.COL_NAMES['image_ds_col']: 'SVO_Probes',
                    utils.COL_NAMES['sent_1_col']: pos_desc,
                    utils.COL_NAMES['sent_1_label_col']: True,
                    utils.COL_NAMES['sent_2_col']: neg_desc,
                    utils.COL_NAMES['sent_2_label_col']: False,
                    utils.COL_NAMES['ds_col']: 'SVO_Probes',
                    utils.COL_NAMES['ds_aspect_col']: aspect
                }
            else:
                dropped_no_image += 1

            if (os.path.exists(os.path.join(image_target_dir, str(row['neg_image_id'])+".jpg"))):
                data_dict[str(idx)+"_1"+"_"+str(num_neg_sent)] = {
                    utils.COL_NAMES['id_col']: "example_" + str(idx)+"_1"+"_"+str(num_neg_sent),
                    utils.COL_NAMES['image_id_col']: str(row['neg_image_id'])+'.jpg',
                    utils.COL_NAMES['image_ds_col']: 'SVO_Probes',
                    utils.COL_NAMES['sent_1_col']: neg_desc,
                    utils.COL_NAMES['sent_1_label_col']: True,
                    utils.COL_NAMES['sent_2_col']: pos_desc,
                    utils.COL_NAMES['sent_2_label_col']: False,
                    utils.COL_NAMES['ds_col']: 'SVO_Probes',
                    utils.COL_NAMES['ds_aspect_col']: aspect
                }
            else:
                dropped_no_image += 1
        
            num_neg_sent += 1

        num_pos_sent += 1

with open(target_path + '_subject.jsonl', 'w') as target_file:
    for element in data_dict_subject.values():
        target_file.write(json.dumps(element) + '\n')

with open(target_path + '_object.jsonl', 'w') as target_file:
    for element in data_dict_object.values():
        target_file.write(json.dumps(element) + '\n')

with open(target_path + '_verb.jsonl', 'w') as target_file:
    for element in data_dict_verb.values():
        target_file.write(json.dumps(element) + '\n')

# print(with_neg, without_neg, without_neg_but_also_without_image)
# print(dropped_no_image)