import json
import os
import shutil
from . import utils
from . import images
from . import labels

projects_file = 'projects.json'


def get_projects_state():
    print(os.getcwd())
    with open(projects_file) as outfile:
        data = json.load(outfile)

    return data['projects']


def add_project(new_project):
    projects = get_projects_state()

    if any(obj['projectName'] == new_project['projectName'] for obj in projects):
        print('project {} name already exist'.format(new_project['projectName']))
    else:
        new_project['projectFolder'] = new_project['projectName'].replace(" ", "_")
        projects.append(new_project)
        save_projects_to_file(projects)
        #crop-data
        if not os.path.exists(new_project['projectFolder']):
             os.makedirs(new_project['projectFolder'])
        #static sym link
        if not os.path.exists('static/{}'.format(new_project['projectFolder'])):
             os.makedirs('static/{}'.format(new_project['projectFolder']))
        generate_files_for_project(new_project)

        #labels file
        with open('{}/{}'.format(new_project['projectFolder'], labels.label_file_name), "w") as label_file:
            label_file.write("")
        #label color map file
        with open('{}/{}'.format(new_project['projectFolder'], labels.label_color_file_name), "w") as label_file:
            label_file.write("{}")

    return projects


def remove_project(project_name):
    projects = get_projects_state()
    project_to_remove_index = -1
    project_to_remove = None
    for i, project in enumerate(projects):
        if project['projectName'] == project_name:
            project_to_remove_index = i
            project_to_remove = project
            break

    if project_to_remove_index > -1:
        del projects[project_to_remove_index]
        save_projects_to_file(projects)
        shutil.rmtree(project_to_remove['projectFolder'])
        shutil.rmtree('static/{}'.format(project_to_remove['projectFolder']))

    return projects


def select_project(project_name):
    projects = get_projects_state()
    for i, project in enumerate(projects):
        if project['projectName'] == project_name:
            selected_project = project
            return selected_project
            break


def save_projects_to_file(projects):
    datas = {'projects': projects}
    with open(projects_file, 'w') as outfile:
        json.dump(datas, outfile)


def generate_files_for_project(project):

    images_name = 'images'
    images_path = project['projectPath']
    images_folder = project['projectFolder']

    if not os.path.exists(images_path):
        images_path = '{}/{}/'.format(images_path, images_name)
        os.mkdir('images_path')
        print("Directory ", images_path, " Created ")
    else:
        print("Directory ", images_path, " already created ")

    utils.create_symbolyc_lnk(images_path, images_folder)

    images.init_images_files(images_folder, images_path)


