from gl import Renderer, V3, color
import shaders

width = 1024
height = 1024

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLoadModel('charizard.obj', 
                 translate = (width/2, height/4, 0),
                 rotate = (0, 0, 0),
                 scale = (25, 25, 25))

rend.glRender()
rend.glFinish('outputObj.bmp')