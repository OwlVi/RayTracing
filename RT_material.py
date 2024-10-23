# material class
import RT_utility as rtu
import RT_ray as rtr
import math
import RT_texture as rtt

def reflect(vRay, vNormal):
    # return the perfect reflection direction
    return vRay - vNormal*rtu.Vec3.dot_product(vRay, vNormal)*2.0

def refract(vRay, vNormal, fRefractRatio):
    cos_theta = min(rtu.Vec3.dot_product(-vRay, vNormal), 1.0)
    sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)
    cannot_refract = fRefractRatio*sin_theta > 1.0

    if cannot_refract or schlick(cos_theta, fRefractRatio) > rtu.random_double():
        return reflect(vRay, vNormal)
    else:
        perpendiular_dir = (vRay + vNormal*cos_theta)*fRefractRatio
        parallel_dir = vNormal*(-math.sqrt(math.fabs(1.0 - perpendiular_dir.len_squared())))
        return perpendiular_dir + parallel_dir

def halfvector(vView, vLight):
    vH = (vView + vLight)*0.5
    return vH

def schlick(fCosine, fIOR):
    r0 = (1-fIOR) / (1+fIOR)
    r0 = r0*r0
    return r0 + (1-r0)*math.pow(1-fCosine, 5)

class Material:
    def __init__(self) -> None:
        pass

    def scattering(self, rRayIn, hHinfo):
        pass

    def is_light(self):
        return False

class Lambertian(Material):
    def __init__(self, cAlbedo) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())

    def scattering(self, rRayIn, hHinfo):
        uvw = rtu.ONB()
        uvw.build_from_w(hHinfo.getNormal())

        scattered_direction = uvw.local(rtu.Vec3.random_cosine_hemisphere_on_z())
        scattered_ray = rtr.Ray(hHinfo.getP(), scattered_direction, rRayIn.getTime())
        attenuation_color = self.BRDF(rRayIn, scattered_ray, hHinfo)
        return rtu.Scatterinfo(scattered_ray, attenuation_color)

    def BRDF(self, rView, rLight, hHinfo):
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())
        return attenuation_color


# a mirror class
class Mirror(Material):
    def __init__(self, cAlbedo) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())

    def scattering(self, rRayIn, hHinfo):
        # generate a reflected ray
        reflected_ray = rtr.Ray(hHinfo.getP(), reflect(rRayIn.getDirection(), hHinfo.getNormal()), rRayIn.getTime())

        # get attenuation_color
        attenuation_color = self.BRDF(rRayIn, reflected_ray, hHinfo)

        # return scattering info
        return rtu.Scatterinfo(reflected_ray, attenuation_color)

    def BRDF(self, rView, rLight, hHinfo):
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())
        return attenuation_color


# A dielectric transparent material 
class Dielectric(Material):
    def __init__(self, cAlbedo, fIor) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.IOR = fIor

    def scattering(self, rRayIn, hHinfo):
        refract_ratio = self.IOR
        if hHinfo.front_face:
            refract_ratio = 1.0/self.IOR

        # generate a refracted ray
        uv = rtu.Vec3.unit_vector(rRayIn.getDirection())
        refracted_dir = refract(uv, hHinfo.getNormal(), refract_ratio)
        scattered_ray = rtr.Ray(hHinfo.getP(), refracted_dir, rRayIn.getTime())

        attenuation_color = self.BRDF(rRayIn, scattered_ray, hHinfo)
        # return scattering info
        return rtu.Scatterinfo(scattered_ray, attenuation_color)

    def BRDF(self, rView, rLight, hHinfo):
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())
        return attenuation_color

# a texture
class TextureColor(Material):
    def __init__(self, color_or_texture) -> None:
        super().__init__()
        if isinstance(color_or_texture, rtu.Color):
            self.color_albedo = rtt.SolidColor(color_or_texture)
        else:
            self.color_albedo = color_or_texture

    def scattering(self, rRayIn, hHinfo):
        uvw = rtu.ONB()
        uvw.build_from_w(hHinfo.getNormal())
        scattered_direction = uvw.local(rtu.Vec3.random_cosine_hemisphere_on_z())

        scattered_ray = rtr.Ray(hHinfo.getP(), scattered_direction, rRayIn.getTime())
        attenuation_color = self.BRDF(rRayIn, scattered_ray, hHinfo)

        return rtu.Scatterinfo(scattered_ray, attenuation_color)

    def BRDF(self, rView, rLight, hHinfo):
        attenuation_color = self.color_albedo.tex_value(hHinfo.u, hHinfo.v, hHinfo.point)
        return attenuation_color


# A metal class with roughness parameter
class Metal(Material):
    def __init__(self, cAlbedo, fRoughness) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.roughness = fRoughness
        if self.roughness > 1.0:
            self.roughness = 1.0

    def scattering(self, rRayIn, hHinfo):
        # compute scattered ray based on the roughtness parameter
        reflected_direction = reflect(rtu.Vec3.unit_vector(rRayIn.getDirection()), hHinfo.getNormal()) + rtu.Vec3.random_vec3_unit()*self.roughness
        reflected_ray = rtr.Ray(hHinfo.getP(), reflected_direction, rRayIn.getTime())
        attenuation_color = self.BRDF(rRayIn, reflected_ray, hHinfo)

        # check if the reflected direction is below the surface normal
        if rtu.Vec3.dot_product(reflected_direction, hHinfo.getNormal()) <= 1e-8:
            attenuation_color = rtu.Color(0,0,0)

        return rtu.Scatterinfo(reflected_ray, attenuation_color)

    def BRDF(self, rView, rLight, hHinfo):
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())
        return attenuation_color    

