import os

class KRes:
    def __init__(self,path):
        self.base_path = path
        self.bgm = os.listdir(path + "/bgm")
        self.field = self.load_field()
        self.img = os.listdir(path + "/img")
        self.se = os.listdir(path + "/se")
        self.text = self.load_script()
        
    def load_field(self):
        files = os.listdir(self.base_path + "/field")
        output = {}
        for f in files:
            name = f[:f.rfind('.')]
            print name
            output[name] = Field(open(self.base_path + "/field/" + f,'r').read())
        return output
        
    def load_script(self):
        files = os.listdir(self.base_path + "/text")
        output = {}
        for f in files:
            name = f[:f.rfind('.')]
            output[name] = Script(open(self.base_path + "/text/" + f,'r').read())
        return output

class Field:
    def __init__(self,data):
        self.data = data
        self.header = self.read_header()
        self.map1 = ""
        self.map2 = ""
        self.map3 = ""
        self.map4 = ""
        self.sprite_sheet = ""
        self.tile1 = ""
        self.tile2 = ""
        self.tile3 = ""
        self.read_data()
        
    def read_header(self):
        return self.data[:16]
        
    def read_data(self):
        pos = 0
        def read_word(pos):
            wsize = ord(self.data[pos])
            return (self.data[pos + 1:pos + 1 + wsize],wsize+1)
        
        header = self.data[:16]
        self.header = header
        pos += 16
        
        # dunno what this word is
        w = read_word(pos)
        #print w[0]
        pos += w[1]
        
        # mapname 1
        w = read_word(pos)
        self.map1 = w[0]
        pos += w[1]
        
        # mapname 2
        w = read_word(pos)
        self.map2 = w[0]
        pos += w[1]
        
        # mapname 3
        w = read_word(pos)
        self.map3 = w[0]
        pos += w[1]
        
        # mapname 4
        w = read_word(pos)
        self.map4 = w[0]
        pos += w[1]
        
        # spritesheet
        w = read_word(pos)
        self.spritesheet = w[0]
        pos += w[1]
        
        # unknown bytes
        pos += 8
        
        # tilesheet 1
        w = read_word(pos)
        self.tile1 = w[0]
        pos += w[1]
        pos += 2 # mystery bytes
        
        # tilesheet 2
        w = read_word(pos)
        self.tile2 = w[0]
        pos += w[1]
        pos += 2 # mystery bytes
        
        # tilesheet 3
        w = read_word(pos)
        self.tile3 = w[0]
        pos += w[1]
        pos += 2 # mystery bytes
        
        # tiledata start
        pos += 8 # skip map header
        self.tilemap1 = Tilemap()
        self.tilemap1.width = ord(self.data[pos])
        self.tilemap1.height = ord(self.data[pos+2])
        pos += 5
        dlen = len(self.data)
        for i in range(self.tilemap1.width * self.tilemap1.height):
            if (pos + i) >= dlen:
                # i dunno why this happens...
                print "exceeded level data..."
                break
            else:
                self.tilemap1.tiles.append(ord(self.data[pos + i]))
        pos += self.tilemap1.width * self.tilemap1.height
        
        pos += 8 # skip map header
        self.tilemap2 = Tilemap()
        self.tilemap2.width = ord(self.data[pos])
        self.tilemap2.height = ord(self.data[pos+2])
        pos += 5
        dlen = len(self.data)
        for i in range(self.tilemap2.width * self.tilemap2.height):
            if (pos + i) >= dlen:
                # i dunno why this happens...
                print "exceeded level data..."
                break
            else:
                self.tilemap2.tiles.append(ord(self.data[pos + i]))
        pos += self.tilemap2.width * self.tilemap2.height
        
            
class Tilemap:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.tiles = []
        
    def get_tile(self,x,y):
        return self.tiles[(x % self.width)+(y * self.width)]
        
    def set_tile(self,x,y,index):
        self.tiles[(x % self.width)+(y * self.width)] = index
        
    def to_data(self):
        output = "pxMAP01"
        output += chr(0)
        output += chr(self.width)
        output += chr(0)
        output += chr(self.height)
        output += chr(0)
        for t in self.tiles:
            output += chr(t)
        return output
        
        
class Script:
    def __init__(self,data):
        self.data = data
        
if __name__ == "__main__":
    #debug sturr
    
    p_path = r"C:\Stuff\Games\PinkHourEnhack\rsc_p"
    pr = KRes(p_path)
    
    # test reading tiles
    pf = pr.field['00title']
    # print "{} , {}".format(pf.width,pf.height)
    # print pf.tiledat