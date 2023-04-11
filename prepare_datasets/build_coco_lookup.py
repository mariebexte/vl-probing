import os
import json

# Build lookup structure to find whether an image id falls into train, val or test

coco_path = "/Volumes/Beauty/Datasets/UNITER MS_COCO"
target_path = "coco_filenames.json"
coco_dict = {}

for dir in ['train2014', 'val2014', 'test2014']:

    for file in os.listdir(os.path.join(coco_path, dir)):

       if not file.startswith("."):
           
           stripped_file = file[file.rindex("_")+1:]
        #    print(stripped_file)

           coco_dict[stripped_file] = file

with open(os.path.join(coco_path, target_path), 'w') as target_file:

    json.dump(coco_dict, target_file)




