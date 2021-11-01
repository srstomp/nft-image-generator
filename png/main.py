from PIL import Image
from PIL import ImageColor
import numpy as np
import random
import os
import logging
import json

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger()

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = f'{ROOT_DIR}/resources'
DESTINATION_DIR = f'{ROOT_DIR}/generated'

def combine(img, top):
    img.paste(top, (0, 0), mask = top) # combine image at the top left corner
    return img


def get_random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))


def change_image_color(src, org_hex_color, new_rgb_color):
    """
    Change color of image

    :param src: the source image object
    :param org_hex_color: original color in hex format
    :param new_rgb_color: new color in rgb format
    :return: the updated image object
    """

    im = src.convert('RGBA')
    data = np.array(im)
    red, green, blue, alpha = data.T

    rgb = ImageColor.getrgb(org_hex_color)
    areas = (red == rgb[0]) & (green == rgb[1]) & (blue == rgb[2])
    data[..., :-1][areas.T] = new_rgb_color

    return Image.fromarray(data)


def generate_image_asset(item):
    img = Image.open(f'{RESOURCES_DIR}/{item["file"]}')
    for c in item['colors']: # Loop through every color and change it
        img = change_image_color(img, c, get_random_color())
    return img


def generate_background():
    img = Image.open(f'{RESOURCES_DIR}/bg.png') # Retrieve background source file
    return change_image_color(img, '#FFFFFF', get_random_color())


def save_image(img, name):
    '''
    Resize image in the best quality and save image

    :param img: the combined image
    :param name: file name string
    :return: no value
    '''
    img = img.resize((2000, 2000),Image.LANCZOS)
    img.save(f'{DESTINATION_DIR}/{name}.png')


def generate_image(index):
    """
    Generate image. Steps:
    - Generate image layers
    - Combine images
    - Save to file

    :param index: int
    :return: no value
    """

    logger.info(f'Fetch base image')
    image = generate_background()

    f = open(os.path.join(os.path.dirname(__file__), 'resources/data.json'), 'r') # fetch image resources
    data = json.load(f)

    for i in data['assets']:
        weights = [x['weight']/100 for x in i['items']] # create a new array of only the probabilities
        weighted_choice = np.random.choice(i['items'], 1, p=weights)[0]
        logger.info(f'Weighted choice: {weighted_choice}')
        combine(image, generate_image_asset(weighted_choice))

    save_image(image, f'{data["name"]}_{index}')


def generate_batch(amount, file_name):
    logger.info(f'Started creating {amount} images')
    for i in range(amount):
        logger.info(f'Image {i} of {amount}')
        generate_image(f'{file_name}_{i}')


if __name__ == '__main__':
    generate_batch(10, 'letter')