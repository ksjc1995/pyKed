from PIL import Image

def apply_rotation(image,degrees):
    switcher = {
        "ROTATE_30":image.rotate(30),
        "ROTATE_45":image.rotate(45),
        "ROTATE_90":image.rotate(90),
        "ROTATE_135":image.rotate(135),
        "ROTATE_180":image.rotate(180),
        "ROTATE_225":image.rotate(225),
        "ROTATE_270":image.rotate(270),
    }

    image = switcher.get(degrees, None)
    return image