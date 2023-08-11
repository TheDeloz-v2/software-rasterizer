from math import isclose

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
def multiplicationMV(m, v):
    result = []
    
    for i in range(len(m)):
        result.append(0)
        for j in range(len(v)):
            result[i] += m[i][j] * v[j]
            
    return result
    

# Function to multiply vector x vector
def multiplicationVV(v1, v2):
            
    result = []
    
    for i in range(len(v1)):
        result.append(v1[i] * v2[i])
    
    return result
        

# Function to cross product of two vectors
def crossProductVV(v1, v2):
        
        return [v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]]


# Function to substraction matrix - matrix
def substractionMM(A, B):
    
        result = []
        
        for i in range(len(A)):
            result.append([])
            for j in range(len(A[0])):
                result[i].append(A[i][j] - B[i][j])
        
        return result

# Function to substraction vector - vector
def substractionVV(v1, v2):
        
    result = []
    
    for i in range(len(v1)):
        result.append(v1[i] - v2[i])
    
    return result


# Function to divide vector / escalar
def divisionVE(v, e):
        
        result = []
        
        for i in range(len(v)):
            result.append(v[i] / e)
        
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
    
    return temp


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
    transposed = []
    for i in range(len(matrix)):
        transposed.append([matrix[j][i] for j in range(len(matrix))])
    
    return transposed



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
    
    areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

    areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

    areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    if areaABC == 0:
        return None

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
        return (u, v, w)
    else:
        return None
