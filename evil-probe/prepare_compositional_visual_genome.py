import pandas as pd
import utils
import json
import os

data_path = '../source_datasets/Compositional-Visual-Genome/ComVG.csv'
target_path = os.path.join(utils.TARGET_PATH)


def get_gold_descriptions(probes):

    target_file = '../source_datasets/Compositional-Visual-Genome/image_descs.csv'
    image_descs = {}

    for _, row in probes.iterrows():

        descriptions = image_descs.get(str(row['pos_image_id'])+row['pos_triplet'], [])

        # Only need to append if it is a new one
        if not row['sentence'] in descriptions:
            descriptions.append(row['sentence'])
            image_descs[str(row['pos_image_id'])+row['pos_triplet']] = descriptions

    # Write to csv
    with open(target_file, 'w') as descs:

        for id, sentence in image_descs.items():

            descs.write(str(id)+","+str(sentence)+"\n")
        
    return image_descs


### Have to replace word in original caption to obtain negative caption
def get_neg_sentence(orig, orig_triplet, neg_triplet):

    neg_triplet = neg_triplet.replace('\'', '').replace('(', '').replace(')', '').replace(' ', '')

    orig_triplet = orig_triplet.split(",")
    neg_triplet = neg_triplet.split(",")

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
    
    # print(orig, orig_triplet, neg_triplet, target_index)
    neg_sent = orig.replace(orig_triplet[target_index], neg_triplet[target_index])
    # print(orig, neg_sent)

    return neg_sent

data_dict_subject = {}
data_dict_object = {}
data_dict_verb = {}

comp_vg = pd.read_csv(data_path)
descriptions = get_gold_descriptions(comp_vg)

for _, row in comp_vg.iterrows():

    # neg_sent = get_neg_sentence(row['sentence'], row['pos_triplet'], row['neg_triplet'])
    neg_triplet = row['neg_triplet']
    neg_triplet = neg_triplet.replace('\'', '').replace('(', '').replace(')', '').replace(' ', '')
    neg_sents = descriptions.get(str(row['neg_image_id'])+neg_triplet, None)

    if row['neg_value'] == 'subject':
        data_dict = data_dict_subject
    elif row['neg_value'] == 'object':
        data_dict = data_dict_object
    elif row['neg_value'] == 'verb':
        data_dict = data_dict_verb
    else:
        print('Unknown POS:', row['neg_value'])

    if neg_sents is not None:

        for neg_sent in neg_sents:
            data_dict[str(row['id'])+"_0"] = {
                utils.COL_NAMES['id_col']: "example_" + str(row['id'])+"_0",
                utils.COL_NAMES['image_id_col']: str(row['pos_image_id'])+'.jpg',
                utils.COL_NAMES['image_ds_col']: 'VisualGenome',
                utils.COL_NAMES['sent_1_col']: row['sentence'],
                utils.COL_NAMES['sent_1_label_col']: True,
                utils.COL_NAMES['sent_2_col']: neg_sent,
                utils.COL_NAMES['sent_2_label_col']: False,
                utils.COL_NAMES['ds_col']: 'Comp_VG',
                utils.COL_NAMES['ds_aspect_col']: row['neg_value']
            }

            data_dict[str(row['id'])+"_1"] = {
                utils.COL_NAMES['id_col']: "example_" + str(row['id'])+"_1",
                utils.COL_NAMES['image_id_col']: str(row['neg_image_id'])+'.jpg',
                utils.COL_NAMES['image_ds_col']: 'VisualGenome',
                utils.COL_NAMES['sent_1_col']: neg_sent,
                utils.COL_NAMES['sent_1_label_col']: True,
                utils.COL_NAMES['sent_2_col']: row['sentence'],
                utils.COL_NAMES['sent_2_label_col']: False,
                utils.COL_NAMES['ds_col']: 'Comp_VG',
                utils.COL_NAMES['ds_aspect_col']: row['neg_value']
            }
        
    else:
        print("No negative sentence found for: ", row)


if not os.path.exists(target_path):
    os.makedirs(target_path)

with open(os.path.join(target_path, "compositional_visual_genome_subject.jsonl"), 'w') as target_file:
    for element in data_dict_subject.values():
        target_file.write(json.dumps(element) + "\n")

with open(os.path.join(target_path, "compositional_visual_genome_object.jsonl"), 'w') as target_file:
    for element in data_dict_object.values():
        target_file.write(json.dumps(element) + "\n")

with open(os.path.join(target_path, "compositional_visual_genome_verb.jsonl"), 'w') as target_file:
    for element in data_dict_verb.values():
        target_file.write(json.dumps(element) + "\n")