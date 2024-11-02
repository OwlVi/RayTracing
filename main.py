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
    main_camera.samples_per_pixel = 5
    main_camera.max_depth = 5
    main_camera.vertical_fov = 60
    main_camera.look_from = rtu.Vec3(0, 2, 2)# (x rotation ,y rotation,z rotation)
    main_camera.look_at = rtu.Vec3(0, 0, -1)
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    defocus_angle = 2.0
    focus_distance = 5.0
    aperture = 1.0
    main_camera.init_camera(defocus_angle, focus_distance, aperture)
    
    # Setting Material
    ground = rtm.Dielectric(rtu.Color(0.270, 0.667, 0.9),3.33)
    red_mat = rtm.Blinn(rtu.Color(1,0,0),   0.8, 14,   2)
    blue_mat = rtm.Blinn( rtu.Color(0,0,1), 0.8, 14,   2)
    point_light = rtl.Diffuse_light(rtu.Color(0.125,0.125,0.125))

    # add objects to the scene
    world = rts.Scene()
    # background
    world.add_object(rto.Sphere(rtu.Vec3(   0,-101.5,-1),  100,ground))
    
    # Light
    point = rto.Sphere(rtu.Vec3(0,5,3),1,point_light)
    world.add_object(point)
    
    # Sphere
    r_sphere = 0.75
    # sphere left 
    left_centerP = rtu.Vec3(-0.1,1,0)
    sphere_left = rto.Sphere(left_centerP,r_sphere,red_mat)
    sphere_left.add_moving(left_centerP + rtu.Vec3(.5,0,0))
    world.add_object(sphere_left)
    
    # sphere right 
    right_centerP =rtu.Vec3(0.1,1,0)
    sphere_right = rto.Sphere(right_centerP,r_sphere,blue_mat)
    sphere_right.add_moving(right_centerP + rtu.Vec3(-.5,0,0))
    world.add_object(sphere_right)
    
    
    
    intg = rti.Integrator(bSkyBG=True)

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
    
    light_red = rtl.SaberLight(rtu.Color(1,0.15,0.15))
    light_greed = rtl.SaberLight(rtu.Color(0.15,1,0.15))
    light_white = rtl.Diffuse_light(rtu.Color(1,1,1))
    metal_mat = rtm.Metal(rtu.Color(0.612,0.612,0.612),0.005)

    # add objects to the scene
    world = rts.Scene()

    # vCenter light same base
    # lightsaber lEFT
    obj_center_left = rtu.Vec3( -1.5, -1, -0.75)
    obj_axit_left = rtu.Vec3(1,1,0)

    # lightsaber RIGHT
    obj_center_right = rtu.Vec3( 1.5, -1, -0.5)
    obj_axit_right = rtu.Vec3(-1,1,0)
   
    # ---------------------
    r_bullet = 0.04
    e_bullet = 1.4
    # Bullet 1
    x1 = 1
    y1 = -1
    z1 = 0.2
    bulletS_1 = rtu.Vec3(x1, y1, z1)
    bulletE_1 = rtu.Vec3(x1+e_bullet, y1, z1)
    bullet1 = rto.Capsule(bulletS_1,  bulletE_1, r_bullet,light_white)
    bullet1.add_moving(rtu.Vec3(-0.1,0,0))
    # Bullet 2
    x2 = -2
    y2 = -1
    z2 = -2
    bulletS_2 = rtu.Vec3( x2, y2, z2)
    bulletE_2 = rtu.Vec3(x2-e_bullet, y2, z2)
    bullet2 = rto.Capsule(bulletS_2,bulletE_2, r_bullet,light_white)
    bullet2.add_moving(rtu.Vec3(0.1,0,0))
    # Bullet 3
    x3 = 0.6
    y3 = 0
    z3 = -1.2
    bulletS_3 = rtu.Vec3( x3, y3, z3)
    bulletE_3 = rtu.Vec3(x3-e_bullet, y3, z3)
    bullet3 = rto.Capsule(bulletS_3,bulletE_3, r_bullet,light_white)
    bullet3.add_moving(rtu.Vec3(0.1,0,0))
    # Bullet 4
    x4 = -1.5
    y4 = 1
    z4 = 0.25
    bulletS_4 = rtu.Vec3( x4, y4, z4)
    bulletE_4 = rtu.Vec3(x4+e_bullet, y4, z4)
    bullet4 = rto.Capsule(bulletS_4,bulletE_4, r_bullet,light_white)
    bullet4.add_moving(rtu.Vec3(-0.5,0,0))
    # Bullet 5
    x5 = 2
    y5 = 1
    z5 = -0.5
    bulletS_5 = rtu.Vec3( x5, y5, z5)
    bulletE_5 = rtu.Vec3(x5+e_bullet, y5, z5)
    bullet5 = rto.Capsule(bulletS_5,bulletE_5, r_bullet,light_white)
    bullet5.add_moving(rtu.Vec3(-0.5,0,0))
    # Bullet 6
    x6 = 0
    y6 = 0.75
    z6 = 1
    bulletS_6 = rtu.Vec3( x6, y6, z6)
    bulletE_6 = rtu.Vec3(x6+e_bullet, y6, z6)
    bullet6 = rto.Capsule(bulletS_6,bulletE_6, r_bullet,light_white)
    bullet6.add_moving(rtu.Vec3(-0.5,0,0))
    # Bullet 7
    x7 = -1
    y7 = 1
    z7 = -2.5
    bulletS_7 = rtu.Vec3( x7, y7, z7)
    bulletE_7 = rtu.Vec3(x7-e_bullet, y7, z7)
    bullet7 = rto.Capsule(bulletS_7,bulletE_7, r_bullet,light_white)
    bullet7.add_moving(rtu.Vec3(0.5,0,0))
    
    # Add to world
    world.add_object(rto.Cylinder(obj_center_left,  0.08, 3.4, obj_axit_left,light_red))   # light
    world.add_object(rto.Cylinder(obj_center_left,  0.14, 0.8, obj_axit_left,metal_mat))    # base    
    world.add_object(rto.Cylinder(obj_center_right,  0.08, 3.4, obj_axit_right,light_greed))    # light
    world.add_object(rto.Cylinder(obj_center_right,  0.14, 0.8, obj_axit_right,metal_mat))    # base
    world.add_object(bullet1)# bullet    
    world.add_object(bullet2)# bullet    
    world.add_object(bullet3)# bullet
    world.add_object(bullet4)# bullet
    world.add_object(bullet5)# bullet
    world.add_object(bullet6)# bullet
    world.add_object(bullet7)# bullet

    intg = rti.Integrator(bSkyBG=False)

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


