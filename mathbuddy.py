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


# Function to cross product of two vectors
def crossProductVV(v1, v2):
        
        return [v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]]


# Function to substraction matrix x matrix
def substractionMM(A, B):
    
        result = []
        
        for i in range(len(A)):
            result.append([])
            for j in range(len(A[0])):
                result[i].append(A[i][j] - B[i][j])
        
        return result


# Function to get a cofactor from a matrix
def cofactor(matrix, i, j):
    
    return [row[: j] + row[j + 1:] for row in (matrix[: i] + matrix[i + 1:])]


# Function to get the determinant of a matrix
def determinant(matrix):
    
    det = 0
    
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        for j in range(len(matrix)):
            det += matrix[0][j] * ((-1) ** j) * determinant(cofactor(matrix, 0, j))
    
    return det
   
    
# Function to normalize a vector
def normalize(v):
    temp = 0
    for i in range(len(v)):
        temp += v[i] ** 2
        
    temp = temp ** 0.5
    
    return [v[i] / temp for i in range(len(v))]


# Function to get the adjoint of a matrix
def adjointMatrix(matrix):
    adj = []
    for i in range(len(matrix)):
        adj.append([])
        for j in range(len(matrix)):
            adj[i].append(((-1) ** (i + j)) * determinant(cofactor(matrix, i, j)))
    
    return adj

        
# Function to get the transpose of a matrix
def transposeMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(i, len(matrix)):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    return matrix


# Function to get the inverse of a matrix
def inverseMatrix(matrix):
    det = determinant(matrix)
    if det == 0:
        return None
    else:
        adjtrans = transposeMatrix(adjointMatrix(matrix))
        inverse = []
        for i in range(len(adjtrans)):
            inverse.append([])
            for j in range(len(adjtrans)):
                inverse[i].append(adjtrans[i][j] / det)
        
        return inverse


# Function to get the barycentric coordinates of a triangle
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
