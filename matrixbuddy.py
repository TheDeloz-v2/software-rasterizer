# Function to multiply matrix x matrix
def multiplicationMM(A, B):

    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    result = [[0 for row in range(cols_B)] for col in range(rows_A)]

    for a in range(rows_A):
        for b in range(cols_B):
            for c in range(cols_A):
                result[a][b] += A[a][c] * B[c][b]

    return result 

# Function to multiply matrix x vector
def multiplicationMV(m , v):
    
    result = []
    
    for i in range(len(m)):
        temp = 0
        for j in range(len(v)):
            temp += m[i][j] * v[j]
        result.append(temp)
        
    return result

def barycentrinCoords(A, B, C, P):
    
    areaPCB = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    
    areaABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
    
    areaACP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    
    if areaABC == 0:
        return -1, -1, -1
    
    u = areaPCB / areaABC
    
    v = areaACP / areaABC
    
    w = 1 - u - v
    
    return u, v, w
