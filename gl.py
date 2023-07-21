import struct
from collections import namedtuple
import matrixbuddy
import math
from obj import Obj

V2 = namedtuple('point', ['x','y'])
V3 = namedtuple('point', ['x','y','z'])
POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

# Write the BMP file 
def char(c):
    return struct.pack('=c', c.encode('ascii'))
def word(w):
    return struct.pack('=h', w)
def dword(d):
    return struct.pack('=l', d)

# Transform the color format from float to bytes
def color(r, g, b):
    return bytes([int(b*255), int(g*255), int(r*255)])

class Model(object):
    def __init__(self, filename, translate = (0, 0, 0), rotate = (0, 0, 0), scale = (1, 1, 1)):
        model = Obj(filename)
        
        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals
        self.faces = model.faces
        
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        

class Renderer(object):
    # Constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClearColor(0,0,0)
        self.glClear()
        self.glColor(1,1,1)

        self.vertexShader = None
        self.fragmentShader = None
        self.primitiveType = TRIANGLES
        self.vertexBuffer = []
        
        self.objects = []

    def glAddVertices(self, vertices):
        for vertex in vertices:
            self.vertexBuffer.append(vertex)
       
    def glPrimitiveAssembly(self, transformedVertices):
        # Assembly the vertices into points, lines or triangles
        primitives = []

        if self.primitiveType == TRIANGLES:
            for i in range(0, len(transformedVertices), 3):
                triangle = [
                    transformedVertices[i],
                    transformedVertices[i+1],
                    transformedVertices[i+2]
                ]
                primitives.append(triangle)
    
        return primitives

    # Color to clear the screen
    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)
    
    # Clear the screen
    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]
        
    # Set color
    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)
        
    # Draw a point
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels [x][y] = clr or self.currColor
            
    # Draw a line
    def glLine(self, v0, v1, clr = None):
        # Bressenham line algorith
        # y = mx+b
        
        #m = (v1.y-v0.y)/(v1.x-v0.x)
        #y = v0.y
        
        #for x in range(v0.x, v1.x+1):
        #   self.glPoint(x,int(y))
        #   y += m
            
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])
        

        # Si las coordenadas son las mismas, se dibuja un solo pixel
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        # Se verifica si la pendiente es mayor que 1 (Porque, si es así, saltaría pixeles)
        steep = dy > dx
        
        # Si la pendiente es mayor que 1 o menor que -1
        # entonces intercambiamos los valores de x y y
        # para reorientar la linea (Se dibuja vertical en vez de horizontal)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        # Si el punto inicial es mayor que el punto final, se intercambian
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        # Se recalculan las diferencias
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset = 0
        limit = 0.5
        
        m = dy/dx
        y = y0
        
        for x in range(x0, x1+1):
            # Si la pendiente es mayor que 1, se dibuja vertical
            if steep:
               self.glPoint(y, x, clr or self.currColor)
            else:
                self.glPoint(x, y, clr or self.currColor)
            
            offset += m
            
            if offset > limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1
        
    # Draw a triangle
    def glTriangle(self, A, B, C, clr = None):
        self.glLine(A, B, clr or self.currColor)
        self.glLine(B, C, clr or self.currColor)
        self.glLine(C, A, clr or self.currColor)

    def glModelMatrix(self, translate = (0,0,0), scale = (1,1,1), rotate = (0,0,0)):        
        translation = [[1,0,0,translate[0]],
                       [0,1,0,translate[1]],
                       [0,0,1,translate[2]],
                       [0,0,0,1]]
        
        scaleMat = [[scale[0],0,0,0],
                    [0,scale[1],0,0],
                    [0,0,scale[2],0],
                    [0,0,0,1]]
        
        rxMat = [[1, 0, 0, 0],
                 [0, math.cos(math.radians(rotate[0])), -math.sin(math.radians(rotate[0])), 0],
                 [0, math.sin(math.radians(rotate[0])), math.cos(math.radians(rotate[0])), 0],
                 [0, 0, 0, 1]]
        
        ryMat = [[math.cos(math.radians(rotate[1])), 0, math.sin(math.radians(rotate[1])), 0],
                 [0, 1, 0, 0],
                 [-math.sin(math.radians(rotate[1])), 0, math.cos(math.radians(rotate[1])), 0],
                 [0, 0, 0, 1]]
        
        rzMat = [[math.cos(math.radians(rotate[2])), -math.sin(math.radians(rotate[2])), 0, 0],
                 [math.sin(math.radians(rotate[2])), math.cos(math.radians(rotate[2])), 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]]
        
        rotationMat = matrixbuddy.multiplicationMM(matrixbuddy.multiplicationMM(rxMat, ryMat), rzMat)
        
        return matrixbuddy.multiplicationMM(matrixbuddy.multiplicationMM(translation, scaleMat), rotationMat)


    def glLoadModel(self, filename, translate = (0, 0, 0), rotate = (0, 0, 0), scale = (1, 1, 1)):
        self.objects.append(Model(filename, translate, rotate, scale))
        
        
    def glRender(self):
        transformedVerts = []

        for model in self.objects:
            mMatrix = self.glModelMatrix(model.translate, model.scale, model.rotate)

            for face in model.faces:
                vertCount = len(face)
                v0=model.vertices[face[0][0] -1]
                v1=model.vertices[face[1][0] -1]
                v2=model.vertices[face[2][0] -1]
                if vertCount == 4:
                    v3=model.vertices[face[3][0] -1]

                if self.vertexShader:
                    
                    v0=self.vertexShader(v0, modelMatrix=mMatrix)
                    v1=self.vertexShader(v1, modelMatrix=mMatrix)
                    v2=self.vertexShader(v2, modelMatrix=mMatrix)
                    if vertCount == 4:
                        v3=self.vertexShader(v3, modelMatrix=mMatrix)
                
                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                if vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)

        primitives = self.glPrimitiveAssembly(transformedVerts)

        primColor = None
        if self.fragmentShader:
            primColor = self.fragmentShader()
            primColor = color(primColor[0],
                              primColor[1],
                              primColor[2],)
        else:
            primColor = self.currColor

        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(prim[0], prim[1], prim[2], primColor)
    
    # Draw a polygon      
    def glDrawPolygon(self, vertices, clr = None):
        # Draw lines between each vertex
        for i in range(len(vertices)):
            v0 = vertices[i]
            v1 = vertices[(i + 1) % len(vertices)]  # Close the polygon
            
            # -- Temporally - only x and y dimensions
            self.glLine(V3(v0[0], v0[1], 0), V3(v1[0], v1[1], 0), clr or self.currColor)
        
    # Fill a polygon    
    def glFillPolygon(self, vertices, clr = None):
        # Get the bounding box of the polygon
        x_min = min(vertices, key=lambda x: x[0])[0]
        x_max = max(vertices, key=lambda x: x[0])[0]
        y_min = min(vertices, key=lambda x: x[1])[1]
        y_max = max(vertices, key=lambda x: x[1])[1]
        
        # Draw box
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                self.glPoint(x, y, clr or self.currColor)
            
            
    # Export the BMP file
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char("B")) # BMP
            file.write(char("M")) # BMP
            file.write(dword(14 + 40 + (self.width * self.height * 3))) #size
            file.write(dword(0)) #reserved
            file.write(dword(14 + 40)) #pixel offset

            # InfoHeader
            file.write(dword(40)) # InfoHeader size
            file.write(dword(self.width)) # Width
            file.write(dword(self.height)) # Height
            file.write(word(1)) # Planes
            file.write(word(24)) # Bits per pixel
            file.write(dword(0)) # Compression
            file.write(dword(self.width * self.height * 3)) # Image size
            file.write(dword(0)) # X resolution
            file.write(dword(0)) # Y resolution
            file.write(dword(0)) # N colors
            file.write(dword(0)) # Important colors

            # ColorTable
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])