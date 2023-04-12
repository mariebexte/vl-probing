import json
import os
import utils

data_dir = './datasets/orig/Counting-Probe'
target_dir = './datasets/prepared'

for file in os.listdir(data_dir):

    split = file[file.index('.')+1:file.rindex('.')]

    with open(os.path.join(data_dir, file), 'r') as probe_file:

        probe_data = json.load(probe_file)
        probe_dict = {}

        for probe in probe_data:

            # print(probe_data[probe])
            probe_example = probe_data[probe]

            num_foil = 0

            for foil in probe_example['declarative_statement_foils']:

                probe_dict[str(probe_example['dataset_idx']+"_"+str(num_foil))]={
                    utils.COL_NAMES['image_id_col']: probe_example['image_file'],
                    utils.COL_NAMES['image_ds_col']: 'Visual7w',
                    utils.COL_NAMES['sent_1_col']: probe_example['declarative_statement'],
                    utils.COL_NAMES['sent_1_label_col']: True,
                    utils.COL_NAMES['sent_2_col']: foil,
                    utils.COL_NAMES['sent_2_label_col']: False,
                    utils.COL_NAMES['ds_col']: 'Counting-Probe',
                    utils.COL_NAMES['ds_aspect_col']: file[:file.index('.')]
                }
            
        with open(os.path.join(target_dir, file[:file.index('.')] + "_" + split + ".json"), 'w') as target_file:

            json.dump(probe_dict, target_file)
        


