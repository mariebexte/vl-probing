import json
import utils
import os

foil_train = "./datasets/orig/FOIL-IT/foilv1.0_train_2017.json"
foil_test = "./datasets/orig/FOIL-IT/foilv1.0_test_2017.json"
filename_lookup_path = "/Volumes/Beauty/Datasets/UNITER MS_COCO/coco_filenames.json"

def get_coco_filename(coco_filenames, filename):

    filename = str(filename).zfill(12) + ".jpg"
    return coco_filenames[filename]

def process_foil(file_path, target_name):

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

            # TODO: Map image id to actual dataset
            foil_dict[utils.COL_NAMES['image_id_col']] = get_coco_filename(coco_filenames, annotation['image_id'])
            foil_dict[utils.COL_NAMES['image_ds_col']] = 'COCO'
            foil_dict[utils.COL_NAMES['ds_aspect_col']] = 'noun'
            foil_dict[utils.COL_NAMES['ds_col']] = 'FOIL-IT'

            if(annotation['target_word']) == 'ORIG':
                foil_dict[utils.COL_NAMES['sent_1_col']] = annotation['caption']
                foil_dict[utils.COL_NAMES['sent_1_label_col']] = True
            
            else:
                foil_dict[utils.COL_NAMES['sent_2_col']] = annotation['caption']
                foil_dict[utils.COL_NAMES['sent_2_label_col']] = False
            
            foil_processed[annotation['id']] = foil_dict
    
    with open(os.path.join(utils.TARGET_PATH, target_name), 'w') as target_file:
        json.dump(foil_processed, target_file)


process_foil(foil_test, 'foil_test.json')
process_foil(foil_train, 'foil_train.json')