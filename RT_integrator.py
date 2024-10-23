# a simple integrator class
# A ray is hit and then get the color.
# It is the rendering equation solver.
import RT_utility as rtu
import RT_ray as rtr
import RT_material as rtm
import math

class Integrator():
    def __init__(self, bDlight=True, bSkyBG=False) -> None:
        self.bool_direct_lighting = bDlight
        self.bool_sky_background = bSkyBG
        pass

    def compute_scattering(self, rGen_ray, scene, maxDepth):

        if maxDepth <= 0:
            return rtu.Color()

        # if the generated ray hits an object
        found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0.000001, rtu.infinity_number))
        if found_hit == True:
            # get the hit info
            hinfo = scene.getHitList()
            # get the material of the object
            hmat = hinfo.getMaterial()
            # compute scattering
            sinfo = hmat.scattering(rGen_ray, hinfo)
            # if no scattering (It is a light source)
            if sinfo is None:
                # return Le
                return hmat.emitting()


            Le = rtu.Color()
            # if direct lighting is enabled
            if self.bool_direct_lighting:
                # for each point light
                for light in scene.point_light_list:
                    # check if there is an occlusion between a point light and a surface point.
                    tolight_dir = light.center - hinfo.getP()
                    tolight_ray = rtr.Ray(hinfo.getP(), tolight_dir)
                    max_distance = tolight_dir.len()
                    occlusion_hit = scene.find_occlusion(tolight_ray, rtu.Interval(0.000001, max_distance))
                    # if not occluded.
                    if not occlusion_hit:
                        # accumulate all unoccluded light
                        Le_BRDF = hmat.BRDF(rGen_ray, tolight_ray, hinfo)
                        # Le = Le + (Le_BRDF * light.material.emitting() * min(1.0, 1.0/max_distance))
                        NdotLe = rtu.Vec3.dot_product(hinfo.getNormal(), tolight_dir)
                        if NdotLe < 1e-06:
                            NdotLe = 0.0
                        direct_L_i = light.material.emitting()
                        Le = Le + (Le_BRDF * direct_L_i * NdotLe)

            # return the color
            # Le*attennuation_color upto the point before reflection models otherwise it is not correct.
            NdotL = rtu.Vec3.dot_product(hinfo.getNormal(), sinfo.scattered_ray.getDirection())
            if NdotL < 1e-06:
                NdotL = 0.0
            L_i = self.compute_scattering(sinfo.scattered_ray, scene, maxDepth-1)
            Fr =  hmat.BRDF(rGen_ray, sinfo.scattered_ray, hinfo)
            return Le + ( Fr * L_i * NdotL )

        if self.bool_sky_background:
            return scene.get_sky_background_color(rGen_ray)
        return scene.getBackgroundColor()

