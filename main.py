from gl import Renderer
import shaders

# Tamanio del FrameBuffer
width = 2040
height = 1960

# Creacion del Renderer
rend = Renderer(width, height)

# Shaders a utilizar
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

# Medium Shot
def mediumShot():
    rend.glClear()
    output = "photoshoot/outputModel3-MS.bmp"
    
    rend.glLookAt(camPos = (0,0,0), eyePos= (0,0,-5))

    rend.glLoadModel(filename = "pin.obj",
                 texturename = "pin.bmp",
                 translate = (0, -1, -4),
                 rotate = (0, 0, 0),
                 scale = (0.5,0.5,0.5))

    rend.glRender()
    rend.glFinish(output)
    rend.glClear()


# Low Angle Shot
def lowAngleShot():
    rend.glClear()
    output = "photoshoot/outputModel3-LS.bmp"
    
    rend.glLookAt(camPos = (0,-2.5,-2), eyePos= (0,1,-5))

    rend.glLoadModel(filename = "pin.obj",
                 texturename = "pin.bmp",
                 translate = (0, -1, -4),
                 rotate = (0, 0, 0),
                 scale = (0.5,0.5,0.5))

    rend.glRender()
    rend.glFinish(output)
    rend.glClear()


# High Angle Shot
def highAngleShot():
    rend.glClear()
    output = "photoshoot/outputModel3-HS.bmp"
    
    rend.glLookAt(camPos = (0,4,-2), eyePos= (0,-1,-4.5))

    rend.glLoadModel(filename = "pin.obj",
                 texturename = "pin.bmp",
                 translate = (0, -1, -4),
                 rotate = (0, 0, 0),
                 scale = (0.5,0.5,0.5))

    rend.glRender()
    rend.glFinish(output)
    rend.glClear()


# Dutch Angle Shot
def DutchAngleShot():
    rend.glClear()
    output = "photoshoot/outputModel3-DS.bmp"
    
    rend.glLookAt(camPos = (2,-0.5,0), eyePos= (0,0,-5))

    rend.glLoadModel(filename = "pin.obj",
                 texturename = "pin.bmp",
                 translate = (0, -1, -4),
                 rotate = (0, 0, -29),
                 scale = (0.5,0.5,0.5))

    rend.glRender()
    rend.glFinish(output)
    rend.glClear()
    

# Generacion de shots
# Borrar el # para generar el shot

# mediumShot()
# lowAngleShot()
# highAngleShot()
# DutchAngleShot()
