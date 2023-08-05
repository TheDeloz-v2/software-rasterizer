from gl import Renderer
import shaders

# El tamanio del FrameBuffer
width = 960
height = 540

# Se crea el renderizador
rend = Renderer(width, height)

# Le damos los shaders que se utilizaran
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

rend.glLookAt(camPos = (-3,-1,-2), eyePos= (0,0,-5))

# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "model2.obj",
                 texturename = "model2.bmp",
                 translate = (-1, -1.5, -4),
                 rotate = (0, 180, 0),
                 scale = (5,5,5))

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("outputModel2Cameras.bmp")
