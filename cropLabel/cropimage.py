import cv2


def crop_image(image_path, destination_path, crop_work, name_format):

    img = cv2.imread(image_path)
    crop_img = img[crop_work.y:crop_work.y+crop_work.h, crop_work.x:crop_work.x+crop_work.w]
    file_name = name_format.format(destination_path, crop_work.image_name, crop_work.label)
    print('creating crop to file {}'.format(file_name))
    cv2.imwrite(file_name, img)

