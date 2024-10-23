# Camera class

import RT_utility as rtu
import RT_ray as rtr

import numpy as np
import math
from PIL import Image as im

class Camera:
    def __init__(self) -> None:
        self.img_spectrum = 3
        self.aspect_ratio = 16.0/9.0
        self.img_width = 400
        self.center = rtu.Vec3()
        self.intensity = rtu.Interval(0.000, 0.999)
        self.samples_per_pixel = 10
        self.vertical_fov = 90
        self.look_from = rtu.Vec3(0, 0, -1)
        self.look_at = rtu.Vec3(0, 0, 0)
        self.vec_up = rtu.Vec3(0, 1, 0)

        self.Lens = None

        self.one_over_sqrt_spp = 1.0/math.sqrt(self.samples_per_pixel)

        self.defocus_disk_u = rtu.Vec3()
        self.defocus_disk_v = rtu.Vec3()

        self.init_camera()
        pass

    def compute_img_height(self):
        h = int(self.img_width / self.aspect_ratio)
        return  h if h > 1 else 1
    
    def init_camera(self,fDefocusAngle=0.0, fFocusDist=10.0 ,fAperture = 0.1):
        self.set_Lens(fDefocusAngle, fFocusDist, fAperture)

        self.img_height = self.compute_img_height()
        self.center = self.look_from

        h = math.tan(math.radians(self.vertical_fov)/2.0)
        self.viewport_height = 2.0 * h * self.Lens.get_focus_dist()
        self.viewport_width = self.viewport_height * float(self.img_width/self.img_height)

        self.camera_frame_w = rtu.Vec3.unit_vector(self.look_from - self.look_at)
        self.camera_frame_u = rtu.Vec3.unit_vector(rtu.Vec3.cross_product(self.vec_up, self.camera_frame_w))
        self.camera_frame_v = rtu.Vec3.cross_product(self.camera_frame_w, self.camera_frame_u)

        self.viewport_u = self.camera_frame_u*self.viewport_width
        self.viewport_v = -self.camera_frame_v*self.viewport_height
        self.pixel_du = self.viewport_u / self.img_width
        self.pixel_dv = self.viewport_v / self.img_height

        self.viewport_upper_left = self.center - (self.camera_frame_w*self.Lens.get_focus_dist()) - self.viewport_u/2 - self.viewport_v/2
        self.pixel00_location = self.viewport_upper_left + (self.pixel_du+self.pixel_dv)*0.5
        self.film = np.zeros((self.img_height, self.img_width, self.img_spectrum))

        # compute defocus parameters.
        defocus_radius = self.Lens.get_focus_dist() * math.tan(math.radians(self.Lens.get_defocus_angle() * 0.5))
        self.defocus_disk_u = self.camera_frame_u * defocus_radius
        self.defocus_disk_v = self.camera_frame_v * defocus_radius
        # compute aperture parameters.
        self.focal_length = (self.look_from - self.look_at).len()
        F_num = self.Lens.get_aperture() * 2.0 * self.viewport_height
        aperture = self.focal_length / F_num
        self.aperture_disk_u = self.camera_frame_u * aperture
        self.aperture_disk_v = self.camera_frame_v * aperture

    # call right before init_camera()
    def set_Lens(self, fDefocusAngle, fFocusDist, fAperture):
        self.Lens = Thinlens(fDefocusAngle, fFocusDist, fAperture)

    def write_to_film(self, widthId, heightId, cPixelColor):
        # scaling with samples_per_pixel
        scale = 1.0/self.samples_per_pixel
    
        r = cPixelColor.r()*scale
        g = cPixelColor.g()*scale
        b = cPixelColor.b()*scale

        r = rtu.linear_to_gamma(r, 2.0)
        g = rtu.linear_to_gamma(g, 2.0)
        b = rtu.linear_to_gamma(b, 2.0)

        self.film[heightId,widthId,0] = self.intensity.clamp(r)
        self.film[heightId,widthId,1] = self.intensity.clamp(g)
        self.film[heightId,widthId,2] = self.intensity.clamp(b)


    def get_center_ray(self, i, j):
        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        ray_direction = pixel_center - self.center
        return rtr.Ray(self.center, ray_direction)

    def get_ray(self, i, j):
        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        pixel_sample = pixel_center + self.random_pixel_in_square(self.pixel_du, self.pixel_dv)

        ray_origin = self.center
        if self.Lens.get_defocus_angle() > 1e-06:
            ray_origin = self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin
        ray_time = rtu.random_double()              # an additional parameter for motion blur

        return rtr.Ray(ray_origin, ray_direction, ray_time)
    
    def get_jittered_ray(self, i, j, s_i, s_j):

        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        pixel_sample = pixel_center + self.pixel_sample_square(self.pixel_du, self.pixel_dv, s_i, s_j) * 0.5

        ray_origin = self.center
        if self.Lens.get_defocus_angle() > 1e-06:
            ray_origin = self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin
        ray_time = rtu.random_double() 

        return rtr.Ray(ray_origin, ray_direction, ray_time)

    def get_ray_aperture(self, i, j):
        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        pixel_sample = pixel_center + self.random_pixel_in_square(self.pixel_du, self.pixel_dv)

        ray_origin = self.center
        if self.Lens.get_aperture() > 1e-06:
            ray_origin = self.aperture_disk_sample()
        ray_direction = pixel_sample - ray_origin
        ray_time = rtu.random_double()              # an additional parameter for motion blur

        return rtr.Ray(ray_origin, ray_direction, ray_time)
    
    def get_jittered_ray_aperture(self, i, j, s_i, s_j):

        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        pixel_sample = pixel_center + self.pixel_sample_square(self.pixel_du, self.pixel_dv, s_i, s_j) * 0.5

        ray_origin = self.center
        if self.Lens.get_aperture() > 1e-06:
            ray_origin = self.aperture_disk_sample()
        ray_direction = pixel_sample - ray_origin
        ray_time = 0

        return rtr.Ray(ray_origin, ray_direction,ray_time)
    
    def random_pixel_in_square(self, vDu, vDv):
        px = -0.5 + rtu.random_double()
        py = -0.5 + rtu.random_double()
        return (vDu*px) + (vDv*py)

    def pixel_sample_square(self, vDu, vDv, s_i, s_j):
        px = -0.5 + self.one_over_sqrt_spp * (s_i + rtu.random_double())
        py = -0.5 + self.one_over_sqrt_spp * (s_j + rtu.random_double())
        return (vDu * px) + (vDv * py)

    # an additional defocus method --> To move the ray orgin away from its center by defecous parameters.
    def defocus_disk_sample(self):
        pp = rtu.Vec3.random_vec3_in_unit_disk()
        du = (self.defocus_disk_u * pp.x())
        dv = (self.defocus_disk_v * pp.y())
        return self.center + du + dv
    
    def aperture_disk_sample(self):
        pp = rtu.Vec3.random_vec3_in_unit_disk()
        du = (self.aperture_disk_u * pp.x())
        dv = (self.aperture_disk_v * pp.y())
        return self.center + du + dv


class Lens():
    def __init__(self) -> None:
        pass

class Thinlens(Lens):
    def __init__(self, fDefocusAngle=0.0, fFocusDist=10.0, fAperture = 0.1) -> None:
        super().__init__()
        
        self.defocus_angle = fDefocusAngle
        self.focus_distance = fFocusDist
        self.aperture = fAperture

    def get_focus_dist(self):
        return self.focus_distance
    def get_defocus_angle(self):
        return self.defocus_angle
    def get_aperture(self):
        return self.aperture

    