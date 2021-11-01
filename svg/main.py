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

if __name__ == '__main__':
    generate_batch(10, 'coin')