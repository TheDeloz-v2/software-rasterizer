from gl import Renderer
import shaders

# Tamanio del FrameBuffer
width = 2040
height = 1960

# Creacion del Renderer
rend = Renderer(width, height)

# Shaders a utilizar
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.rainbowShader

rend.glClear()
output = "outputPin-S3.bmp"

rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

rend.glLoadModel(filename = "pin.obj",
                texturename = "pin.bmp",
                translate = (0, -2, -5),
                rotate = (0, 0, 0),
                scale = (1,1,1))

rend.glRender()
rend.glFinish(output)
rend.glClear()