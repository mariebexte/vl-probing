import json
import os
import utils

valse_path = "./datasets/orig/VALSE"
target_path = "./datasets/prepared"

# For each instrument
for file in os.listdir(valse_path):

    print(file)

    # For each instrument
    with open(os.path.join(valse_path, file), 'r') as instrument_file:

        instrument = json.load(instrument_file)
        instrument_dict = {}

        # dataset, dataset_idx, image_file, phenomena, caption, answer, classes, split, original_split, classes_foil, mturk (foil)
        for id, example in instrument.items():

            # print(id, example)
            example_dict = {}

            example_dict[utils.COL_NAMES['image_id_col']] = example['image_file']
            example_dict[utils.COL_NAMES['image_ds_col']] = example['dataset']
            example_dict[utils.COL_NAMES['sent_1_col']] = example['caption']
            example_dict[utils.COL_NAMES['sent_1_label_col']] = True
            example_dict[utils.COL_NAMES['sent_2_col']] = example['foil']
            example_dict[utils.COL_NAMES['sent_2_label_col']] = False
            example_dict[utils.COL_NAMES['ds_col']] = "VALSE"
            example_dict[utils.COL_NAMES['ds_aspect_col']] = example['linguistic_phenomena']

            instrument_dict[id] = example_dict
    
        with open(os.path.join(target_path, "VALSE-"+file), 'w') as target_file:

            json.dump(instrument_dict, target_file)