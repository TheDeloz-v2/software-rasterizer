from gl import Renderer
import shaders

# Tamanio del FrameBuffer
width = 2040
height = 1960

# Creacion del Renderer
rend = Renderer(width, height)

# Shaders a utilizar
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.gouradShader

rend.glClear()
output = "outputModel4.bmp"

rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

rend.glLoadModel(filename = "model.obj",
                texturename = "model.bmp",
                translate = (0, 0, -4),
                rotate = (0, 0, 0),
                scale = (1,1,1))

rend.glRender()
rend.glFinish(output)
rend.glClear()