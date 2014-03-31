import os
import random
from django.conf import settings


def random_image(image_dir=''):
    try:
        valid_extensions = settings.RANDOM_IMAGE_EXTENSIONS
    except AttributeError:
        valid_extensions = ['.jpg','.jpeg','.png','.gif',]

    if image_dir:
        rel_dir = image_dir
    else:
        rel_dir = settings.RANDOM_IMAGE_DIR

    rand_dir = os.path.join(settings.STATIC_ROOT, rel_dir)
    files = [f for f in os.listdir(rand_dir) if os.path.splitext(f)[1] in valid_extensions]

    #Don't cache these images
    image = os.path.join(rel_dir, random.choice(files))
    image.split('.')[0].join('.').join(image.split('.')[-1])

    return image