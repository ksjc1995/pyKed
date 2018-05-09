def convert_to_grayscale(image_copy):
    """method to convert image to grayscale"""
    #getting pixel map
    pixels = image_copy.load()
    value  = 0
    #converting each pixel rgba to grayscale
    for i in range(image_copy.size[0]):
        for j in range(image_copy.size[1]):
            value = pixels[i,j][0]//3
            pixels[i,j] = (value, value, value)
    
    return image_copy