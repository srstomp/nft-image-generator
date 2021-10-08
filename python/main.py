from PIL import Image
import numpy as np
import random
import os
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logger = logging.getLogger()

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = f'{ROOT_DIR}/resources/'


def change_image_color(source, ):
    img = source.convert("RGB")

    data = img.getdata()

    new_image_data = []
    for item in data:
        # change all white (also shades of whites) pixels to yellow
        if item[0] in list(range(190, 256)):
            new_image_data.append((255, 204, 100))
        else:
            new_image_data.append(item)

    # update image data
    img.putdata(new_image_data)

    # save new image
    #img.save("test_image_altered_background.jpg")

    # show image in preview
    #img.show()


def generate_background():
    bg = Image.open(f'{RESOURCES_DIR}bg.png')
    bg = alt




def generate_image(index):
    '''
    :param index: int
    :return:
    '''
    logger.debug(f'Fetch base image')


def generate_batch(amount):
    logger.info(f'Started creating {amount} images')
    logger.info(RESOURCES_DIR)
    for i in range(amount):
        logger.info(f'Image {i} of {amount}')
        generate_image(i)


if __name__ == '__main__':
    generate_batch(100)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
