import mathbuddy

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
    
    