import os
import json
from . import cropdata

CROP_DATA_FOLDER = 'crop-data'
CROP_DATA_EXT = '.json'


def list_crop_data(selected_project):
    # move to init
    crop_data_folder = './{}/{}'.format(selected_project['projectFolder'], CROP_DATA_FOLDER)
    print('Images folder... [{}]'.format(crop_data_folder))
    # filter temp files like ._22.png.json
    file_names = [fn for fn in os.listdir(crop_data_folder)
                  if any( (fn.endswith(ext) and not fn.startswith('.'))
                         for ext in CROP_DATA_EXT)]

    image_folder = selected_project['projectPath']
    file_names.sort()
    obj = dict()
    obj['imagePath'] = image_folder
    obj['cropdata'] = file_names
    obj['selected'] = 0

    return obj


def create_crop_folder(project_folder):
    project_crop_folder = '{}/{}'.format(project_folder, CROP_DATA_FOLDER)
    # if crop folder does not exist, create one
    if os.path.exists(project_crop_folder):
        print('{} folder exist.'.format(project_crop_folder))
    else:
        print('creating {} folder.'. format(project_crop_folder))
        os.makedirs(project_crop_folder)

    return project_crop_folder


def init_crop_data_files(crop_data_folder, image_folder):
    # if folder exist
    project_crop_data_folder = create_crop_folder(crop_data_folder)

    print('Crop data folder... [{}]'.format(project_crop_data_folder))
    file_names = [fn for fn in os.listdir(project_crop_data_folder) if any(fn.endswith(ext) for ext in CROP_DATA_EXT)]

    for file_name in file_names:
        image_uri = ("{}/{}".format(image_folder, file_name[:-len(CROP_DATA_EXT)]))
        print(image_uri)
        if os.path.exists(image_uri):
            print('Crop data file {} exist in image folder'.format(file_name))
        else:
            print('removing {} because is not in image folder'.format(file_name))
            os.remove(("./{}/{}".format(project_crop_data_folder, file_name)))


def load_image_crop_data(project_folder, img_name):
    with open('{}/{}/{}'.format(project_folder, cropdata.CROP_DATA_FOLDER, img_name + '.json')) as f:
        data = json.load(f)
        return data


def save_capture_to_file(project_folder, img_crop_data, file_name):
    with open('{}/{}/{}'.format(project_folder, cropdata.CROP_DATA_FOLDER, file_name), 'w') as outfile:
        json.dump(img_crop_data, outfile)
