import json

label_file_name = 'label.txt'
label_color_file_name = 'label_color.json'


def get_labels_from_file(project_name):
    f = open("{}/{}".format(project_name, label_file_name), "r")
    contents = f.readlines()
    content_list = []
    for line in contents:
        content_list.append(line.rstrip("\n\r"))

    return content_list


def save_label_to_file(project_folder, label_list):
    with open('{}/{}'.format(project_folder, label_file_name), 'w') as f:
        for item in label_list:
            f.write("%s\n" % item)


def save_label_color_to_file(project_folder, label_color_map):
    with open('{}/{}'.format(project_folder, label_color_file_name), 'w') as outfile:
        json.dump(label_color_map, outfile)


def extract_label_color_map(project_folder):
    with open('{}/{}'.format(project_folder, label_color_file_name)) as file:
        label_color_map = json.load(file)

    return label_color_map
