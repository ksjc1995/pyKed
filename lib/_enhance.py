from PIL import ImageEnhance

def contrast(image,val):
    _image = ImageEnhance.Contrast(image)
    return _image.enhance(val)

def brightness(image,val):
    _image = ImageEnhance.Brightness(image)
    return _image.enhance(val)

def color_balance(image,val):
    _image = ImageEnhance.Color(image)
    return _image.enhance(val)

def sharpness(image,val):
    _image = ImageEnhance.Sharpness(image)
    return  _image.enhance(val)
