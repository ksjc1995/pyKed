from PIL import ImageEnhance

def enhance_all(image,brightness,color_balance,sharpness,contrast):
    _image = ImageEnhance.Contrast(image)
    ic = _image.enhance(contrast)
    _image = ImageEnhance.Brightness(ic)
    ib = _image.enhance(brightness)
    _image = ImageEnhance.Sharpness(ib)
    ish = _image.enhance(sharpness)
    _image = ImageEnhance.Color(ish)
    return _image.enhance(color_balance)
    
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
