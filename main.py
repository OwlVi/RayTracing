import RT_utility as rtu
import RT_camera as rtc
import RT_renderer as rtren
import RT_material as rtm
import RT_scene as rts
import RT_object as rto
import RT_integrator as rti
import RT_light as rtl
import RT_texture as rtt

pixel = 1920
spp = 100
mdepth = 5

def renderTest():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0/9.0
    main_camera.img_width = 320
    main_camera.center = rtu.Vec3(0,0,0)
    main_camera.samples_per_pixel = 10
    main_camera.max_depth = 5
    main_camera.vertical_fov = 60
    main_camera.look_from = rtu.Vec3(0, 0, 2)# (x rotation ,y rotation,z rotation)
    main_camera.look_at = rtu.Vec3(0, 0, -1)
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    defocus_angle = 2.0
    focus_distance = 5.0
    aperture = 1.0
    main_camera.init_camera(defocus_angle, focus_distance, aperture)
    
    # Setting Material
    
    light_red = rtl.SaberLight(rtu.Color(1,0.2,0.2))
    light_greed = rtl.SaberLight(rtu.Color(0.2,1,0.2))
    light_white = rtl.Diffuse_light(rtu.Color(1,1,1))
    metal_mat = rtm.Metal(rtu.Color(0.612,0.612,0.612),0.005)
    mat_blinn1 = rtm.Dielectric(rtu.Color(0.8, 0.5, 0.8),0.1)



    # add objects to the scene
    world = rts.Scene()
    # background
    #world.add_object(rto.Sphere(rtu.Vec3(   0,-101.5,-1),  100,mat_blinn1))

    # vCenter light same base
    # lightsaber lEFT
    obj_center_left = rtu.Vec3( -1.5, -1, 0)
    obj_axit_left = rtu.Vec3(1,1,0)
    world.add_object(rto.Cylinder(obj_center_left,  0.08, 3.4, obj_axit_left,light_red))   # light
    world.add_object(rto.Cylinder(obj_center_left,  0.14, 0.8, obj_axit_left,metal_mat))    # base
    # lightsaber RIGHT
    obj_center_right = rtu.Vec3( 1.5, -1, 0)
    obj_axit_right = rtu.Vec3(-1,1,0)
    world.add_object(rto.Cylinder(obj_center_right,  0.08, 3.4, obj_axit_right,light_greed))    # light
    world.add_object(rto.Cylinder(obj_center_right,  0.14, 0.8, obj_axit_right,metal_mat))    # base
    # Bullet
    radius_bullet = 0.1
    bulletC_1 = rtu.Vec3( 0, -1, -2)
    bulletA_1 = rtu.Vec3(0,1,0)
    bullet1 = rto.Cylinder(bulletC_1,  radius_bullet, 0.06, bulletA_1,light_white)
    bullet1.add_moving(bulletC_1 + rtu.Vec3( 0.2, 0, 0))
    world.add_object(bullet1)# bullet
    # Bullet
    bulletC_2 = rtu.Vec3( -2.5, 2, -2)
    bulletA_2 = rtu.Vec3(0,1,0)
    bullet2 = rto.Cylinder(bulletC_2,  radius_bullet, 0.06, bulletA_2,light_white)
    bullet2.add_moving(bulletC_2 + rtu.Vec3( 0.2, 0, 0))
    world.add_object(bullet2)# bullet



    intg = rti.Integrator(bSkyBG=False)

    renderer = rtren.Renderer(main_camera, intg, world)

    renderer.render()
    renderer.write_img2png('SceneTest.png')    


