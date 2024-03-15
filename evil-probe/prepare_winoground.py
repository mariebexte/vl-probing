import json
import utils
import os
from winoground_split import AMBIGUOUSLY_CORRECT

file_path = "../source_datasets/Winoground/examples.jsonl"
target_path = os.path.join(utils.TARGET_PATH)
winoground_dict_relation = {}
winoground_dict_object = {}
winoground_dict_both = {}

if not os.path.exists(target_path):
    os.mkdir(target_path)

with open(file_path, 'r') as winoground_data:

    for winoground_example in winoground_data:

        example = json.loads(winoground_example)  
        if (example['id'] in AMBIGUOUSLY_CORRECT):
            # print('SKIP', example['id'])
            pass
        else:

            if example['collapsed_tag'] == 'Relation':
                winoground_dict = winoground_dict_relation
            elif example['collapsed_tag'] == 'Object':
                winoground_dict = winoground_dict_object
            elif example['collapsed_tag'] == 'Both':
                winoground_dict = winoground_dict_both
            else:
                print('Unknown aspect:', example['collapsed_tag'])

            winoground_dict[str(example['id'])+"_0"] = {
                utils.COL_NAMES['id_col']: "example_" + str(example['id'])+"_0",
                utils.COL_NAMES['image_id_col']: example['image_0'] + '.png',
                utils.COL_NAMES['image_ds_col']: 'Winoground',
                utils.COL_NAMES['sent_1_col']: example['caption_0'],
                utils.COL_NAMES['sent_1_label_col']: True,
                utils.COL_NAMES['sent_2_col']: example['caption_1'],
                utils.COL_NAMES['sent_2_label_col']: False,
                utils.COL_NAMES['ds_col']: 'Winoground',
                utils.COL_NAMES['ds_aspect_col']: example['collapsed_tag']
            }
            winoground_dict[str(example['id'])+"_1"] = {
                utils.COL_NAMES['id_col']: "example_" + str(example['id'])+"_1",
                utils.COL_NAMES['image_id_col']: example['image_1'] + '.png',
                utils.COL_NAMES['image_ds_col']: 'Winoground',
                utils.COL_NAMES['sent_1_col']: example['caption_1'],
                utils.COL_NAMES['sent_1_label_col']: True,
                utils.COL_NAMES['sent_2_col']: example['caption_0'],
                utils.COL_NAMES['sent_2_label_col']: False,
                utils.COL_NAMES['ds_col']: 'Winoground',
                utils.COL_NAMES['ds_aspect_col']: example['collapsed_tag']
            }
    
if not os.path.exists(target_path):
    os.makedirs(target_path)

with open(os.path.join(target_path, 'winoground_relation.jsonl'), 'w') as target_file:
    for element in winoground_dict_relation.values():
        target_file.write(json.dumps(element) + '\n')

with open(os.path.join(target_path, 'winoground_object.jsonl'), 'w') as target_file:
    for element in winoground_dict_object.values():
        target_file.write(json.dumps(element) + '\n')

with open(os.path.join(target_path, 'winoground_both.jsonl'), 'w') as target_file:
    for element in winoground_dict_both.values():
        target_file.write(json.dumps(element) + '\n')