# Phong reflection model
# fr = kd + ks*(R.V)^roughness
class Phong(Material):
    def __init__(self, cAlbedo, kd, ks, fAlpha) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.kd = kd
        self.ks = ks
        self.alpha = fAlpha

    def scattering(self, rRayIn, hHinfo):
        uvw = rtu.ONB()
        uvw.build_from_w(hHinfo.getNormal())

        reflected_direction = uvw.local(rtu.Vec3.random_cosine_hemisphere_on_z())
        reflected_ray = rtr.Ray(hHinfo.getP(), reflected_direction, rRayIn.getTime())
        phong_color = self.BRDF(rRayIn, reflected_ray, hHinfo)

        return rtu.Scatterinfo(reflected_ray, phong_color)

    def BRDF(self, rView, rLight, hHinfo):
        # calculate diffuse color
        diff_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())*self.kd*(1.0/math.pi)

        perfect_reflection = rtu.Vec3.unit_vector(reflect(-rLight.getDirection(), hHinfo.getNormal()))
        viewingVector = rtu.Vec3.unit_vector(-rView.getDirection())
        R_dot_V = max(0, rtu.Vec3.dot_product(perfect_reflection, viewingVector))
        spec_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())*self.ks*math.pow(R_dot_V, self.alpha)

        return diff_color + spec_color
    

# Blinn-Phong reflection model
# fr = kd + ks*(H.N)^roughness
class Blinn(Material):
    def __init__(self, cAlbedo, kd, ks, fAlpha) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.kd = kd
        self.ks = ks
        self.alpha = fAlpha

    def scattering(self, rRayIn, hHinfo):
        uvw = rtu.ONB()
        uvw.build_from_w(hHinfo.getNormal())

        reflected_direction = uvw.local(rtu.Vec3.random_cosine_hemisphere_on_z())
        reflected_ray = rtr.Ray(hHinfo.getP(), reflected_direction, rRayIn.getTime())
        blinn_color = self.BRDF(rRayIn, reflected_ray, hHinfo)

        return rtu.Scatterinfo(reflected_ray, blinn_color)

    def BRDF(self, rView, rLight, hHinfo):
        # calculate diffuse color
        diff_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())*self.kd*(1.0/math.pi)

        half_vector = rtu.Vec3.unit_vector(halfvector(-rView.getDirection(), rLight.getDirection()))
        H_dot_N = max(0, rtu.Vec3.dot_product(half_vector, hHinfo.getNormal()))
        spec_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())*self.ks*math.pow(H_dot_N, self.alpha)

        return diff_color + spec_color

# Cook-Torrance BRDF model
# fr = kd/pi + ks*(DFG/4(w_o.N * w_i.N))
class CookTorrance(Material):
    def __init__(self, kd, ks, fAlpha, fIOR) -> None:
        super().__init__()
        self.kd = kd
        self.ks = ks
        self.alpha = fAlpha
        self.ior = fIOR

    def scattering(self, rRayIn, hHinfo):
        uvw = rtu.ONB()
        uvw.build_from_w(hHinfo.getNormal())

        reflected_direction = uvw.local(rtu.Vec3.random_cosine_hemisphere_on_z())
        reflected_ray = rtr.Ray(hHinfo.getP(), reflected_direction, rRayIn.getTime())
        ct_color = self.BRDF(rRayIn, reflected_ray, hHinfo)

        return rtu.Scatterinfo(reflected_ray, ct_color)

    def BRDF(self, rView, rLight, hHinfo):
        half_vector = rtu.Vec3.unit_vector(halfvector(-rView.getDirection(), rLight.getDirection()))
        vN = hHinfo.getNormal()
        V_dot_N = max(1e-08, rtu.Vec3.dot_product(-rView.getDirection(), vN))
        L_dot_N = max(1e-08, rtu.Vec3.dot_product(rLight.getDirection(), vN))

        dterm = self.Dterm_GGX(half_vector, vN, self.alpha)
        gterm1 = self.Gterm(-rView.getDirection(), half_vector, vN, self.alpha)
        gterm2 = self.Gterm(rLight.getDirection(), half_vector, vN, self.alpha)

        cos_theta = min(rtu.Vec3.dot_product(rLight.getDirection(), vN), 1.0)
        fterm = schlick(cos_theta, self.ior)

        denom = 1/(4 * V_dot_N * L_dot_N)
        # calculate diffuse color
        diff_color = self.kd/math.pi
        spec_color = self.ks * dterm * gterm1 * gterm2 * fterm * denom

        return diff_color + spec_color

    def chi_GGX(self, fVal):
        if fVal>1e-08:
            return 1.0
        return 0.0
    
    def Dterm_GGX(self, vH, vN, fAlpha):
        H_dot_N = max(1e-08, rtu.Vec3.dot_product(vH, vN))
        alpha2 = fAlpha*fAlpha
        H_dot_N2 = H_dot_N*H_dot_N
        tan2 = ( 1-H_dot_N2 ) / H_dot_N2
        denom = H_dot_N2 * (alpha2 + tan2)
        return (self.chi_GGX(H_dot_N) * alpha2) / (math.pi * denom * denom)

    def Gterm(self, vP, vH, vN, fAlpha):
        v_dot_H = max(1e-08, rtu.Vec3.dot_product(vP, vH))
        v_dot_N = max(1e-08, rtu.Vec3.dot_product(vP, vN))
        chi = self.chi_GGX(v_dot_H / v_dot_N)
        v_dot_H2 = v_dot_H * v_dot_H
        tan2 = ( 1 - v_dot_H2 ) / v_dot_H2
        return (chi * 2) / (1 + math.sqrt(1 + fAlpha*fAlpha*tan2))
    

