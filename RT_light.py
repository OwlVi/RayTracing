# light class
import random
import RT_utility as rtu
import RT_material as rtm
import RT_ray as rtr

class Light(rtm.Material):
    def __init__(self) -> None:
        pass

    def scattering(self, rRayIn, hHinfo):
        return None

    def emitting(self):
        return rtu.Color(0,0,0)

    def is_light(self):
        return True

class Diffuse_light(Light):
    def __init__(self, cAlbedo) -> None:
        super().__init__()
        self.light_color = cAlbedo

    def scattering(self, rRayIn, hHinfo):
        return None
    
    def emitting(self):
        return self.light_color
    
class SaberLight(Light):
    def __init__(self, cAlbedo, intensity=4.0) -> None:
        super().__init__()
        self.light_color = cAlbedo
        self.intensity = intensity
        
    def emitting(self):
        return self.light_color * self.intensity
    
    def scattering(self, rRayIn, hHinfo):
        return None