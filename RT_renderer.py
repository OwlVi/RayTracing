# renderer class

import RT_utility as rtu
import numpy as np
from PIL import Image as im
import math
import RT_pbar

class Renderer():

    def __init__(self, cCamera, iIntegrator, sScene) -> None:

        self.camera = cCamera
        self.integrator = iIntegrator
        self.scene = sScene
        pass

    def render(self):
        # gather lights to the light list
        self.scene.find_lights()
        renderbar = RT_pbar.start_animated_marker(self.camera.img_height*self.camera.img_width)
        k = 0
                
        for j in range(self.camera.img_height):
            for i in range(self.camera.img_width):

                pixel_color = rtu.Color(0,0,0)
                # shoot multiple rays at random locations inside the pixel
                for spp in range(self.camera.samples_per_pixel):
                    generated_ray = self.camera.get_ray(i, j)
                    pixel_color = pixel_color + self.integrator.compute_scattering(generated_ray, self.scene, self.camera.max_depth)

                self.camera.write_to_film(i, j, pixel_color)
                renderbar.update(k)
                k = k+1

    def render_aperture(self):
        # gather lights to the light list
        self.scene.find_lights()
        renderbar = RT_pbar.start_animated_marker(self.camera.img_height*self.camera.img_width)
        k = 0
                
        for j in range(self.camera.img_height):
            for i in range(self.camera.img_width):

                pixel_color = rtu.Color(0,0,0)
                # shoot multiple rays at random locations inside the pixel
                for spp in range(self.camera.samples_per_pixel):
                    generated_ray = self.camera.get_ray_aperture(i, j)
                    pixel_color = pixel_color + self.integrator.compute_scattering(generated_ray, self.scene, self.camera.max_depth)

                self.camera.write_to_film(i, j, pixel_color)
                renderbar.update(k)
                k = k+1

    def render_jittered(self):
        # gather lights to the light list
        self.scene.find_lights()
        renderbar = RT_pbar.start_animated_marker(self.camera.img_height*self.camera.img_width)
        k = 0
        sqrt_spp = int(math.sqrt(self.camera.samples_per_pixel))
                
        for j in range(self.camera.img_height):
            for i in range(self.camera.img_width):

                pixel_color = rtu.Color(0,0,0)
                # shoot multiple rays at random locations inside the pixel
                for s_j in range(sqrt_spp):
                    for s_i in range(sqrt_spp):

                        generated_ray = self.camera.get_jittered_ray(i, j, s_i, s_j)
                        pixel_color = pixel_color + self.integrator.compute_scattering(generated_ray, self.scene, self.camera.max_depth)

                self.camera.write_to_film(i, j, pixel_color)
                renderbar.update(k)
                k = k+1

    def render_jittered_aperture(self):
        # gather lights to the light list
        self.scene.find_lights()
        renderbar = RT_pbar.start_animated_marker(self.camera.img_height*self.camera.img_width)
        k = 0
        sqrt_spp = int(math.sqrt(self.camera.samples_per_pixel))
                
        for j in range(self.camera.img_height):
            for i in range(self.camera.img_width):

                pixel_color = rtu.Color(0,0,0)
                # shoot multiple rays at random locations inside the pixel
                for s_j in range(sqrt_spp):
                    for s_i in range(sqrt_spp):

                        generated_ray = self.camera.get_jittered_ray_aperture(i, j, s_i, s_j)
                        pixel_color = pixel_color + self.integrator.compute_scattering(generated_ray, self.scene, self.camera.max_depth)

                self.camera.write_to_film(i, j, pixel_color)
                renderbar.update(k)
                k = k+1

    def write_img2png(self, strPng_filename):
        png_film = self.camera.film * 255
        data = im.fromarray(png_film.astype(np.uint8))
        data.save(strPng_filename)

