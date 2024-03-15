import json
import os
import sys
import utils
import requests
from requests.exceptions import SSLError, ConnectionError, TooManyRedirects
import shutil
from nltk.tokenize import word_tokenize

VG_location_local = '/Volumes/Beauty/Datasets/VisualGenome/VG_100K_2'
VG_location_web = 'https://cs.stanford.edu/people/rak248/VG_100K_2'

base_path = '../source_datasets/VL-Checklist/'
target_path = os.path.join(utils.TARGET_PATH)

if not os.path.exists(target_path):
    os.mkdir(target_path)

def download_image(filename):

    try:
        res = requests.get(os.path.join(VG_location_web, filename), stream=True)
    except SSLError:
        print('Image couldn\'t be retrieved (SSLError):', filename)
    except ConnectionError:
        print('Image couldn\'t be retrieved (ConnectionError):', filename)
    except TooManyRedirects:
        print('Image couldn\'t be retrieved (TooManyRedirects):', filename)
        

    if res.status_code == 200:
        try:
            size = int(res.headers['Content-length'])
        except KeyError:
            size=1

        if size > 0:
            res.raw.decode_content = True
            with open(os.path.join(VG_location_local, filename),'wb') as f:
                shutil.copyfileobj(res.raw, f)
                print('Collected image: ', filename)
    else:
        print('Image couldn\'t be retrieved (status != 200):', filename)


def get_vg_images(probes):

    for image_path, example in probes:

        image_path_parts = image_path.split("/")
        if image_path_parts[0] == 'VG_100K_2':

            if not os.path.exists(os.path.join(VG_location_local, image_path_parts[1])):
                download_image(image_path_parts[1])
            else:
                print('Dont need to collect:', image_path_parts[1])


def write_required_open_images(probes, file):

    with open(os.path.join(base_path, 'open_images_' + file[0:file.index('.')] + '.txt'), 'w') as image_file:
        for image_path, example in probes:

            image_path_parts = image_path.split("/")
            if image_path_parts[0] == 'openimages':
                # print('writing')
                image_file.write('train/' + image_path_parts[1] + '\n')



def process(in_path, out_path):

    for file in os.listdir(in_path):

        if file.endswith(".json"):

            with open(os.path.join(in_path, file), 'r') as in_file:

                data = json.load(in_file)
                data_dict = {}
                id = 0

                # get_vg_images(data)
                write_required_open_images(data, file)

                for image_path, example in data:
                    # print(file, image_path)

                    image_path = image_path.split('/')
                    if len(image_path) == 1:
                        image_path.insert(0, 'SWiG')

                    dataset = image_path[0]

                    if 'VG_100K' in dataset:
                        dataset = 'VisualGenome'

                    if dataset == 'openimages':
                        dataset = 'OpenImages'

                    if dataset == 'hcvrd':
                        dataset = 'VisualGenome'

                    # pic train and val are merged here
                    # if dataset == 'pic':
                    #     dataset = 'pic/train'

                    if dataset == 'vcoco':
                        dataset = 'MS_COCO/' + image_path[1]
                        image_path.pop(0)

                    if dataset == 'hico_20160224_det':
                        dataset = 'hico_20160224_det/'+image_path[2]
                        image_path.pop(1)
                        image_path.pop(1)
                    
                    pos_sents = example['POS']
                    neg_sents = example['NEG']

                    if len(pos_sents) != len(neg_sents):
                        print(pos_sents)
                        print(neg_sents)

                    for i in range(len(pos_sents)):
                        pos_sent = pos_sents[i].lower()
                        neg_sent = neg_sents[i].lower()

                        postokens = set(word_tokenize(pos_sent))
                        negtokens = set(word_tokenize(neg_sent))
                        overlap = len(postokens.intersection(negtokens))

                        if overlap > 0:

                            if ' ON ' in pos_sent:
                                print(pos_sent)
                                
                            data_dict[id] = {
                                utils.COL_NAMES['id_col']: 'example_' + str(id),
                                utils.COL_NAMES['image_id_col']: image_path[1],
                                utils.COL_NAMES['image_ds_col']: dataset,
                                utils.COL_NAMES['sent_1_col']: pos_sent,
                                utils.COL_NAMES['sent_1_label_col']: True,
                                utils.COL_NAMES['sent_2_col']: neg_sent,
                                utils.COL_NAMES['sent_2_label_col']: False,
                                utils.COL_NAMES['ds_col']: 'VL_Checklist',
                                utils.COL_NAMES['ds_aspect_col']: file[:file.index('.')]
                            }
          
                        else:
                            # print("Skipping", pos_sent, '--', neg_sent)
                            pass


                        # Also increment if example is skipped
                        id += 1
                
                with open(os.path.join(out_path + "_" + file + 'l'), 'w') as out_file:
                    for element in data_dict.values():
                        out_file.write(json.dumps(element) + '\n')


process(os.path.join(base_path, 'Attribute', 'vaw'), os.path.join(target_path, 'vl-checklist-attribute-vaw'))
process(os.path.join(base_path, 'Attribute', 'vg'), os.path.join(target_path, 'vl-checklist-attribute-vg'))

process(os.path.join(base_path, 'Object','Location', 'hake_location'), os.path.join(target_path, 'vl-checklist-object-location'))
process(os.path.join(base_path, 'Object','Location', 'swig_location', 'swig_agent'), os.path.join(target_path, 'vl-checklist-object-location'))
process(os.path.join(base_path, 'Object','Location', 'swig_location', 'swig_destination'), os.path.join(target_path, 'vl-checklist-object-location'))
process(os.path.join(base_path, 'Object','Location', 'swig_location', 'swig_item'), os.path.join(target_path, 'vl-checklist-object-location'))
process(os.path.join(base_path, 'Object','Location', 'swig_location', 'swig_tool'), os.path.join(target_path, 'vl-checklist-object-location'))
process(os.path.join(base_path, 'Object','Location', 'vg_location'), os.path.join(target_path, 'vl-checklist-object-location'))
process(os.path.join(base_path, 'Object','Size', 'hake_size'), os.path.join(target_path, 'vl-checklist-object-size'))
process(os.path.join(base_path, 'Object','Size', 'swig_size', 'swig_agent'), os.path.join(target_path, 'vl-checklist-object-size'))
process(os.path.join(base_path, 'Object','Size', 'swig_size', 'swig_destination'), os.path.join(target_path, 'vl-checklist-object-size'))
process(os.path.join(base_path, 'Object','Size', 'swig_size', 'swig_item'), os.path.join(target_path, 'vl-checklist-object-size'))
process(os.path.join(base_path, 'Object','Size', 'swig_size', 'swig_place'), os.path.join(target_path, 'vl-checklist-object-size'))
process(os.path.join(base_path, 'Object','Size', 'swig_size', 'swig_tool'), os.path.join(target_path, 'vl-checklist-object-size'))
process(os.path.join(base_path, 'Object','Size', 'vg_size'), os.path.join(target_path, 'vl-checklist-object-size'))

process(os.path.join(base_path,'Relation'), os.path.join(target_path, 'vl-checklist-relation'))
process(os.path.join(base_path,'Relation', 'vg'), os.path.join(target_path, 'vl-checklist-relation-vg'))