def renderScene1():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0/9.0
    main_camera.img_width = pixel
    main_camera.center = rtu.Vec3(0,0,0)
    main_camera.samples_per_pixel = spp
    main_camera.max_depth = mdepth
    main_camera.vertical_fov = 60
    main_camera.look_from = rtu.Vec3(-2, 2, 1)
    main_camera.look_at = rtu.Vec3(0, 0, -1)
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    defocus_angle = 2.0
    focus_distance = 5.0
    aperture = 1.0
    main_camera.init_camera(defocus_angle, focus_distance, aperture)
    
    # Setting Material
    tex_checker_bw = rtt.CheckerTexture(0.32, rtu.Color(.2, .2, .2), rtu.Color(.9, .9, .9))
    mat_tex_checker_bw = rtm.TextureColor(tex_checker_bw)

    mat_blinn1 = rtm.Blinn(rtu.Color(0.8, 0.5, 0.8), 0.5, 0.2, 8)
    mat_blinn2 = rtm.Blinn(rtu.Color(0.4, 0.5, 0.4), 0.5, 0.6, 8)
    mat_blinn3 = rtm.Blinn(rtu.Color(0.8, 0.5, 0.4), 0.5, 0.2, 8)


    # add objects to the scene
    world = rts.Scene()
    world.add_object(rto.Sphere(rtu.Vec3(   0,-100.5,-1),  100, mat_tex_checker_bw))
    world.add_object(rto.Sphere(rtu.Vec3(-1.0,   0.0,-1),  0.5, mat_blinn1))    # left
    world.add_object(rto.Sphere(rtu.Vec3(   0,   0.0,-1),  0.5, mat_blinn2))    # center
    world.add_object(rto.Sphere(rtu.Vec3( 1.0,   0.0,-1),  0.5, mat_blinn3))    # right

    intg = rti.Integrator(bSkyBG=True)

    renderer = rtren.Renderer(main_camera, intg, world)

    renderer.render()
    renderer.write_img2png('Scene-1.png')    

def renderScene2():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0/9.0
    main_camera.img_width = 320
    main_camera.center = rtu.Vec3(0,0,0)
    main_camera.samples_per_pixel = 5
    main_camera.max_depth = mdepth
    main_camera.vertical_fov = 60
    main_camera.look_from = rtu.Vec3(-2, 2, 1)
    main_camera.look_at = rtu.Vec3(0, 0, -1)
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    defocus_angle = 0.0
    focus_distance = 5.0
    aperture = 1.0
    main_camera.init_camera(defocus_angle, focus_distance,aperture)

    # Setting Material
    tex_checker_bw = rtt.CheckerTexture(0.32, rtu.Color(.2, .2, .2), rtu.Color(.9, .9, .9))
    mat_tex_checker_bw = rtm.TextureColor(tex_checker_bw)

    mat_blinn1 = rtm.Blinn(rtu.Color(0.8, 0.5, 0.8), 0.5, 0.2, 8)
    mat_blinn2 = rtm.Blinn(rtu.Color(0.4, 0.5, 0.4), 0.5, 0.6, 8)
    mat_blinn3 = rtm.Blinn(rtu.Color(0.8, 0.5, 0.4), 0.5, 0.2, 8)


    # add objects to the scene
    sph_left = rto.Sphere(rtu.Vec3(-1.0,   0.0,-1),  0.5, mat_blinn1)
    sph_left.add_moving(rtu.Vec3(-1.0,   0.0,-1) + rtu.Vec3(0.0, 0.5,0.0))

    world = rts.Scene()
    world.add_object(rto.Sphere(rtu.Vec3(   0,-100.5,-1),  100, mat_tex_checker_bw))
    world.add_object(sph_left)    # left
    world.add_object(rto.Sphere(rtu.Vec3(   0,   0.0,-1),  0.5, mat_blinn2))    # center
    world.add_object(rto.Sphere(rtu.Vec3( 1.0,   0.0,-1),  0.5, mat_blinn3))    # right

    intg = rti.Integrator(bSkyBG=True)

    renderer = rtren.Renderer(main_camera, intg, world)
    renderer.render_jittered()
    renderer.write_img2png('Scene2.png')    

if __name__ == "__main__":
    renderTest()
    #renderScene1()
    #renderScene2()


