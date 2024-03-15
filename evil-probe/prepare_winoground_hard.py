import os
import utils
import json
from winoground_split import AMBIGUOUSLY_CORRECT

data_path = "../source_datasets/Why-Winoground-Hard/examples_augmented.jsonl"
target_dir = os.path.join(utils.TARGET_PATH)

# key: aspect, value: dict with examples for this aspect
masterdict = {}

with open(data_path, 'r') as data:
    for line in data:

        example = json.loads(line)
        if example['id'] in AMBIGUOUSLY_CORRECT:
            # print('Skip', example['id'])
            pass
        else:
            for caption in ['_0', '_1']:

                caption_data = example['caption' + caption]
                image = example['image' + caption] + '.png'

                id = str(example['id']) + caption
                num_example = 0

                caption_lookup = {}


                # Sort captions into the categories they cover
                for caption in caption_data:

                    caption_type = caption['type'] + "_" + caption['name']
                    caption_type_set = caption_lookup.get(caption_type, set())
                    caption_type_set.add(caption['variant'])
                    caption_lookup[caption_type] = caption_type_set
                

                # Grab the original caption(s) and pair aspect-wise
                orig_captions = caption_lookup.pop('original_original')
                for orig_caption in orig_captions:

                    for aspect in caption_lookup.keys():

                        aspect_captions = caption_lookup[aspect]
                        for aspect_caption in aspect_captions:

                            aspect_dict = masterdict.get(aspect, {})
                            aspect_dict[id + "_" + str(num_example)] = {
                                utils.COL_NAMES['id_col']: 'example_' + id + "_" + str(num_example),
                                utils.COL_NAMES['image_id_col']: image,
                                utils.COL_NAMES['image_ds_col']: 'Winoground',
                                utils.COL_NAMES['sent_1_col']: orig_caption,
                                utils.COL_NAMES['sent_1_label_col']: True,
                                utils.COL_NAMES['sent_2_col']: aspect_caption,
                                utils.COL_NAMES['sent_2_label_col']: True,
                                utils.COL_NAMES['ds_col']: 'why_winoground_hard',
                                utils.COL_NAMES['ds_aspect_col']: aspect
                            }
                            masterdict[aspect] = aspect_dict
                            num_example += 1


for aspect in masterdict:
    num_duplicates=0
    aspect_dict = masterdict[aspect]
    for example in aspect_dict.values():

        sent1 = example['sent_1'].lower()
        sent2 = example['sent_2'].lower()

        if sent1 == sent2:
            # print(sent1, '-', sent2)
            num_duplicates += 1
    
    # print(aspect, num_duplicates)

# Write the examples for each aspect to a separate jsonl file
for aspect in masterdict:

    aspect_dict = masterdict[aspect]
    
    with open(os.path.join(target_dir, "WH_" + aspect + ".jsonl"), 'w') as outfile:
        for example in aspect_dict.values():
            outfile.write(json.dumps(example) + '\n')
