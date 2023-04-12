import json
import os
import utils

def process(in_path, out_path):

    for file in os.listdir(in_path):

        if file.endswith(".json"):

            with open(os.path.join(in_path, file), 'r') as in_file:

                data = json.load(in_file)
                data_dict = {}
                id = 0


                for image_path, example in data:
                    print(file, image_path)

                    image_path = image_path.split('/')
                    if len(image_path) == 1:
                        image_path.insert(0, 'SWiG')

                    data_dict[id] = {
                        utils.COL_NAMES['image_id_col']: image_path[1],
                        utils.COL_NAMES['image_ds_col']: image_path[0],
                        utils.COL_NAMES['sent_1_col']: example['POS'],
                        utils.COL_NAMES['sent_1_label_col']: True,
                        utils.COL_NAMES['sent_2_col']: example['NEG'],
                        utils.COL_NAMES['sent_2_label_col']: False,
                        utils.COL_NAMES['ds_col']: 'VL_Checklist',
                        utils.COL_NAMES['ds_aspect_col']: file[:file.index('.')]
                    }
                    id += 1
                
                with open(os.path.join(out_path + "_" + file), 'w') as out_file:

                    json.dump(data_dict, out_file)



base_path = './datasets/orig/VL-Checklist/'
target_path = './datasets/prepared/'
process(os.path.join(base_path, 'Attribute', 'vaw'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path, 'Attribute', 'vg'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))

process(os.path.join(base_path, 'Object','Location', 'hake_location'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path, 'Object','Location', 'swig_location'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path, 'Object','Location', 'vg_location'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path, 'Object','Size', 'hake_size'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path, 'Object','Size', 'swig_size'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path, 'Object','Size', 'vg_size'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))

process(os.path.join(base_path,'Relation'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path,'Relation', 'vg'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))


