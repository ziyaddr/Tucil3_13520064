from shutil import move
import numpy as np
import timeit
import bisect
import copy


class Tree:
    accessedMat = set() # static
    livingNode = [] # static
    nodeCount = [0] # static
    steps = [] # static
    timeElapsed = [0] # static

    def __init__(self, parent, matrix, fx, gx, lastMove):
        self.parent = parent
        self.matrix = matrix
        self.fx = fx
        self.gx = gx
        self.lastMove = lastMove
        hashed = self.matrix.hash()
        if hashed not in self.accessedMat:
            bisect.insort_right(self.livingNode, self, key=totalCost)
            self.accessedMat.add(hashed)
            self.nodeCount[0] += 1
    
    def expand(self):
        self.livingNode.remove(self)
        if self.lastMove != "down" and self.matrix.pos_16r > 0:
            mat = self.matrix.move('u')
            self.uChild = Tree(self, mat, self.fx+1, mat.getIncorrectTile(), 'u')
        if self.lastMove != "up" and self.matrix.pos_16r < 3:
            mat = self.matrix.move('d')
            self.uChild = Tree(self, mat, self.fx+1, mat.getIncorrectTile(), 'd')
        if self.lastMove != "right" and self.matrix.pos_16c > 0:
            mat = self.matrix.move('l')
            self.uChild = Tree(self, mat, self.fx+1, mat.getIncorrectTile(), 'l')
        if self.lastMove != "left" and self.matrix.pos_16c < 3:
            mat = self.matrix.move('r')
            self.uChild = Tree(self, mat, self.fx+1, mat.getIncorrectTile(), 'r')
    
    def solve(self):
        start = timeit.default_timer()
        while self.livingNode[0].matrix.getIncorrectTile() != 0:
            self.livingNode[0].expand()
        self.livingNode[0].getSteps()
        end = timeit.default_timer()
        self.timeElapsed[0] = end-start
        return self.livingNode[0]

    def getSteps(self):
        p = self
        while p.parent != None:
            p.steps.insert(0, p.lastMove)
            p = p.parent
    
    def reset():
        Tree.livingNode = []
        Tree.steps = []
        Tree.accessedMat = set()
        Tree.nodeCount = [0]
        Tree.timeElapsed = [0]
    


class Matrix:
    buffer = np.matrix
    pos_16r: int
    pos_16c: int
    
    def __init__(self):
        self.buffer = np.matrix("0")
        self.pos_16c = 0
        self.pos_16r = 0
    
    def readFile(self, filename):
        self.buffer = np.genfromtxt(filename).astype(int)
        for i in range(4):
            for j in range(4):
                if (self.buffer[i, j] == 16):
                    self.pos_16r = i
                    self.pos_16c = j

    def randomize(self):
        random = np.random.permutation([i+1 for i in range(16)])
        self.buffer = np.asmatrix(np.array_split(random, 4))
        for i in range(4):
            for j in range(4):
                if (self.buffer[i, j] == 16):
                    self.pos_16r = i
                    self.pos_16c = j


        

    def Kurang(self, num):
        found = False
        count = 0
        for i in range(4):
            for j in range(4):
                if (not found):
                    if (self.buffer[i, j] == num):
                        found = True
                else:
                    if (self.buffer[i, j] < num):
                        count += 1
        return count

    def TotalKurang(self):
        count = 0
        for i in range(16):
            count += self.Kurang(i+1)
        return count

    def isSolveable(self):
        return (self.TotalKurang() + ((self.pos_16r%2)^(self.pos_16c%2)))%2 == 0

    def switch(self, i1, j1, i2, j2):
        self.buffer[i1,j1], self.buffer[i2,j2] = self.buffer[i2,j2], self.buffer[i1,j1]


    def move(self, dir):
        mat_cpy = copy.deepcopy(self)
        if dir == 'u' and self.pos_16r > 0:
            mat_cpy.switch(self.pos_16r, self.pos_16c, self.pos_16r-1, self.pos_16c)
            mat_cpy.pos_16r -= 1
        elif dir == 'd' and self.pos_16r < 3:
            mat_cpy.switch(self.pos_16r, self.pos_16c, self.pos_16r+1, self.pos_16c)
            mat_cpy.pos_16r += 1
        elif dir == 'l' and self.pos_16c > 0:
            mat_cpy.switch(self.pos_16r, self.pos_16c, self.pos_16r, self.pos_16c-1)
            mat_cpy.pos_16c -= 1
        elif dir == 'r' and self.pos_16c < 3:
            mat_cpy.switch(self.pos_16r, self.pos_16c, self.pos_16r, self.pos_16c+1)
            mat_cpy.pos_16c += 1
        return mat_cpy
    
    def getIncorrectTile(self):
        count = 0
        for i in range(4):
            for j in range(4):
                number = i*4+j+1
                if number != self.buffer[i, j] and number != 16:
                    count += 1
        return count
    
    def hash(self):
        str = ""
        for i in range(4):
            for j in range(4):
                str += f"{self.buffer[i, j]:02d}"
        return str



    
def num_to_x(num):
    return num//4
def num_to_y(num):
    return num%4
def totalCost(tree):
    return tree.gx







