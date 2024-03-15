import json
import sys
import os
import utils

out_dir = os.path.join(utils.TARGET_PATH)
in_file = '../source_datasets/EqBen/ann_json_finegrained_random.json'

# For each subset, build one dict with id -> dict, where dict has idx -> caption/image_path
masterdict = {}

with open(in_file, 'r') as data:

    eqben = json.load(data)

    for example in eqben:
        dataset = example['private_info']['dataset']
        dataset_dict = masterdict.get(dataset, {})
        element_idx = example['private_info']['name']
        caption = element_idx[:2]
        image = element_idx[2:]
        sample_id = example['private_info']['sample_cnt']
        example_dict = dataset_dict.get(sample_id, {})
        example_dict[image] = example['image']
        example_dict[caption] = example['caption']
        dataset_dict[sample_id] = example_dict
        masterdict[dataset] = dataset_dict


num_ex = 0
num_ex_rest = 0

specificity = []
im_type = []
color = []
nouns = []

for example in masterdict['eqbensd'].items():
    
    ex = example[1]
    sent1 = ex['c0']
    sent2 = ex['c1']

    # sent1 = example[1]['c1'].lower()
    # sent2 = example[1]['c2'].lower()
    # if (sent1 in sent2) or 


    if (sent1 in sent2):
        # print(sent1, "--------", sent2)
        num_ex += 1
    
    else:
        # print(sent1, '---', sent2)
        num_ex_rest += 1


# print(num_ex)
# print(num_ex_rest)

# For each dataset, write examples to file
for dataset in masterdict.keys():

    dataset_dict = {}

    # From each example, build two triples for respective subset
    for id, example in masterdict[dataset].items():
        if len(example) != 4:
            print(example)
            print("The above example seems to to not have exactly two images and two captions!")
            sys.exit(0)

        img_path = example['i0']
        image_dataset = os.path.join('EqBen', img_path[:img_path.rindex('/')])
        image_filename = img_path[img_path.rindex('/')+1:]

        if '.npy' in image_filename:
            image_filename = image_filename.replace('.npy', '.png')
        
        dataset_dict[str(id)+'_0'] = {
            utils.COL_NAMES['id_col']: "example_" + str(id)+'_0',
            utils.COL_NAMES['image_id_col']: image_filename,
            utils.COL_NAMES['image_ds_col']: image_dataset,
            utils.COL_NAMES['sent_1_col']: example['c0'],
            utils.COL_NAMES['sent_1_label_col']: True,
            utils.COL_NAMES['sent_2_col']: example['c1'],
            utils.COL_NAMES['sent_2_label_col']: False,
            utils.COL_NAMES['ds_col']: 'EqBen',
            utils.COL_NAMES['ds_aspect_col']: dataset
        }

        img_path = example['i1']
        image_dataset = os.path.join('EqBen', img_path[:img_path.rindex('/')])
        image_filename = img_path[img_path.rindex('/')+1:]

        if '.npy' in image_filename:
            image_filename = image_filename.replace('.npy', '.png')

        dataset_dict[str(id)+'_1'] = {
            utils.COL_NAMES['id_col']: "example_" + str(id)+'_1',
            utils.COL_NAMES['image_id_col']: image_filename,
            utils.COL_NAMES['image_ds_col']: image_dataset,
            utils.COL_NAMES['sent_1_col']: example['c1'],
            utils.COL_NAMES['sent_1_label_col']: True,
            utils.COL_NAMES['sent_2_col']: example['c0'],
            utils.COL_NAMES['sent_2_label_col']: False,
            utils.COL_NAMES['ds_col']: 'EqBen',
            utils.COL_NAMES['ds_aspect_col']: dataset
        }
    
    with open(os.path.join(out_dir, 'EqBen_' + dataset + '.jsonl'), 'w') as out_file:
        for example in dataset_dict.values():
            out_file.write(json.dumps(example) + '\n')
    
    



