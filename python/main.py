from PIL import Image
from PIL import ImageColor
import numpy as np
import random
import os
import logging
import json

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logger = logging.getLogger()

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = f'{ROOT_DIR}/resources'
DESTINATION_DIR = f'{ROOT_DIR}/generated'

def combine(img, top):
    img.paste(top, (0, 0), mask = top)
    return img


def get_random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))


def change_image_color(src, org_hex_color, new_rgb_color):
    '''
    Change color of image

    :param src: obj
    :param org_hex_color: string
    :param new_rgb_color: string
    :return:
    '''
    im = src.convert('RGBA')
    data = np.array(im)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    rgb = ImageColor.getrgb(org_hex_color)
    logger.debug(rgb)
    areas = (red == rgb[0]) & (green == rgb[1]) & (blue == rgb[2])
    data[..., :-1][areas.T] = new_rgb_color  # Transpose back needed

    return Image.fromarray(data)


def generate_image_asset(item):
    logger.debug(item)
    img = Image.open(f'{RESOURCES_DIR}/{item["file"]}')
    for c in item['colors']:
        logger.debug(c)
        img = change_image_color(img, c, get_random_color())

    return img


def generate_background():
    img = Image.open(f'{RESOURCES_DIR}/bg.png')
    return change_image_color(img, '#FFFFFF', get_random_color())


def save_image(img, name):
    img = img.resize((576, 720),Image.LANCZOS)
    img.save(f'{DESTINATION_DIR}/{name}.png')
    #img.show()


def generate_image(index):
    '''
    Generate image. Steps:
    - Generate image layers
    - Combine images
    - Save to file

    :param index: int
    :return:
    '''
    logger.debug(f'Fetch base image')
    image = generate_background()

    f = open(os.path.join(os.path.dirname(__file__), 'resources/data.json'), 'r')
    data = json.load(f)

    weighted_choice = lambda s: random.choice(sum(([v] * wt for v, wt in s), []))

    for i in data['assets']:
        if i['type'] == 'root':
            combine(image, generate_image_asset(i))
        if i['type'] == 'mouth':
            combine(image, generate_image_asset(random.choice(i['items'])))

    save_image(image, f'{data["name"]}_{index}')


def generate_batch(amount, file_name):
    logger.info(f'Started creating {amount} images')
    for i in range(amount):
        logger.info(f'Image {i} of {amount}')
        generate_image(f'{file_name}_{i}')


if __name__ == '__main__':
    generate_batch(100, 'letter')