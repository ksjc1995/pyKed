from PIL import ImageFilter

def apply_filter(image,filter_name):
    """method to apply filter to image"""
    switcher = {
        "BLUR":image.filter(ImageFilter.BLUR),
        "CONTOUR":image.filter(ImageFilter.CONTOUR),
        "DETAIL":image.filter(ImageFilter.DETAIL),
        "EDGE_ENHANCE":image.filter(ImageFilter.EDGE_ENHANCE),
        "EDGE_ENHANCE_MORE":image.filter(ImageFilter.EDGE_ENHANCE_MORE),
        "EMBOSS":image.filter(ImageFilter.EMBOSS),
        "FIND_EDGES":image.filter(ImageFilter.FIND_EDGES),
        "SHARPEN":image.filter(ImageFilter.SHARPEN),
        "SMOOTH":image.filter(ImageFilter.SMOOTH),
        "SMOOTH_MORE":image.filter(ImageFilter.SMOOTH_MORE)
    }
    image = switcher.get(filter_name, None)
    return image


    