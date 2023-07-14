import shaders
from gl import Renderer, V2, V3

width = 512
height = 512

render = Renderer(width, height)

render.vertexShader = shaders.vertexShader
render.fragmentShader = shaders.fragmentShader

triangle = [V3(0,300,0),
            V3(512, 300, 0),
            V3(256, 0, 0)]

render.glAddVertices(triangle)

render.glModelMatrix(translate = (width/2, height/2, 0))

render.glRender()

render.glFinish('output8.bmp')
