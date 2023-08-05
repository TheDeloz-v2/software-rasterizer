from gl import Renderer, V3, color
import shaders
import mathbuddy

# width = 2024
# height = 2024

# rend = Renderer(width, height)

# rend.vertexShader = shaders.vertexShader
# rend.fragmentShader = shaders.fragmentShader

# rend.glLoadModel(filename = "./models/model.obj", texturename= "./models/model2.bmp", translate=(width/3.5, height/1.7, 0), scale=(1000, 1000, 1000), rotate=(0, 0, 0))
# rend.glLoadModel(filename = "./models/model2.obj", texturename= "./models/model2.bmp", translate=(width/1.4, height/1.7, 0), scale=(1000, 1000, 1000), rotate=(0, 270, 0 ))

# rend.glLoadModel(filename = "./models/model2.obj", texturename= "./models/model2.bmp", translate=(width/2.7, height/5, 0), scale=(1000, 1000, 1000), rotate=(0, 315, 45))
# rend.glLoadModel(filename = "./models/model2.obj", texturename= "./models/model2.bmp", translate=(width/1.6, height/5, 0), scale=(1000, 1000, 1000), rotate=(0, 45, 315))

# rend.glRender()
# rend.glFinish('outputModel2.bmp')

matrix = [[2, 2, 2],[4, 0, 2],[4, 4, 2]]

print(mathbuddy.determinant(matrix))

print(mathbuddy.transposeMatrix(mathbuddy.adjointMatrix(matrix)))

print(mathbuddy.inverseMatrix(matrix))
