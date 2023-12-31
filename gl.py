import struct
from collections import namedtuple
import mathbuddy
import math
from obj import Obj
from texture import Texture

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
    def __init__(self, filename, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):

        self.loadModel(filename)
        self.filename = filename
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        self.texture = None
        self.normalMap = None

        self.setShaders(None, None)

    def loadModel(self, filename) -> None:

        model = Obj(filename)

        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals
        self.faces = model.faces

    def loadTexture(self, texturename) -> None:

        self.texture = Texture(texturename)

    def loadNormalMap(self, normalMap) -> None:

        self.normalMap = Texture(normalMap)

    def setShaders(self, vertexShader, fragmentShader) -> None:

        self.vertexShader = vertexShader
        self.fragmentShader = fragmentShader
        

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
        
        self.activeTexture = None
        self.activeNormalMap = None
        
        self.background = None
        
        self.activeModelMatrix = None
        
        self.glViewPort(0,0,self.width,self.height)
        self.glCamMatrix()
        self.glProjectionMatrix()
        
        self.directionalLight = (1, 0, 0)
        

    def glAddVertices(self, vertices):
        for vertex in vertices:
            self.vertexBuffer.append(vertex)
            
       
    def glPrimitiveAssembly(self, tVerts, uVerts, tTexCoords, tNormals):
        primitives = [ ]
        if self.primitiveType == TRIANGLES:
            for i in range(0, len(tVerts), 3):
                transformedverts = [
                    tVerts[i],
                    tVerts[i + 1],
                    tVerts[i + 2]]
                
                untransformedverts = [
                    uVerts[i],
                    uVerts[i + 1],
                    uVerts[i + 2]]
                
                texCoords = [
                    tTexCoords[i],
                    tTexCoords[i + 1],
                    tTexCoords[i + 2]]
                
                normals = [
                    tNormals[i],
                    tNormals[i + 1],
                    tNormals[i + 2]]
                
                triangle = [
                    transformedverts,
                    untransformedverts,
                    texCoords,
                    normals]
                
                primitives.append(triangle)
        return primitives

    def glAddModel(self, model):
        self.objects.append(model)

    # Color to clear the screen
    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)
        
    # Background Texture
    def glBackgroundTexture(self, filename):
        self.backgroundTexture = Texture(filename)
    
    def glClearBackground(self):
        self.glClear()
        
        if self.backgroundTexture:
            for x in range(self.vpX, self.vpX+self.vpWidth+1):
                for y in range(self.vpY, self.vpY+self.vpHeight+1):
                    u=(x-self.vpX)/self.vpWidth
                    v=(y-self.vpY)/self.vpHeight
                    texColor = self.backgroundTexture.getColor(u, v)
                    if texColor:
                        self.glPoint(x,y,color(texColor[0],texColor[1],texColor[2]))
              
    
    # Clear the screen
    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] 
                       for x in range(self.width)]
        
        self.zbuffer = [[float('inf') for y in range(self.height)] 
                        for x in range(self.width)]
        
    
    def glDirectionalLightDirection(self, x, y, z):
        self.directionalLight = (x, y, z)
        
        
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
        
    
    def glCamMatrix(self, translate = (0,0,0), rotate = (0,0,0)):
        # Crea una matrix de camera
        self.camMatrix = self.glModelMatrix(translate, rotate)
        
        # La matriz de vista es igual a la inversa de la camara
        self.viewMatrix = mathbuddy.inverseMatrix(self.camMatrix)
        
    
    def glLookAt(self, camPos = (0,0,0), eyePos = (0,0,0)):
        worldUp = (0,1,0)
        
        foward = mathbuddy.substractionVV(camPos, eyePos)
        foward = mathbuddy.divisionVE(foward, mathbuddy.normalize(foward))
        
        right = mathbuddy.crossProductVV(worldUp, foward)
        right = mathbuddy.divisionVE(right, mathbuddy.normalize(right))
        
        up = mathbuddy.crossProductVV(foward, right)
        up = mathbuddy.divisionVE(up, mathbuddy.normalize(up))
        
        self.camMatrix = [[right[0], up[0], foward[0], camPos[0]],
                          [right[1], up[1], foward[1], camPos[1]],
                          [right[2], up[2], foward[2], camPos[2]],
                          [0,0,0,1]]
        
        self.viewMatrix = mathbuddy.inverseMatrix(self.camMatrix)
    
    
    def glProjectionMatrix(self, fov = 60, n = 0.1, f = 1000):
        
        aspectRadio = self.vpWidth / self.vpHeight
        
        t = math.tan(math.radians(fov) / 2) * n
        r = t * aspectRadio
        
        self.projectionMatrix = [[n/r, 0, 0, 0],
                                    [0, n/t, 0, 0],
                                    [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
                                    [0, 0, -1, 0]]
        
        
    def glViewPort(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height
        
        self.vpMatrix =[[self.vpWidth/2,0,0,self.vpX+self.vpWidth/2],
                        [0,self.vpHeight/2,0,self.vpY+self.vpHeight/2],
                        [0,0,0.5,0.5],
                        [0,0,0,1]]
        
    
    def glModelMatrix(self, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):        
        translation = [[1,0,0,translate[0]],
                       [0,1,0,translate[1]],
                       [0,0,1,translate[2]],
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
        
        rotationMat = mathbuddy.multiplicationMM(mathbuddy.multiplicationMM(rxMat, ryMat), rzMat)
        
        scaleMat = [[scale[0],0,0,0],
            [0,scale[1],0,0],
            [0,0,scale[2],0],
            [0,0,0,1]]
                
        return mathbuddy.multiplicationMM(mathbuddy.multiplicationMM(translation, rotationMat ),scaleMat)


    def glLoadModel(self, filename, texturename, translate = (0, 0, 0), rotate = (0, 0, 0), scale = (1, 1, 1)):
        
        model = Model(filename, translate, rotate, scale)
        
        model.LoadTexture(texturename)
        
        self.objects.append( model )
        
        
    def glRender(self):
        
        for model in self.objects:
            
            transformedVerts = []
            untransformedVerts = []
            texCoords = []
            normals = []
            
            self.vertexShader = model.vertexShader
            self.fragmentShader = model.fragmentShader
            self.activeTexture = model.texture
            self.activeNormalMap = model.normalMap
            self.activeModelMatrix = self.glModelMatrix(model.translate, model.rotate, model.scale)

            for face in model.faces:
                vertCount = len(face)
                
                v0=model.vertices[face[0][0] -1]
                v1=model.vertices[face[1][0] -1]
                v2=model.vertices[face[2][0] -1]
                
                if vertCount == 4:
                    v3=model.vertices[face[3][0] -1]   
                    
                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                
                if vertCount == 4:
                    vt3 = model.texcoords[face[3][1] - 1]
                
                texCoords.append(vt0)
                texCoords.append(vt1)
                texCoords.append(vt2)
                
                if vertCount == 4:
                    texCoords.append(vt0)
                    texCoords.append(vt2)
                    texCoords.append(vt3)
                
                vn0 = model.normals[face[0][2] - 1]
                vn1 = model.normals[face[1][2] - 1]
                vn2 = model.normals[face[2][2] - 1]
                
                if vertCount == 4:
                    vn3 = model.normals[face[3][2] - 1]
                    
                normals.append(vn0)
                normals.append(vn1)
                normals.append(vn2)
                if vertCount == 4:
                    normals.append(vn0)
                    normals.append(vn2)
                    normals.append(vn3)   
                
                
                untransformedVerts.append(v0)
                untransformedVerts.append(v1)
                untransformedVerts.append(v2)
                
                if vertCount == 4:
                    untransformedVerts.append(v0)
                    untransformedVerts.append(v2)
                    untransformedVerts.append(v3)
                
                
                if self.vertexShader:
                    
                    v0=self.vertexShader(v0, 
                                        modelMatrix=self.activeModelMatrix, 
                                        viewMatrix=self.viewMatrix,
                                        projectionMatrix=self.projectionMatrix,
                                        vpMatrix=self.vpMatrix,
                                        normals = vn0)
                    
                    v1=self.vertexShader(v1, 
                                        modelMatrix=self.activeModelMatrix,
                                        viewMatrix=self.viewMatrix,
                                        projectionMatrix=self.projectionMatrix,
                                        vpMatrix=self.vpMatrix, 
                                        normals = vn1)
                    
                    v2=self.vertexShader(v2,
                                        modelMatrix=self.activeModelMatrix,
                                        viewMatrix=self.viewMatrix,
                                        projectionMatrix=self.projectionMatrix,
                                        vpMatrix=self.vpMatrix,
                                        normals = vn2)
                    
                    if vertCount == 4:
                        v3=self.vertexShader(v3,
                                            modelMatrix=self.activeModelMatrix,
                                            viewMatrix=self.viewMatrix,
                                            projectionMatrix=self.projectionMatrix,
                                            vpMatrix=self.vpMatrix,
                                            normals = vn3)
                
                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)
                
                if vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)
                    
                

        primitives = self.glPrimitiveAssembly(transformedVerts, untransformedVerts, texCoords, normals)

        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(prim[0], prim[1], prim[2], prim[3])
    
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
        
        # For each pixel in the bounding box
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                # If the pixel is inside the polygon
                if self.glPointInPolygon(x, y, vertices):
                    self.glPoint(x, y, clr or self.currColor)
        
    # Check if a point is inside a polygon
    # Using Ray Casting Algorithm
    # http://philliplemons.com/posts/ray-casting-algorithm
    def glPointInPolygon(self, x, y, vertices):
        n = len(vertices)
        inside = False
        
        for i in range(n):
            j = (i + 1) % n
            
            if (vertices[i][1] > y) != (vertices[j][1] > y):
                
                # Calculate the intersection of the polygon's edge with the horizontal line
                intersection = (vertices[j][0] - vertices[i][0]) * (y - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) + vertices[i][0]
                
                # Check if the point is to the left of the intersection (inside the polygon)
                if x < intersection:
                    inside = not inside
            
        return inside
    
    
    def glTriangle(self, transformedVerts, untransformedVerts, texCoords, normals):
        
        A = transformedVerts[0]
        B = transformedVerts[1]
        C = transformedVerts[2]
        
        uA = untransformedVerts[0]
        uB = untransformedVerts[1]
        uC = untransformedVerts[2]
        
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))
        
        
        edge1 = mathbuddy.substractionVV(uB, uA)
        edge2 = mathbuddy.substractionVV(uC, uA)
        
        deltaUV1 = mathbuddy.substractionVV(texCoords[1], texCoords[0])
        deltaUV2 = mathbuddy.substractionVV(texCoords[2], texCoords[0])
        
        num = deltaUV1[0] * deltaUV2[1] - deltaUV2[0] * deltaUV1[1]
        f = 1
        
        if num != 0:
            f = 1.0 / num
        
        tangent = [f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0]),
                   f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1]),
                   f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])]
        
        tangent = mathbuddy.divisionVE(tangent, mathbuddy.normalize(tangent))
        
        
        

        # Para cada pixel dentro del bounding box
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                # Si el pixel est� dentro del FrameBuffer
                if (0 <= x < self.width) and (0 <= y < self.height):
                    P = (x,y)
                    bCoords = mathbuddy.barycentrinCoords(A, B, C, P)
                    
                    if bCoords != None:
                        u, v, w = bCoords
                        
                        z = u * A[2] + v * B[2] + w * C[2]
                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z
                            
                            if self.fragmentShader != None:
                                colorP = self.fragmentShader(texture = self.activeTexture,
                                                             normalMap = self.activeNormalMap,
                                                            texCoords = texCoords,
                                                            normals = normals,
                                                            dLight = self.directionalLight,
                                                            bCoords = bCoords,
                                                            camMatrix = self.camMatrix,
                                                            modelMatrix = self.activeModelMatrix,
                                                            tangent = tangent)

                                self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                            else:
                                self.glPoint(x, y)
                            
    
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