import json
import utils
import os

filename_lookup_path = "../source_datasets/MS_COCO/coco_filenames.json"

def get_coco_filename(coco_filenames, filename):

    filename = str(filename).zfill(12) + ".jpg"
    return coco_filenames[filename]

def process_foil(file_path, split, target_name, data_loc):

    foil_processed = {}
    with open(os.path.join(filename_lookup_path), 'r') as coco_filename_lookup:
        coco_filenames = json.load(coco_filename_lookup)

    with open(file_path, 'r') as file:

        # keys: info, images, anntoations, licenses
        foil_data = json.load(file)

        # Information on image licenses
        # for license in foil_data.get('licenses', ""):
        #     print(license)

        # Information on images (license, url/filename in flickr and coco)
        # for image in foil_data.get('images', ""):
        #     print(image)

        # id, foil_id, image_id, caption, target_word (can be 'ORIG'), foil_word, foil: bool
        for annotation in foil_data.get('annotations', ""):
            # print(annotation)

            foil_dict = foil_processed.get(annotation['id'], {})

            # if 'train' not in get_coco_filename(coco_filenames, annotation['image_id']):
            #     print(get_coco_filename(coco_filenames, annotation['image_id'])

            foil_dict[utils.COL_NAMES['id_col']] = 'example_' + str(annotation['id'])
            foil_dict[utils.COL_NAMES['image_id_col']] = get_coco_filename(coco_filenames, annotation['image_id'])
            foil_dict[utils.COL_NAMES['image_ds_col']] = data_loc
            foil_dict[utils.COL_NAMES['ds_aspect_col']] = 'noun'
            foil_dict[utils.COL_NAMES['ds_col']] = 'FOIL-IT'

            if(annotation['target_word']) == 'ORIG':
                foil_dict[utils.COL_NAMES['sent_1_col']] = annotation['caption']
                foil_dict[utils.COL_NAMES['sent_1_label_col']] = True
            
            else:
                foil_dict[utils.COL_NAMES['sent_2_col']] = annotation['caption']
                foil_dict[utils.COL_NAMES['sent_2_label_col']] = False
            
            foil_processed[annotation['id']] = foil_dict
    
    if not os.path.exists(os.path.join(utils.TARGET_PATH)):
        os.makedirs(os.path.join(utils.TARGET_PATH))

    with open(os.path.join(utils.TARGET_PATH, target_name), 'w') as target_file:
        for element in foil_processed.values():
            target_file.write(json.dumps(element) + "\n")


foil_test = "../source_datasets/FOIL-IT/foilv1.0_test_2017.json"
process_foil(foil_test, 'test', 'foil_test.jsonl', 'MS_COCO/val2014')