from PIL import Image

def apply_rotation(image,degrees):
    switcher = {
        "ROTATE_45":image.rotate(45),
        "ROTATE_90":image.rotate(90),
        "ROTATE_135":image.rotate(135)
    }

    image = switcher.get(degrees, None)
    return image