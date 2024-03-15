import json
import os
import utils

data_path = "../source_datasets/ARO"
target_path = os.path.join(utils.TARGET_PATH)

def prepare_aro(in_path, aspect, out_path):

    data_dict = {}
    dict_idx = 0

    with open(in_path, 'r') as data_in:
        data = json.load(data_in)

        for example in data:
            data_dict[dict_idx] = {
                utils.COL_NAMES['id_col']: 'example_' + str(dict_idx),
                utils.COL_NAMES['image_id_col']: example['image_path'],
                utils.COL_NAMES['image_ds_col']: 'ARO',
                utils.COL_NAMES['sent_1_col']: example['true_caption'],
                utils.COL_NAMES['sent_1_label_col']: True,
                utils.COL_NAMES['sent_2_col']: example['false_caption'],
                utils.COL_NAMES['sent_2_label_col']: False,
                utils.COL_NAMES['ds_col']: 'ARO',
                utils.COL_NAMES['ds_aspect_col']: aspect
            }
            dict_idx += 1
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        with open(os.path.join(target_path, out_path), 'w') as target_file:
            for element in data_dict.values():
                target_file.write(json.dumps(element) + "\n")


prepare_aro(os.path.join(data_path, "visual_genome_attribution.json"), 'attribute', "aro_attribute.jsonl")
prepare_aro(os.path.join(data_path, "visual_genome_relation.json"), 'relation', "aro_relation.jsonl")