from gl import Renderer
import shaders
import converter

# Tamanio del FrameBuffer
width = 2040
height = 1960

# Creacion del Renderer
rend = Renderer(width, height)

# Shaders a utilizar
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.meshShader

rend.glClear()
output = "outputModel2-S9-Mesh.bmp"

rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

rend.glLoadModel(filename = "pin.obj",
                texturename = "pin.bmp",
                translate = (0, -2, -5),
                rotate = (0, 180, 0),
                scale = (1,1,1))

rend.glRender()
rend.glFinish(output)
rend.glClear()

outputJPG = output.replace(".bmp", ".jpg")

converter.bmp_to_jpg(output, outputJPG)