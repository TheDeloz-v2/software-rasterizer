class Obj(object):
    def __init__(self, filename):
        with open(filename,"r") as file:
            self.lines = file.read().splitlines()
        
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in self.lines:
            if line != ' ' or line != '\n':
                try:
                    if line[-1] == ' ' or line[-1] == '\n' or line[-1] == '\t':
                        line = line[:-1]
                    
                    if (line[2] == ' ' and line[3] == ' ') or (line[1] == ' ' and line[2] == ' '):
                        line = line.replace(line[1], '')

                    prefix, value = line.split(" ", 1)
                except:
                    continue
                
                if prefix =="v": #Vertices
                    self.vertices.append(list(map(float, list(filter(None, value.split(" "))))))
                
                elif prefix == "vt":  # Texture coordinates
                    self.texcoords.append(list(map(float, list(filter(None, value.split(" "))))))

                elif prefix =="vn": #Normals
                    self.normals.append(list(map(float, list(filter(None, value.split(" "))))))

                elif prefix == "f": #Faces
                    self.faces.append([list(map(int, list(filter(None, face.split("/"))))) for face in list(filter(None, value.split(" ")))])
                else:
                    pass