from PIL import Image
from PIL import ImageColor
import numpy as np
import random
import os
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logger = logging.getLogger()

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = f'{ROOT_DIR}/resources'
DESTINATION_DIR = f'{ROOT_DIR}/generated'

def get_random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))


def change_image_color(src, org_color, new_color):
    im = Image.open(src)
    im = im.convert('RGBA')
    data = np.array(im)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    rgb = ImageColor.getrgb(org_color)
    areas = (red == rgb[0]) & (blue == rgb[1]) & (green == rgb[2])
    data[..., :-1][areas.T] = new_color  # Transpose back needed

    return Image.fromarray(data)


def generate_background():
    return change_image_color(f'{RESOURCES_DIR}/bg.png', '#FFFFFF', get_random_color())


def save_image(img, name):
    img = img.resize((1000, 1000),Image.NEAREST)
    #img.save(f'{DESTINATION_DIR}/{name}.png')
    img.show()


def generate_image(index):
    '''
    :param index: int
    :return:
    '''
    logger.debug(f'Fetch base image')
    image = generate_background()

    image.show()
    save_image(image, 'blabla')


def generate_batch(amount, file_name):
    logger.info(f'Started creating {amount} images')
    for i in range(amount):
        logger.info(f'Image {i} of {amount}')
        generate_image(f'{file_name}_{i}')


if __name__ == '__main__':
    generate_batch(1, 'letter')