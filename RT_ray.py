# Ray class
import RT_utility as rtu

class Ray:
    def __init__(self, vOrigin=rtu.Vec3(), vDir=rtu.Vec3(), fTime=0.0) -> None:
        self.origin = vOrigin
        self.direction = vDir
        self.time = fTime       # an additional parameter to implement motion blur
        pass

    def at(self, t):
        return self.origin + self.direction*t

    def getOrigin(self):
        return self.origin
    
    def getDirection(self):
        return self.direction
    
    def getTime(self):
        return self.time
    

