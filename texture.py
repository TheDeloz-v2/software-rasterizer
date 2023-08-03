import struct

class Texture(object):
    def __init__(self, filename):
        with open(filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack("=l", image.read(4))[0]
            
            image.seek(18)
            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]
            
            image.seek(headerSize)
            
            self.pixels = []
            
            for y in range(self.height):
                pixelsRow = []
                
                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255 
                    
                    pixelsRow.append([r, g, b])
                
                self.pixels.append(pixelsRow)
                
    def getColor(self, u, v):
        if 0 <= u < 1 and 0 <= v < 1:
            return self.pixels[int(v * self.height)][int(u * self.width)]
        else:
            return None
    
    
            