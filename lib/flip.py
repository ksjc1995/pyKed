from random import choice
from PIL import Image
def flip_image(image_copy):
    """method to flip image (top-bottom or left-right)"""
    prop = choice([Image.FLIP_LEFT_RIGHT,Image.FLIP_TOP_BOTTOM])
    image_copy = image_copy.transpose(prop)
    return image_copy
