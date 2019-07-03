import os
import subprocess


def create_directory(dirName):
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    except FileExistsError:
        print("Directory ", dirName, " already exists")
    return dirName


#ln -s /export/space/common/archive /archive
# crate symbolic link to data
def create_symbolyc_lnk(image_path):
    subprocess.run(["ln", "-s", image_path, "./static/cropLabel/data"])


# create symbolic link to data
def create_symbolyc_lnk(image_path, project_folder):
    subprocess.run(["ln", "-s", image_path, "./static/{}/data".format(project_folder)])

# create folder if doesnt exist
def establish_path(path):
    folders = path.split("/")
    temp_path = ''
    for folder in folders:
        temp_path = temp_path + '/' + folder
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
