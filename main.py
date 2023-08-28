from gl import Renderer
import shaders
import converter
from gl import Model


# PROYECTO 1 - Graficas por Computadora
#
# Autor: Diego Lemus / 21469
#
# Escena: El ultimo bola samurai defendiendo su dojo de los pines invasores.
#
# Objetos: 3 pines, 1 bola, 1 katana, 1 sombrero, 1 hacha, 1 ballesta, 1 espada.
#
# Shaders: gourad, obscure, comic, rainbow, infrared, fragment, outline.
# Los shaders se aplicaron para darle realismo a los personajes y denotar "poderes" en las armas.
#
# Se implemetaron los mapas de normales. Se aplicaron en la ballesta y la katana.
#
# Disclaimer: Se utilizaron distintas luces para resaltar detalles especificos de cada modelo.


# Tamanio del FrameBuffer (basado en imagen de fondo)
width = 1380
height = 820

output = "proyecto1/xd.bmp"
background = "backgrounds/dojo.bmp"

# Creacion del Renderer
rend = Renderer(width, height)
rend.glClear()
rend.glBackgroundTexture(background)
rend.glClearBackground()
rend.glLookAt(camPos = (0,0,0.5), eyePos= (0,0,-5))

# Personaje: Pin junto con hacha
def pin1():
    rend.glDirectionalLightDirection(0, 0, -1)
    
    model11 = Model("models/pin/pin.obj",
                    translate = (4, -2, -6),
                    rotate = (0, 290, 0),
                    scale = (0.5,0.5,0.5))
    
    model11.loadTexture("models/pin/pin.bmp")
    model11.setShaders(shaders.vertexShader, shaders.gouradShader)    
    
    rend.glAddModel(model11)
    rend.glRender()
    
    rend.glDirectionalLightDirection(0, 0, -0.6)
    
    model12 = Model("models/axe/axe.obj",
                    translate = (4.1, -0.9, -5.5),
                    rotate = (0, 0, 105),
                    scale = (1.2,1.2,1.2))
    
    model12.loadTexture("models/axe/axe.bmp")
    model12.setShaders(shaders.vertexShader, shaders.comicShader)
    
    rend.glAddModel(model12)
    rend.glRender()
    
# Personaje: Pin junto con espada
def pin2():
    rend.glDirectionalLightDirection(0, 0, -1)
    
    model21 = Model("models/pin/pin.obj",
                    translate = (2.5, -2, -5),
                    rotate = (0, 290, 0),
                    scale = (0.5,0.5,0.5))
    
    model21.loadTexture("models/pin/pin.bmp")
    model21.setShaders(shaders.vertexShader, shaders.gouradShader)
    
    rend.glAddModel(model21)
    rend.glRender()
    
    model22 = Model("models/sword/sword.obj",
                    translate = (2.1, -1.2, -4.5),
                    rotate = (260, 45, 270),
                    scale = (1.8,1.8,1.8))
    
    model22.loadTexture("models/sword/sword.bmp")
    model22.setShaders(shaders.vertexShader, shaders.rainbowShader)
    
    rend.glAddModel(model22)
    rend.glRender()
    
# Personaje: Pin junto con ballesta
def pin3():
    rend.glDirectionalLightDirection(0, 0, -1)
    
    model31 = Model("models/pin/pin.obj",
                    translate = (4, -2, -4.6),
                    rotate = (0, 290, 0),
                    scale = (0.5,0.5,0.5))
    
    model31.loadTexture("models/pin/pin.bmp")
    model31.setShaders(shaders.vertexShader, shaders.gouradShader)
    
    rend.glAddModel(model31)
    rend.glRender()
    
    rend.glDirectionalLightDirection(0.8, 0, -1)
    
    model32 = Model("models/crossbow/crossbow.obj",
                    translate = (3.6, -1.3, -4.2),
                    rotate = (20, 90, 0),
                    scale = (0.01,0.01,0.01))
    
    model32.loadTexture("models/crossbow/crossbow.bmp")
    model32.loadNormalMap("models/crossbow/crossbow_normal.bmp")
    model32.setShaders(shaders.vertexShader, shaders.infraredShader)
    
    rend.glAddModel(model32)
    rend.glRender()
    
# Personaje: Bola junto con sombrero y katana
def ball():
    
    model41 = Model("models/ball/ball.obj",
                    translate = (-11, -2, -27),
                    rotate = (75, 0, 170),
                    scale = (0.38,0.38,0.38))
    
    model41.loadTexture("models/ball/ball.bmp")
    model41.setShaders(shaders.vertexShader, shaders.fragmentShader)
    
    rend.glAddModel(model41)
    rend.glRender()
    
    rend.glDirectionalLightDirection(0, 0, 1)
    
    model42 = Model("models/hat/hat.obj",
                    translate = (-3.25, -0.7, -7),
                    rotate = (0, 205, 355),
                    scale = (0.2,0.17,0.2))
    
    model42.loadTexture("models/hat/hat.bmp")
    model42.setShaders(shaders.vertexShader, shaders.obscureShader)
    
    rend.glAddModel(model42)
    rend.glRender()
    
    rend.glDirectionalLightDirection(-0.8, 0, -1)
    
    model43 = Model("models/katana/katana.obj",
                    translate = (-3.8, -2.2, -7),
                    rotate = (0, 360, 290),
                    scale = (2.5,2.5,2.5))
    
    model43.loadTexture("models/katana/katana.bmp")
    model43.loadNormalMap("models/katana/katana_normal.bmp")
    model43.setShaders(shaders.vertexShader, shaders.blazeShader)

    rend.glAddModel(model43)
    rend.glRender()

# Se renderizan los personajes

ball()

# Se guarda el render
rend.glFinish(output)
rend.glClear()

# Se convierte el render a JPG
outputJPG = output.replace(".bmp", ".jpg")
converter.bmp_to_jpg(output, outputJPG)