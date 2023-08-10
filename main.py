from gl import Renderer
import shaders

# El tamanio del FrameBuffer
width = 2040
height = 1960

# Se crea el renderizador
rend = Renderer(width, height)

# Le damos los shaders que se utilizaran
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

# rend.glLookAt(camPos = (1,1,1), eyePos= (0,0,-5))

rend.glCamMatrix(translate = (0,0,0), rotate = (0,0,0))

# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "pin.obj",
                 texturename = "pin.bmp",
                 translate = (0, 0, -4),
                 rotate = (0, 0, 0),
                 scale = (0.5,0.5,0.5))

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("outputModel3-1.bmp")
