import json
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import pandas as pd
import sys
import utils
import os


path = "../source_datasets/Visual-Spatial-Reasoning/all_vsr_validated_data.jsonl"
target_path = os.path.join(utils.TARGET_PATH)
example_dict = {}
dict_index = 0

if not os.path.exists(target_path):
    os.mkdir(target_path)

# Read jsonl into dataframe
with open(path, 'r') as f:
    lines = f.read().splitlines()

    df_inter = pd.DataFrame(lines)
    df_inter.columns = ['json_element']
    df_inter['json_element'].apply(json.loads)
    df_data = pd.json_normalize(df_inter['json_element'].apply(json.loads))


# Check whether two descriptions discuss the same two nouns
def same_nouns(descr1, descr2):

    exclusions = ['side', 'front', 'top', 'edge', 'part', 'middle', 'back']

    tokens1 = word_tokenize(descr1)
    tokens2 = word_tokenize(descr2)
    pos1 = pos_tag(tokens1)
    pos2 = pos_tag(tokens2)
    noun1 = [token for (token, pos) in pos1 if pos=='NN' and (not (token in exclusions))]
    noun2 = [token for (token, pos) in pos2 if pos=='NN' and (not (token in exclusions))]

    match = True
    for noun in noun1:
        if not noun in noun2:
            match = False
    for noun in noun2:
        if not noun in noun1:
            match = False

    return match



# For each image, collect all descriptions
for image in df_data['image'].unique():

    df_image = df_data[df_data['image'] == image]

    df_image_0 = df_image[df_image['label'] == 0]
    df_image_1 = df_image[df_image['label'] == 1]

    if (len(df_image) != (len(df_image_0) + len(df_image_1))):
        print('There seems to be a label other than 0 and 1 present!')
        sys.exit(0)

    # For each matching description, pair with all mismatched ones that discuss the same nouns
    for id1, description_1 in df_image_1.iterrows():
        for id0, description_0 in df_image_0.iterrows():

            if same_nouns(description_1['caption'], description_0['caption']):

                image_ds = 'MS_COCO/train2017'
                if 'val2017' in description_1['image_link']:
                    image_ds = 'MS_COCO/val2017'

                # if '000000294831.jpg' in description_1['image_link']:
                #     print(description_1)
                # print(str(id1)+"_"+str(id0))

                example_dict[str(id1)+"_"+str(id0)] = {
                    utils.COL_NAMES['id_col']: 'example_' + str(id1)+"_"+str(id0),
                    utils.COL_NAMES['image_id_col']: image,
                    utils.COL_NAMES['image_ds_col']: image_ds,
                    utils.COL_NAMES['sent_1_col']: description_1['caption'],
                    utils.COL_NAMES['sent_1_label_col']: True,
                    utils.COL_NAMES['sent_2_col']: description_0['caption'],
                    utils.COL_NAMES['sent_2_label_col']: False,
                    utils.COL_NAMES['ds_col']: 'VSR',
                    utils.COL_NAMES['ds_aspect_col']: 'preposition'
                }

if not os.path.exists(target_path):
    os.makedirs(target_path)

# Convert dict to json and save
with open(os.path.join(target_path, 'visual_spatial_reasoning.jsonl'), 'w') as target_file:
    for element in example_dict.values():
        target_file.write(json.dumps(element) + '\n')