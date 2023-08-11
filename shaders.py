import mathbuddy
import numpy as np

modelMatrix = None
viewMatrix = None
projectionMatrix = None
vpMatrix = None

def vertexShader(vertex, **kwargs):
      modelMatrix = kwargs['modelMatrix']
      viewMatrix = kwargs['viewMatrix']
      projectionMatrix = kwargs['projectionMatrix']
      vpMatrix = kwargs['vpMatrix']
      
      vt = [vertex[0],
            vertex[1],
            vertex[2],
            1]
    
      o1 = mathbuddy.multiplicationMM(vpMatrix, projectionMatrix)
      o2 = mathbuddy.multiplicationMM(o1, viewMatrix)
      o3 = mathbuddy.multiplicationMM(o2, modelMatrix)
      vt = mathbuddy.multiplicationMV(o3, vt)

      # Check zero division
      for i in range(len(vt)):
            if vt[i] == 0:
                  vt[i] = 1
      
      vt = [vt[0] / vt[3], 
            vt[1] / vt[3], 
            vt[2] / vt[3]]

      return vt

def fragmentShader(**kwargs):
      texCoords = kwargs['texCoords']
      texture = kwargs['texture']
      
      if texture != None:
            color = texture.getColor(texCoords[0], texCoords[1])
      else:
          color = (1, 1, 1)
      
      return color

def gouradShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]
    
    normal=[u * nA[0] + v * nB[0] + w * nC[0],
            u * nA[1] + v * nB[1] + w * nC[1],
            u * nA[2] + v * nB[2] + w * nC[2]]
    
    dLight = np.array(dLight)
    
    color = [1, 1, 1]
    
    if texture != None:
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w
        textureColor = texture.getColor(tU, tV)
        color = [c * t for c, t in zip(color, textureColor)]
    
    intensity = np.dot(normal, -dLight)
    
    color = [max(0, min(1, c * intensity)) for c in color]
    
    return color