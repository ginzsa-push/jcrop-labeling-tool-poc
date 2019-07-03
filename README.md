# jcrop-labeling-tool-poc
This a POC trying to use Jcrop for labelling images

The application use the following libraries

Jcrop and Jquery for the front end app
Python 3.6 and Django for the appliction
OpenCv for image cropping


The application has two pages

First you create a project name, and set the images location path.

The second page show the images, with the ability to swap through them. It also an area can be selected and a label modal window where the user can create a new label or use an existing one.

The first implementation generates a formated files for YOLO model. It also generates de cropped images to build a classiffier.


## Django Execution

```
python manage.py runserver
```
