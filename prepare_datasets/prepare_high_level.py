import json
import utils

def prepare(in_file, out_file):

    dataset_dict = {}
    dataset_index = 0

    confident = 0
    not_confident = 0

    with open(in_file, 'r') as data_in:

        for line in data_in:

            example = json.loads(line)
            # print(example)

            # Pair each object-centric caption with all other captions,
            # Excluding those where confidence is too low
            for aspect in ['scene', 'action', 'rationale']:
                for caption, confidence in zip(example['captions'][aspect], example['confidence'][aspect]):

                    # If confidence is high enough, take it
                    if confidence > 3:

                        confident += 1
                         
                        for object_caption in example['captions']['object']:


                            dataset_dict[dataset_index] = {
                                    utils.COL_NAMES['image_id_col']: example['file_name'],
                                    utils.COL_NAMES['image_ds_col']: 'COCO',
                                    utils.COL_NAMES['sent_1_col']: object_caption,
                                    utils.COL_NAMES['sent_1_label_col']: True,
                                    utils.COL_NAMES['sent_2_col']: caption,
                                    utils.COL_NAMES['sent_2_label_col']: True,
                                    utils.COL_NAMES['ds_col']: 'High-level',
                                    utils.COL_NAMES['ds_aspect_col']: aspect
                            } 
                            dataset_index += 1

                    else:
                        not_confident += 1
                        print(confidence, caption)


    with open(out_file, 'w') as dataset_file:

        json.dump(dataset_dict, dataset_file)
    
    print(confident, not_confident)


prepare('./datasets/orig/High-level/train.jsonl', './datasets/prepared/High-level_train.json')
prepare('./datasets/orig/High-level/test.jsonl', './datasets/prepared/High-level_test.json')