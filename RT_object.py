# object class
import numpy as np
import RT_utility as rtu
import math

class Object:
    def __init__(self) -> None:
        self.moving_center = None       # where to the sphere moves to
        self.is_moving = False          # is it moving ?
        self.moving_dir = None          # moving direction
    pass

    def intersect(self, rRay, cInterval):
        pass
    
    def add_moving(self, vCenter):
        self.moving_center = vCenter
        self.is_moving = True
        self.moving_dir = self.moving_center - self.center

    def move_sphere(self, fTime):
        return self.center + self.moving_dir*fTime


class Sphere(Object):
    def __init__(self, vCenter, fRadius, mMat=None) -> None:
        super().__init__()
        self.center = vCenter
        self.radius = fRadius
        self.material = mMat
        
        self.moving_center = None       # where to the sphere moves to
        self.is_moving = False          # is it moving ?
        self.moving_dir = None          # moving direction

    def add_material(self, mMat):
        self.material = mMat

    def printInfo(self):
        self.center.printout()        
    
    def intersect(self, rRay, cInterval):        

        # check if the sphere is moving then move center of the sphere.
        sphere_center = self.center
        if self.is_moving:
            sphere_center = self.move_sphere(rRay.getTime())

        oc = rRay.getOrigin() - sphere_center
        a = rRay.getDirection().len_squared()
        half_b = rtu.Vec3.dot_product(oc, rRay.getDirection())
        c = oc.len_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c 

        if discriminant < 0:
            return None
        sqrt_disc = math.sqrt(discriminant)

        root = (-half_b - sqrt_disc) / a 
        if not cInterval.surrounds(root):
            root = (-half_b + sqrt_disc) / a 
            if not cInterval.surrounds(root):
                return None
            
        hit_t = root
        hit_point = rRay.at(root)
        hit_normal = (hit_point - sphere_center) / self.radius
        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)
        hinfo.set_face_normal(rRay, hit_normal)

        # set uv coordinates for texture mapping
        fuv = self.get_uv(hit_normal)
        hinfo.set_uv(fuv[0], fuv[1])

        return hinfo

    # return uv coordinates of the sphere at the hit point.
    def get_uv(self, vNormal):
        theta = math.acos(-vNormal.y())
        phi = math.atan2(-vNormal.z(), vNormal.x()) + math.pi

        u = phi / (2*math.pi)
        v = theta / math.pi
        return (u,v)

# Ax + By + Cz = D
class Quad(Object):
    def __init__(self, vQ, vU, vV, mMat=None) -> None:
        super().__init__()
        self.Qpoint = vQ
        self.Uvec = vU
        self.Vvec = vV
        self.material = mMat
        self.uxv = rtu.Vec3.cross_product(self.Uvec, self.Vvec)
        self.normal = rtu.Vec3.unit_vector(self.uxv)
        self.D = rtu.Vec3.dot_product(self.normal, self.Qpoint)
        self.Wvec = self.uxv / rtu.Vec3.dot_product(self.uxv, self.uxv)

    def add_material(self, mMat):
        self.material = mMat

    def intersect(self, rRay, cInterval):
        denom = rtu.Vec3.dot_product(self.normal, rRay.getDirection())
        # if parallel
        if rtu.Interval.near_zero(denom):
            return None

        # if it is hit.
        t = (self.D - rtu.Vec3.dot_product(self.normal, rRay.getOrigin())) / denom
        if not cInterval.contains(t):
            return None
        
        hit_t = t
        hit_point = rRay.at(t)
        hit_normal = self.normal

        # determine if the intersection point lies on the quad's plane.
        planar_hit = hit_point - self.Qpoint
        alpha = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(planar_hit, self.Vvec))
        beta = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(self.Uvec, planar_hit))
        if self.is_interior(alpha, beta) is None:
            return None

        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)
        hinfo.set_face_normal(rRay, hit_normal)

        # set uv coordinates for texture mapping
        hinfo.set_uv(alpha, beta)

        return hinfo
    
    def is_interior(self, fa, fb):
        delta = 0   
        if (fa<delta) or (1.0<fa) or (fb<delta) or (1.0<fb):
            return None

        return True


class Triangle(Object):
    def __init__(self) -> None:
        super().__init__()

    def intersect(self, rRay, cInterval):
        return super().intersect(rRay, cInterval)
    
