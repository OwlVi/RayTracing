# Texture class
import math
from PIL import Image as im
import RT_utility as rtu

class Texture:
    def __init__(self) -> None:
        pass

    def tex_value(self, fu, fv, vPoint):
        pass

# solid color as a texture
class SolidColor(Texture):
    def __init__(self, cColor) -> None:
        super().__init__()
        self.solid_color = cColor

    def tex_value(self, fu, fv, vPoint):
        return self.solid_color

# checker board as a texture    
class CheckerTexture(Texture):
    def __init__(self, fScale, cColor1, cColor2) -> None:
        super().__init__()
        self.inv_scale = 1.0/fScale
        self.even_texture = SolidColor(cColor1)
        self.odd_texture = SolidColor(cColor2)

    def tex_value(self, fu, fv, vPoint):

        xInteger = int(math.floor(vPoint.x()*self.inv_scale))
        yInteger = int(math.floor(vPoint.y()*self.inv_scale))
        zInteger = int(math.floor(vPoint.z()*self.inv_scale))

        isEven = (xInteger + yInteger + zInteger) % 2 == 0

        if isEven:
            return self.even_texture.tex_value(fu, fv, vPoint)
        
        return self.odd_texture.tex_value(fu, fv, vPoint)
    
# an PNG,JPG image as a texture
class ImageTexture(Texture):
    def __init__(self, strImgFilename) -> None:
        super().__init__()
        # read up image information
        self.invalid = False
        try:
            self.img = im.open(strImgFilename)
        except:
            print('The texture file could not be loaded.\n{}'.format(strImgFilename))
        if self.img.height <= 0:    # image is invalid.
            print(self.img.size)
            self.invalid = True
        if self.img.format.lower() == 'png'.lower() or self.img.format.lower() == 'jpeg'.lower():
            self.invalid = False
        else:
            print(self.img.format)
            self.invalid = True

    def __del__(self):
        self.img.close()
        print('closing texture.')

    def tex_value(self, fu, fv, vPoint):

        if self.invalid:
            return rtu.Color(0, 1, 1)
        
        # clamping values to (0,1)
        u = rtu.Interval(0, 1).clamp(fu)
        v = rtu.Interval(0, 1).clamp(fv)

        # scale to pixel location and get the pixel value
        i = int(u*self.img.width)
        j = int(v*self.img.height)
        pixel = self.img.getpixel((i,j))

        # return the pixel color of the texture
        # remember to scale the value to (0,1)
        scale = 1.0/255
        return rtu.Color(pixel[0]*scale, pixel[1]*scale, pixel[2]*scale)
    

