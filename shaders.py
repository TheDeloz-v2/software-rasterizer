import mathbuddy
from math import exp
import random

modelMatrix = None
viewMatrix = None
projectionMatrix = None
vpMatrix = None

# Vertex Shader, uses the matrices to calculate the position of the vertex
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


# Fat Shader, increase the size of the model
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


# Fragment Shader, uses the color of the texture to paint the model
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


# Gourad Shader, uses the normals of the model to create the efect of a more detailed texture
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
    

# Normal Map Shader, uses a normal map to create the efect of a more detailed texture
def normalMapShader(**kwargs):
    texture= kwargs["texture"]
    normalMap= kwargs["normalMap"]
    tA, tB, tC= kwargs["texCoords"]
    nA, nB, nC= kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w= kwargs["bCoords"]
    tangent = kwargs["tangent"]

    b= 1.0
    g= 1.0
    r= 1.0

    tU= u * tA[0] + v * tB[0] + w * tC[0]
    tV= u * tA[1] + v * tB[1] + w * tC[1]
        
    if texture != None:
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    normal= [u * nA[0] + v * nB[0] + w * nC[0],
             u * nA[1] + v * nB[1] + w * nC[1],
             u * nA[2] + v * nB[2] + w * nC[2]]
    
    if normalMap != None:
        texNormal = normalMap.getColor(tU, tV)
        texNormal = [texNormal[0] * 2 - 1,
                        texNormal[1] * 2 - 1,
                        texNormal[2] * 2 - 1]
        
        texNormal = mathbuddy.divisionVE(texNormal, mathbuddy.normalize(texNormal))
        
        bitangent = mathbuddy.crossProductVV(normal, tangent)
        bitangent = mathbuddy.divisionVE(bitangent, mathbuddy.normalize(bitangent))
        
        
        tangent = mathbuddy.crossProductVV(normal, bitangent)
        tangent = mathbuddy.divisionVE(tangent, mathbuddy.normalize(tangent))
        
        
        tangentMatrix = [[tangent[0], bitangent[0], normal[0]],
                            [tangent[1], bitangent[1], normal[1]],
                            [tangent[2], bitangent[2], normal[2]]]
        
        texNormal = mathbuddy.multiplicationMV(tangentMatrix, texNormal)
        texNormal = mathbuddy.divisionVE(texNormal, mathbuddy.normalize(texNormal))
        
        intensity = mathbuddy.dotProductVV(texNormal, mathbuddy.negativeV(dLight))
        
    else:
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

# Obscure Shader, obscure the color of the texture
def obscureShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    u, v, w = kwargs["bCoords"]
    
    b= 1.0
    g= 1.0
    r= 1.0
    
    obsc = 0.7

    if texture != None:
        tU= u * tA[0] + v * tB[0] + w * tC[0]
        tV= u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)    
        b *= textureColor[2] * obsc
        g *= textureColor[1] * obsc
        r *= textureColor[0] * obsc
        
    return r,g,b


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
    

# Blaze Shader, creates the efect of a blaze vision based in a specific color
def blazeShader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    dLight = kwargs["dLight"]
    u, v, w = kwargs["bCoords"]

    if texture != None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        
        textureColor = texture.getColor(tU, tV)

    normal = (u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2])
    
    negativedLight = (-dLight[0], -dLight[1], -dLight[2])
    intensity = max(0, mathbuddy.dotProductVV(normal, negativedLight))

    # Color dorado
    outlineColor = (1, 0.84, 0) 
    interiorColor = textureColor if texture != None else (1.0, 1.0, 1.0)
    
    # Factor de umbral de intensidad
    threshold = 0.5
    
    # Factor para suavizar el contorno
    falloff = 0.2 

    mixFactor = exp(-(intensity - threshold) / falloff)

    color = [
        (1 - mixFactor) * interiorColor[channel] + mixFactor * outlineColor[channel]
        for channel in range(3)
    ]

    color = [max(0.0, min(1.0, channel)) for channel in color]

    return color