class Cylinder(Object):
    def __init__(self, vCenter, cRadius, cHeight, vAxisDirection,mMat=None)->None:
        self.center = vCenter
        self.radius = cRadius
        self.height = cHeight
        self.axis_direction = rtu.Vec3.normalize(vAxisDirection)
        self.material = mMat
        
        self.moving_center = None       # where to the sphere moves to
        self.is_moving = False          # is it moving ?
        self.moving_dir = None          # moving direction
    
    def add_moving(self, vCenter):
        self.moving_center = vCenter
        self.is_moving = True
        self.moving_dir = self.moving_center - self.center

    def move_sphere(self, fTime):
        return self.center + self.moving_dir*fTime
      
    def intersect(self, rRay,cInterval):

        obj_center = self.center
        if self.is_moving:
            obj_center = self.move_sphere(rRay.getTime())
        
        # Step 1: Define the vector from the ray origin to the cylinder center
        oc = rRay.getOrigin() - obj_center

        # Step 2: Calculate coefficients for quadratic equation: A*t^2 + B*t + C = 0
        d_dot_a = rtu.Vec3.dot_product(rRay.getDirection(),self.axis_direction)
        #np.dot(ray.getDirection(), self.axis_direction)

        oc_dot_a = rtu.Vec3.dot_product(oc,self.axis_direction)
        #np.dot(oc, self.axis_direction)

        a = rtu.Vec3.dot_product(rRay.getDirection(), rRay.getDirection()) - d_dot_a**2
        #np.dot(ray.getDirection(), ray.getDirection())
        b = 2 * (rtu.Vec3.dot_product(rRay.getDirection(),oc) - d_dot_a * oc_dot_a)
        #np.dot(ray.direction, oc)
        c = rtu.Vec3.dot_product(oc,oc) - oc_dot_a**2 - self.radius**2
        #np.dot(oc, oc)
        # Step 3: Solve the quadratic equation for t
        discriminant = (b*b) - (4 * a * c)

        if discriminant < 0:
            return None  # No intersection

        # Two possible solutions for t
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        
        for t in [t1, t2]:
            if t < 0 or not cInterval.surrounds(t):
                continue  # Ignore negative t (behind the ray origin)

            # Calculate intersection point
            intersection_point = rRay.getOrigin() + rRay.getDirection()* t

            # Project the intersection point onto the cylinder's axis
            height_projection = rtu.Vec3.dot_product(intersection_point - self.center, self.axis_direction)
            if rtu.Interval(0,self.height).contains(height_projection):
                # Valid intersection within cylinder bounds

                # Calculate the normal at the hit point
                point_on_axis = self.center + self.axis_direction * height_projection
                hit_normal = rtu.Vec3.normalize(intersection_point - point_on_axis)

                # Create hit information
                hinfo = rtu.Hitinfo(intersection_point, hit_normal, t, self.material)
                hinfo.set_face_normal(rRay, hit_normal)

                # Optional: Set UV coordinates for texture mapping
                u, v = self.get_uv(hit_normal)
                hinfo.set_uv(u, v)

                return hinfo

        return None
    
    def get_uv(self, vNormal):
        # Vector from cylinder center to the point on the surface
        point_to_center = vNormal - self.center

        # Calculate 'v' coordinate (height-based)
        v = rtu.Vec3.dot_product(point_to_center, self.axis_direction) / self.height  # normalize v to be between 0 and 1


        # Calculate 'u' coordinate (angle-based around the cylinder)
        theta = np.arctan2(self.radius, self.radius)
        u = (theta + rtu.pi) / (2 * rtu.pi)  # normalize u to be between 0 and 1

        return u, v
    
    def printInfo(self):
        self.center.printout()

    def add_material(self, mMat):
        self.material = mMat
    
class Capsule(Object):
    def __init__(self, start_point, end_point, radius, material=None):
        self.start_point = start_point  # จุดเริ่มต้นของแคปซูล
        self.end_point = end_point      # จุดปลายของแคปซูล
        self.center = end_point - start_point
        self.radius = radius            # รัศมีของแคปซูล
        self.material = material        # วัสดุของแคปซูล
        
        self.moving_center = None       # where to the sphere moves to
        self.is_moving = False          # is it moving ?
        self.moving_dir = None          # moving direction
    
    def add_moving(self, vCenter):
        self.moving_center = vCenter
        self.is_moving = True
        self.moving_dir = self.moving_center - self.center

    def move_sphere(self, fTime):
        return self.center + self.moving_dir*fTime
    
    def intersect(self, rRay, cInterval):
        obj_center = self.center
        if self.is_moving:
            obj_center = self.move_sphere(rRay.getTime())
            
        # 1. คำนวณข้อมูลสำหรับทรงกระบอกส่วนตรงกลาง
        cylinder_direction = rtu.Vec3.normalize(obj_center)
        
        cylinder_start = self.start_point + cylinder_direction * self.radius
        cylinder_end = self.end_point - cylinder_direction * self.radius
        adjusted_length = math.sqrt(rtu.Vec3.dot_product(cylinder_end - cylinder_start, cylinder_end - cylinder_start))

        # แปลงทรงกระบอกกลางของแคปซูลให้เป็นวัตถุ Cylinder
        cylinder = Cylinder(cylinder_start, self.radius, adjusted_length, cylinder_direction, self.material)
        hinfo_cylinder = cylinder.intersect(rRay, cInterval)

        # 2. ตรวจจับการชนกับทรงกลมที่ปลายทั้งสองด้าน
        sphere_start = Sphere(self.start_point, self.radius, self.material)
        sphere_end = Sphere(self.end_point, self.radius, self.material)
        
        hinfo_sphere_start = sphere_start.intersect(rRay, cInterval)
        hinfo_sphere_end = sphere_end.intersect(rRay, cInterval)

        # 3. เลือกผลการชนที่ใกล้ที่สุดจากการตรวจจับทั้งหมด , hinfo_sphere_start, hinfo_sphere_end
        hit_infos = [hinfo for hinfo in [hinfo_cylinder, hinfo_sphere_start, hinfo_sphere_end] if hinfo]
        if not hit_infos:
            return None

        # ส่งคืนข้อมูลการชนที่ใกล้ที่สุด
        closest_hit = min(hit_infos, key=lambda hinfo: hinfo.t)
        return closest_hit
    
    def add_material(self, material):
        self.material = material