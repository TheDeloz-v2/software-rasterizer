from gl import Renderer, V3, color
import shaders

width = 1024
height = 1024

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel('model.obj', 
                 translate = (width/2, height/2, 0),
                 rotate = (0, 45, 0),
                 scale = (400, 400, 400))

rend.glRender()
rend.glFinish('outputModelObj.bmp')