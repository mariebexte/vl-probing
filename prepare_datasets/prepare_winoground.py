import json
import utils

file_path = "./datasets/orig/Winoground/examples.jsonl"
target_path = "./datasets/prepared/winoground.json"
winoground_dict = {}

with open(file_path, 'r') as winoground_data:

    for winoground_example in winoground_data:

        example = json.loads(winoground_example)  
        # print(example)

        winoground_dict[str(example['id'])+"_0"] = {
            utils.COL_NAMES['image_id_col']: example['image_0'],
            utils.COL_NAMES['image_ds_col']: 'winoground',
            utils.COL_NAMES['sent_1_col']: example['caption_0'],
            utils.COL_NAMES['sent_1_label_col']: True,
            utils.COL_NAMES['sent_2_col']: example['caption_1'],
            utils.COL_NAMES['sent_2_label_col']: False,
            utils.COL_NAMES['ds_col']: 'Winoground',
            utils.COL_NAMES['ds_aspect_col']: example['collapsed_tag']
        }
        winoground_dict[str(example['id'])+"_1"] = {
            utils.COL_NAMES['image_id_col']: example['image_1'],
            utils.COL_NAMES['image_ds_col']: 'winoground',
            utils.COL_NAMES['sent_1_col']: example['caption_1'],
            utils.COL_NAMES['sent_1_label_col']: True,
            utils.COL_NAMES['sent_2_col']: example['caption_0'],
            utils.COL_NAMES['sent_2_label_col']: False,
            utils.COL_NAMES['ds_col']: 'Winoground',
            utils.COL_NAMES['ds_aspect_col']: example['collapsed_tag']
        }
    
with open(target_path, 'w') as target_file:

    json.dump(winoground_dict, target_file)