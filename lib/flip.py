
from PIL import Image
def flip_image(image_copy):
    """method to flip image (top-bottom or left-right)"""
    image_copy = image_copy.transpose(Image.FLIP_LEFT_RIGHT)
    return image_copy
