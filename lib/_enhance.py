from PIL import ImageEnhance

def contrast(image,val):
    _image = ImageEnhance.Contrast(image)
    _image.enhance(val)
    return _image

def brightness(image,val):
    _image = ImageEnhance.Brightness(image)
    _image.enhance(val)
    return _image

def color_balance(image,val):
    _image = ImageEnhance.Color(image)
    _image.enhance(val)
    return _image

def sharpness(image,val):
    _image = ImageEnhance.Sharpness(image)
    _image.enhance(val)
    return _image