# RT-python-week010
Ray tracing course week 10

This repository is for 'Raytracing in Entertainment Industry' (01418283).
This course is set to be taught for undergrad students at Dept of Computer Science, Faculty of Science, Kasetsart University.
The codes were rewritten and modified from https://raytracing.github.io/books/RayTracingInOneWeekend.html.

**Prerequisites :**
1. C/C++ or python.
2. Object-Oriented Programming (OOP).
3. Linear algebra for undergrad students.


**Class assignment**

Do not forget to submit your codes when code implementation is needed.

Note that to submit the rendered results, please use the following parameters.
- at least 100 samples per pixel.
- at least 5 max depth.
- resolution width = 480p.
- aspect ratio = 16:9.

1. Implement DoF in 'get_jittered_ray()'. Render the output with 'renderDoF()'.
2. Implement DoF by using an 'aperture' parameter instead of 'defocus_angle'. Do not forget to replace all 'defocus_angle' calls. Render the output with 'renderDoF()' using the following parameters and commands.
- aperture = 1.0, focus_distance = 5.0.
- renderer.render() --> submit your rendered result.
- renderer.render_jittered() --> submit your rendered result.
3. Implement Motion blur effect in 'get_jittered_ray()'. Render the output with 'renderMoving().

