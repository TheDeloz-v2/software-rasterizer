import mathbuddy

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

def fatShader(vertex, **kwargs):
    modelMatrix = kwargs['modelMatrix']
    viewMatrix = kwargs['viewMatrix']
    projectionMatrix = kwargs['projectionMatrix']
    vpMatrix = kwargs['vpMatrix']
    normals = kwargs['normals']
    
    blowamount = 0.4
    
    vt = [vertex[0] + (normals[0] * blowamount),
        vertex[1] + (normals[1] * blowamount),
        vertex[2] + (normals[2] * blowamount),
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
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]
    
    color = [1, 1, 1]
    
    if texture != None:
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w
        textureColor = texture.getColor(tU, tV)
        color = [c * t for c, t in zip(color, textureColor)]
    else:
        color = [1, 1, 1]
    
    return color

# Gourad Shader
def gouradShader(**kwargs):
    texture= kwargs["texture"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]

    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]
    
    intensity = mathbuddy.dotProductVV(normal, mathbuddy.negativeV(dLight))
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b

    else:
        return [0,0,0]


# ----------------------------------------------------------------
# ----------------------- SHADERS EXTRAS ------------------------
# ----------------------------------------------------------------


# Negative Shader, invert the color of the texture
def negativeShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]
    
    b= 1.0
    g= 1.0
    r= 1.0

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= 1 - textureColor[2]
        g *= 1 - textureColor[1]
        r *= 1 - textureColor[0]
        
    return r,g,b


# Infrared Shader, creates the efect of infrared vision
def infraredShader(**kwargs):
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]
    
    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]
    
    intensity = mathbuddy.dotProductVV(normal, mathbuddy.negativeV(dLight))
    
    infrared_color = [max(0, min(1, 1 - intensity)),
                      max(0, min(1, 1 - intensity * 0.5)),
                      max(0, min(1, 1 - intensity * 0.2))]
    
    return infrared_color

 
# Rainbow Shader, creates the efect of rainbow vision
def rainbowShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]
    
    normal=[u * nA[0] + v * nB[0] + w * nC[0],
            u * nA[1] + v * nB[1] + w * nC[1],
            u * nA[2] + v * nB[2] + w * nC[2]]
    
    color = [1, 1, 1]
    intensity = mathbuddy.dotProductVV(normal, mathbuddy.negativeV(dLight))
    
    color = getRainbowColor(intensity)
    
    if texture != None:
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w
        textureColor = texture.getColor(tU, tV)
        color = [c * t for c, t in zip(color, textureColor)]
    
    return color

# Function to calculate the color of the rainbow shader
def getRainbowColor(intensity):
    if intensity > 1:
        intensity = 1
    elif intensity < -1:
        intensity = -1
    
    # Red
    if intensity >= 0.7:
        return [1, 0, 0]
    # Orange
    elif intensity >= 0.3:
        return [1, 0.5, 0]
    # Yellow
    elif intensity >= 0:
        return [1, 1, 0]
    # Green
    elif intensity >= -0.3:
        return [0, 1, 0]
    # Blue
    elif intensity >= -0.7:
        return [0, 0, 1]
    # Purple
    else:
        return [0.5, 0, 1]


# Resolution Shader, creates the efect of adjustable low resolution vision
def resolutionShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]
    
    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        size = 35  
        
        pX= 1.0/size
        pY= 1.0/size
        
        pixelX = int(tU/pX)*pX
        pixelY = int(tV/pY)*pY
        
        color = texture.getColor(pixelX, pixelY)
        
        return color
    
    else:
        return [0,0,0]


# Void Shader, which creates the efect of a exaggerated black and white vision
def voidShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]

    threshold = 0.69

    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)
        intensity = (textureColor[0] + textureColor[1] + textureColor[2]) / 3
    
    else:
        intensity = 0.0

    if intensity < threshold:
        
        return [1,1,1]  

    else:

        return [0,0,0]


# Comic Shader, creates the efect of a comic vision
def comicShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]
    
    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)
        
        if textureColor[0] < 0.5:
            textureColor[0] = 0
        else:
            textureColor[0] = 1
        
        if textureColor[1] < 0.5:
            textureColor[1] = 0
        else:
            textureColor[1] = 1
        
        if textureColor[2] < 0.5:
            textureColor[2] = 0
        else:
            textureColor[2] = 1
        
        return textureColor
    
    else:
        return [0,0,0]


# Mesh Shader, creates the efect of a adjustable mesh vision
def meshShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]
    
    pastel = 0.5
    
    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)
        
        textureColor[0] = textureColor[0] * pastel
        textureColor[1] = textureColor[1] * pastel
        textureColor[2] = textureColor[2] * pastel
        
        return textureColor
    
    else:
        return [0,0,0]