import os
import json
from PIL import Image
from shutil import copyfile
from ... import utils

CROP_DATA_FOLDER = 'crop-data'

def buildTransformer():
    return Yolo3Transform()


class Yolo3Transform:

    def get_type(self):
        return 'yolo3'

    def transform(self, project):
        project_name = project['projectName']

        print('transform project: {}'.format(project_name))
        project_path = './{}/{}'.format(project_name, CROP_DATA_FOLDER)
        json_files = [pos_json for pos_json in os.listdir(project_path) if pos_json.endswith('.json')]
        for json_file in json_files:
            with open('{}/{}'.format(project_path, json_file)) as f:
                data = json.load(f)
                self.transform_cropdata(data, project)

    def transform_cropdata(self, data, project):
        # transform

        # for each label
        for label in data:
            # generate line
            print(label)
            crop_data = data[label]
            true_dim = self.extract_dimentions(crop_data)
            print(true_dim)
            dim = (true_dim['twd'], true_dim['thd'])
            # min x, max x, min y, max y
            box = [true_dim['cx'], (true_dim['cx'] + true_dim['cw']),
                   true_dim['cy'], (true_dim['cy'] + true_dim['ch'])]
            converted = self.convert_box(dim, box)
            print(converted)

            project_name = project['projectName']

            # save [image_name].txt to project destination
            # create empty file (check if exist)
            origin_file, origin_ext = self.separate_file_name_extention(crop_data['img'])
            image_file = "{}/{}.txt".format(project['destination'], origin_file)

            utils.establish_path(project['destination'])

            img_file = open(image_file, 'w')
            img_file.write("{} {}\n".format(label, str(converted).strip('()')))
            img_file.close()

            # add class_list.txt
            # copy [project]/label.txt to /destination/[project]/class_list.txt
            src = "./{}/label.txt".format(project_name)
            dst = "{}/{}".format(project['destination'], "class_list.txt")
            copyfile(src, dst)

            # crop to project destination
            # save into label folder
            # image_number.png
            im = Image.open("{}/{}".format(project['projectPath'], crop_data['img']) )
            croped = im.crop((true_dim['cx'],
                     true_dim['cy'],
                     (true_dim['cx'] + true_dim['cw']),
                     (true_dim['cy'] + true_dim['ch'])))

            # crate directory
            croped_path = "{}/{}".format(project['destination'],label)
            if not os.path.exists(croped_path):
                os.makedirs(croped_path)

            croped.save("{}/{}".format(croped_path, "{}{}".format(origin_file, origin_ext)))

        yolo = {}
        return yolo

    def convert_box(self, size, box):

        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (box[0] + box[1]) / 2.0
        y = (box[2] + box[3]) / 2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return x, y, w, h

    def convert(self, x, y, w, h):
        return self.convert_box([w, h], x, y)

    def extract_dimentions(self, crop_data):

        true_dim = {}
        true_dim['twd'] = float(crop_data.get('twd', 1))
        true_dim['thd'] = float(crop_data.get('thd', 1))
        true_dim['cx'] = float(crop_data['cx'])
        true_dim['cy'] = float(crop_data['cy'])
        true_dim['cw'] = float(crop_data['cw'])
        true_dim['ch'] = float(crop_data['ch'])

        return true_dim

    # remove file extentions -
    # todo move to an util class
    def separate_file_name_extention(self, file_name):
        return file_name[:(file_name.index('.') - len(file_name))], file_name[(file_name.index('.') - len(file_name)):]
