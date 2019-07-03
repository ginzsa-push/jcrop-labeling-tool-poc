from . import views
from . import cropdata
import json
import os


def listImages(selected_project):
    # move to init
    if selected_project is not None:
        image_folder = selected_project['projectPath']
        print('Images folder... [{}]'.format(image_folder))
        file_names = [fn for fn in os.listdir(image_folder)
                      if any(fn.endswith(ext) for ext in views.included_extensions)]
        print(file_names)
        obj = dict()
        obj['path'] = image_folder
        obj['images'] = file_names
        obj['imgSelected'] = 0
        return obj

    else:
        return None


def images_list(selected_project):
    img_list = listImages(selected_project)
    return img_list['images']


def listImagesJson():
    img_list = listImages()
    return str(img_list['images'])


def init_images_files(crop_data_folder, image_folder):

    project_crop_data_folder = cropdata.create_crop_folder(crop_data_folder)

    # list images from images folder
    print('crop data folder... [{}]'.format(image_folder))
    file_names = [fn for fn in os.listdir(image_folder)
                      if any(fn.endswith(ext) for ext in views.included_extensions)]

    print(file_names)
    for file_name in file_names:
        if os.path.exists(("{}/{}.json".format(project_crop_data_folder, file_name))):
            print('Crop data file {} exist in crop folder'.format(file_name))
        else:
            print('creating {} because is in image folder'.format(file_name))
            with open('{}/{}.json'.format(project_crop_data_folder, file_name), 'w') as outfile:
                json.dump(dict(), outfile)

    # remove from crop folder the items without corresponding image
    cropdata.init_crop_data_files(crop_data_folder, image_folder)

