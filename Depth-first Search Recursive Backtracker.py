import pygame as py
import random
py.init()

class Cell:

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True]*4
        self.visited = False

    def show(self, color = (121,63,13)):
        i = self.i*size
        j = self.j*size
        if self.visited:
            py.draw.rect(screen, color, (self.i * size, self.j * size, size, size))
        if self.walls[0]: #top
            py.draw.line(screen, white, (i,j), (i+size,j))
        if self.walls[1]: #right
            py.draw.line(screen, white, (i+size,j+size), (i+size,j))
        if self.walls[2]: #bottom
            py.draw.line(screen, white, (i+size,j+size), (i,j+size))
        if self.walls[3]: #left
            py.draw.line(screen, white, (i,j), (i,j+size))

    def highlight(self, color = (0,255,0,50)):
        py.draw.rect(screen, color, (self.i*size,self.j*size,size,size))

    def check_neighbours(self):
        i = self.i
        j = self.j
        neighbours = []
        top = cells[index(i,j-1)]
        right = cells[index(i+1,j)]
        bottom = cells[index(i,j+1)]
        left = cells[index(i-1,j)]

        if top != 0 and not top.visited:
            neighbours.append(top)
        if right != 0 and not right.visited:
            neighbours.append(right)
        if bottom != 0 and not bottom.visited:
            neighbours.append(bottom)
        if left !=  0 and not left.visited:
            neighbours.append(left)

        if len(neighbours) > 0:
            return neighbours[random.randint(0, len(neighbours)-1)]
        else:
            return 0

w, h = 801, 801
size = 30
rows, cols = h//size, w//size
screen = py.display.set_mode((w,h))

black = (0,0,0)
white = (255,255,255)
red = (121,63,13)
blue = (0,0,255,100)
green = (0,255,0,50)

cells, stack = [], []
for j in range(rows):
    for i in range(cols):
        cell = Cell(i,j)
        cells.append(cell)
current = cells[0]

def run():
    global current
    current.visited = True
    for cell in cells:
        cell.show()
    current.highlight()
#Step 1
    new = current.check_neighbours()
    if new != 0:
        new.visited = True
#Step 2
        stack.append(current)
#Step 3
        remove_walls(current,new)
#Step 4
        current = new
    elif len(stack) > 0:
        current = stack.pop()

def index(i,j):
    if i < 0 or j < 0 or i > cols-1 or j > rows-1:
        return 0
    return i + j*cols

def remove_walls(current, new):
    x = current.i - new.i
    if x == 1:
        current.walls[3] = False
        new.walls[1] = False
    elif x == -1:
        current.walls[1] = False
        new.walls[3] = False
    y = current.j - new.j
    if y == 1:
        current.walls[0] = False
        new.walls[2] = False
    elif y == -1:
        current.walls[2] = False
        new.walls[0] = False

clock = py.time.Clock()
game = True
while game:
    for event in py.event.get():
        if event.type == py.QUIT:
            game = False
            py.quit()
    screen.fill(black)
    run()
    py.display.update()
    clock.tick(60)


