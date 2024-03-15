import os
from PIL import Image, UnidentifiedImageError
import requests
from requests.exceptions import SSLError, ConnectionError, TooManyRedirects
import shutil
import sys

# Some VG images are empty (from 100k_2): Check and download if necessary

vg_path_general = "/Volumes/Beauty/Datasets/VisualGenome"
vg_path_probing = "/Volumes/Beauty/Datasets/PROBING_DB/VisualGenome"
VG_location_web = 'https://cs.stanford.edu/people/rak248/VG_100K_2'

def download_image(filename):

    # try:
    #     res = requests.get(os.path.join(VG_location_web, filename), stream=True)
    # except SSLError:
    #     print('Image couldn\'t be retrieved (SSLError):', filename)
    # except ConnectionError:
    #     print('Image couldn\'t be retrieved (ConnectionError):', filename)
    # except TooManyRedirects:
    #     print('Image couldn\'t be retrieved (TooManyRedirects):', filename)
        

    # if res.status_code == 200:
    #     try:
    #         size = int(res.headers['Content-length'])
    #     except KeyError:
    #         size=1

    #     if size > 0:
    #         # res.raw.decode_content = True
    #         # os.remove(os.path.join(vg_path_probing, filename))
    #         with open(os.path.join(vg_path_general, filename),'wb') as f:
    #             shutil.copyfileobj(res.raw, f)
    #             print('Collected image (general): ', filename)
    #         with open(os.path.join(vg_path_probing, filename),'wb') as f:
    #             shutil.copyfileobj(res.raw, f)
    #             print('Collected image (probing): ', filename)
    #     else:
    #         print('Image is empty!')

    # else:
    #     print('Image couldn\'t be retrieved (status != 200):', filename)

    img_data = requests.get(os.path.join(VG_location_web, filename)).content
    with open(os.path.join(vg_path_probing, filename), 'wb') as handler:
        handler.write(img_data)
    with open(os.path.join(vg_path_general, filename), 'wb') as handler:
        handler.write(img_data)


for image in os.listdir(vg_path_probing):

    if image.endswith('.jpg') and not image.startswith('.'):

        try:
            Image.open(os.path.join(vg_path_probing, image))
        
        except UnidentifiedImageError:
            
            # Download from URL to both folders
            print(image)
            download_image(image)