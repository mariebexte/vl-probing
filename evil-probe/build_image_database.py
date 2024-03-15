import os
import pandas as pd
import shutil
import json

# For each of the benchmark subsets, collect only those images that it references
# Also serves as a check to see whether all images are present and at the correct location

file_dir = './benchmark'

image_path = '/Volumes/Beauty/Datasets'
db_path = '/Volumes/Beauty/datasets/PROBING_DB_2'

def copy_images(row):
    if not os.path.exists(os.path.join(db_path, row['img_ds'])):
        os.makedirs(os.path.join(db_path, row['img_ds']))

    if not os.path.exists(os.path.join(db_path, row['img_ds'], row['img_id'])):
        print(row['img_ds'] , row['img_id'])
        shutil.copyfile(os.path.join(image_path, row['img_ds'] , row['img_id']), os.path.join(db_path, row['img_ds'] , row['img_id']))


if not os.path.exists(db_path):
    os.mkdir(db_path)


for file in os.listdir(file_dir):
    if file.endswith('.jsonl'):

        print(file)

        # Read jsonl into dataframe
        with open(os.path.join(file_dir, file), 'r') as f:
            lines = f.read().splitlines()
            df_inter = pd.DataFrame(lines)
            if len(df_inter) > 0:
                df_inter.columns = ['json_element']
                df_inter['json_element'].apply(json.loads)
                df_data = pd.json_normalize(df_inter['json_element'].apply(json.loads))

        # data = pd.read_json(os.path.join(file_dir, file), orient='index')
        df_data.apply(copy_images, axis=1)
