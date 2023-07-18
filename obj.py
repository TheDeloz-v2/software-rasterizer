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
                    self.vertices.append(list(map(float, value.split(" "))))
                
                elif prefix == "vt":  # Texture coordinates
                    vt_values = list(map(float, value.split(" ")))
                    if len(vt_values) == 2:
                        vt_values.append(0.0)  # Adding a default value for the third component
                    self.texcoords.append(vt_values)

                elif prefix =="vn": #Normals
                    self.normals.append(list(map(float, value.split(" "))))

                elif prefix == "f": #Faces
                    if '//' in value:
                        self.faces.append([list(map(int, vert.split("//"))) for vert in value.split(" ")])
                    else:
                        self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])
                
                else:
                    pass