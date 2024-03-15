import json
import utils
import os

def prepare(in_file, split):

    dataset_dict_scene = {}
    dataset_dict_action = {}
    dataset_dict_rationale = {}

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

                            # if 'train' not in example['file_name']:
                            #     print(example['file_name'])

                            if aspect == 'scene':
                                dataset_dict = dataset_dict_scene
                            elif aspect == 'action':
                                dataset_dict = dataset_dict_action
                            elif aspect == 'rationale':
                                dataset_dict = dataset_dict_rationale
                            else:
                                print('Unknown dataset aspect:', aspect)

                            dataset_dict[dataset_index] = {
                                    utils.COL_NAMES['id_col']: "example_" + str(dataset_index),
                                    utils.COL_NAMES['image_id_col']: example['file_name'],
                                    utils.COL_NAMES['image_ds_col']: 'MS_COCO/train2014',
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
                        # print(confidence, caption)


    target_file = os.path.join(utils.TARGET_PATH)
    if not os.path.exists(target_file):
        os.makedirs(target_file)

    with open(os.path.join(target_file, "High-level_"+split+"_scene.jsonl"), 'w') as dataset_file:
        for element in dataset_dict_scene.values():
            dataset_file.write(json.dumps(element) + "\n")

    with open(os.path.join(target_file, "High-level_"+split+"_action.jsonl"), 'w') as dataset_file:
        for element in dataset_dict_action.values():
            dataset_file.write(json.dumps(element) + "\n")

    with open(os.path.join(target_file, "High-level_"+split+"_rationale.jsonl"), 'w') as dataset_file:
        for element in dataset_dict_rationale.values():
            dataset_file.write(json.dumps(element) + "\n")
    
    # print(confident, not_confident)


prepare('../source_datasets/High-level/test.jsonl', 'test')