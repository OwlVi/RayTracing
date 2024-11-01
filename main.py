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
    metal_mat = rtm.Metal(rtu.Color(0.612,0.612,0.612),1)
    black = rtm.Blinn(rtu.Color(0,0,0),1,1,15)


    # add objects to the scene
    world = rts.Scene()
    # background
    #world.add_object(rto.Quad(rtu.Vec3( -2, -2.5, -2), rtu.Vec3(4, 0, 0), rtu.Vec3(0, 10, 0),black))
    
    # vCenter light same base
    # lightsaber lEFT     
    world.add_object(rto.Cylinder(rtu.Vec3( -1.5, -1, 0),  0.1, 3.4, rtu.Vec3(1,1,0),light_red))    # light
    world.add_object(rto.Cylinder(rtu.Vec3( -1.5, -1, 0),  0.14, 0.8, rtu.Vec3(1,1,0),metal_mat))    # base
    # lightsaber RIGHT
    world.add_object(rto.Cylinder(rtu.Vec3( 1.5, -1, 0),  0.1, 3.4, rtu.Vec3(-1,1,0),light_greed))    # light
    world.add_object(rto.Cylinder(rtu.Vec3( 1.5, -1, 0),  0.14, 0.8, rtu.Vec3(-1,1,0),metal_mat))    # base

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
    main_camera.img_width = pixel
    main_camera.center = rtu.Vec3(0,0,0)
    main_camera.samples_per_pixel = spp
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


