from gl import Renderer, V3, color
import shaders

width = 1024
height = 512

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.fragmentShader

# Poligono 1
vertices_poligono_1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
rend.glDrawPolygon(vertices_poligono_1, color(1, 1, 1))
rend.glFillPolygon(vertices_poligono_1, color(1, 1, 1))

# Poligono 2
vertices_poligono_2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
rend.glDrawPolygon(vertices_poligono_2, color(1, 1, 1))

# Poligono 3
vertices_poligono_3 = [(377, 249), (411, 197), (436, 249)]
rend.glDrawPolygon(vertices_poligono_3, color(1, 1, 1))

# Poligono 4
vertices_poligono_4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), 
                       (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]
rend.glDrawPolygon(vertices_poligono_4, color(1, 1, 1))

# Poligono 5
vertices_poligono_41 = [(682, 175), (708, 120) ,(735, 148) ,(739, 170)]
rend.glDrawPolygon(vertices_poligono_41, color(1, 1, 1))

rend.glRender()
rend.glFinish('outputPoligonos.bmp')