import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import importlib

from cropLabel import projects
from . import labels
from . import images
from . import cropdata
from cropLabel.plugins import plugins

from django.views.decorators.csrf import csrf_protect

included_extensions = ['jpg', 'bmp', 'png', 'gif']


# healthcheck returns status 200
def healthcheck(request):
    return HttpResponse(status=200)

@csrf_protect
def cropPicture(request):

    body_string = request.body.decode('utf8').replace("'", '"')
    body = json.loads(body_string)
    print(request.body)

    # request should have a project folder
    project_folder = body['project_folder']

    # request should have the fresh list of labels
    label_list = body['label_list']
    # save to label file
    labels.save_label_to_file(body['project_folder'], label_list)

    # save/update label color map
    label_color_map = body['label_color_map']
    labels.save_label_color_to_file(body['project_folder'], label_color_map)

    # get image name
    image_name = body['image_name']
    # get json file
    img_crop_data = cropdata.load_image_crop_data(project_folder, image_name)

    # get image label list
    image_label_list = body['image_label_list']
    # update file

    # check first if is not empty
    if len(image_label_list) > 0:
        # save capture in the corresponding label file
        for image_data in image_label_list:
            lbl = image_data['label']
            img_crop_data[lbl] = image_data
    else:
        img_crop_data = {}

    cropdata.save_capture_to_file(project_folder, img_crop_data, image_name + '.json')

    return JsonResponse({'project': project_folder, 'message': image_name + 'crops updated'}, status=200)


## remove label cropped data from file
@csrf_protect
def removedCropped(request):
    body_string = request.body.decode('utf8').replace("'", '"')
    body = json.loads(body_string)
    print(request.body)

    # request should have a project folder
    project_folder = body['project_folder']
    image_name = body['image_name']
    label = body['label'];

    # get json file
    img_crop_data = cropdata.load_image_crop_data(project_folder, image_name)
    lbl = label['label']
    del img_crop_data[lbl]

    cropdata.save_capture_to_file(project_folder, img_crop_data, image_name + '.json')

    return JsonResponse({'project': project_folder, 'message': '{} crops removed from {}'.format(label, image_name)}, status=200)



def listImages(request):
    # move to init
    obj = images.listImages()
    if obj is not None:
        return JsonResponse(json.dumps(obj), safe=False)
    else:
        return JsonResponse({'status': 'false', 'message': 'no images folder'}, status=500)


@csrf_protect
def retrieveCaptured(request):
    body_string = request.body.decode('utf8').replace("'", '"')
    body = json.loads(body_string)

    project_name = body['projectName']
    image_name = body['imageName']
    selected_project = projects.select_project(project_name)
    captured = cropdata.load_image_crop_data(selected_project['projectFolder'], image_name)

    if request.method == 'POST':
            return JsonResponse({'captured': captured, 'message': 'image captured {} retrieved'.format(image_name)})

    return JsonResponse({'status': 'false', 'message': 'unreasonable request'}, status=500)


def init(request):
    project_name = request.GET.get('project', '')
    print('requesting project {}'.format(project_name))
    selected_project = projects.select_project(project_name)

    images_list = images.images_list(selected_project)
    crop_object = cropdata.list_crop_data(selected_project)

    if len(images_list) > 0:
        context = {
            'imagesReady': 1,
            'projectName': selected_project['projectName'],
            'projectFolder': selected_project['projectFolder'],
            'imglist': str(images_list),
            'cropDataList': crop_object['cropdata'],
            'imgFormat': '.png',
            'imgPath': '/static/{}/data/'.format(selected_project['projectFolder']),
            'labels': labels.get_labels_from_file(selected_project['projectName']),
            'imgInit': images_list[0],
            'existingCaptures': cropdata.load_image_crop_data(selected_project['projectFolder'], images_list[0]),
            'labelColors': labels.extract_label_color_map(selected_project['projectFolder']),
            'plugins': plugins.getPlugins()
        }
        return render(request, 'init.html', context=context)
    else:
        project_list = projects.get_projects_state()
        context = {
            'project_list': project_list,
                'projectName': selected_project['projectName'],
                   'projectFolder': selected_project['projectFolder'],
                   'imagesReady': 0
                   }
        return render(request, 'index.html', context=context)



# initial page create/select project

def index(request):
    print('request init')
    project_list = projects.get_projects_state()
    context = {
        'imagesReady': 1,
        'project_list': project_list
    }

    return render(request, 'index.html', context=context)


@csrf_protect
def createProject(request):

    if request.method=='POST':
        body_string = request.body.decode('utf8').replace("'", '"')
        new_project = json.loads(body_string)
        prjct_list = projects.add_project(new_project)
        return JsonResponse({'projects': prjct_list, 'message': 'new project created'})

    return JsonResponse({'status': 'false', 'message': 'unreasonable request'}, status=500)


def deleteProject(request, project_name):
    print(project_name)
    project_list = projects.remove_project(project_name)

    if request.method == 'GET':
            return JsonResponse({'projects': project_list, 'message': 'project {} deleted'.format(project_name)})

    return JsonResponse({'status': 'false', 'message': 'unreasonable request'}, status=500)


@csrf_protect
def process(request):
    if request.method == 'POST':
        body_string = request.body.decode('utf8').replace("'", '"')
        process_request = json.loads(body_string)
        prjct = process_request['projectName']
        model = process_request['model']

        # TODO move to its respetive file
        #get plugin
        plugin = plugins.plugins_map[model]

        # build transformer
        to_import = 'cropLabel.plugins.{}.{}'.format(model, plugin['transformer'][:-len('.py')])
        builder = importlib.import_module(to_import)
        transformer = builder.buildTransformer();
        selected_project = projects.select_project(prjct)
        if selected_project is not None:
            transformer.transform(selected_project)
            return JsonResponse({'project': prjct, 'message': 'process model:{}'.format(model)})

    return JsonResponse({'status': 'false', 'message': 'unreasonable request'}, status=500)
