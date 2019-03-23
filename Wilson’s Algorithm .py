import pygame as py
import random
from matplotlib import colors as mcolors
py.init()

w, h = 1401, 801
size = 20

rows, cols = h//size, w//size
screen = py.display.set_mode((w,h))

black = (0,0,0)
white = (255,255,255)
green = (0,255,0,50)
red = (121,63,13)

class Cell:
  def __init__(self, i, j):
    self.i = i
    self.j = j
    self.wall = [True]*4
    self.visited = False

  def show(self, colour):
    py.draw.rect(screen, colour, (self.i * size, self.j * size, size, size))

  def walls(self):
    i = self.i * size
    j = self.j * size
    if self.wall[0]:  # top
      py.draw.line(screen, black, (i, j), (i + size, j))
    if self.wall[1]:  # right
      py.draw.line(screen, black, (i + size, j + size), (i + size, j))
    if self.wall[2]:  # bottom
      py.draw.line(screen, black, (i + size, j + size), (i, j + size))
    if self.wall[3]:  # left
      py.draw.line(screen, black, (i, j), (i, j + size))

  def check_neighbours(self):
    x = self.i
    y = self.j
    neighbours = []
    top = index(x, y - 1)
    right = index(x + 1, y)
    bottom = index(x, y + 1)
    left = index(x - 1, y)
    probability = [27,20,25,30]
    if top != 0:
      temp = [Cells[top]]*probability[0]
      neighbours.extend(temp)
    if right != 0:
      temp = [Cells[right]]*probability[1]
      neighbours.extend(temp)
    if bottom != 0:
      temp = [Cells[bottom]]*probability[2]
      neighbours.extend(temp)
    if left != 0:
      temp = [Cells[left]]*probability[3]
      neighbours.extend(temp)

    if len(neighbours) > 0:
      return neighbours[random.randint(0, len(neighbours) - 1)]
    else:
      return 0

Cells, Cells_Maze, Branch, New_Branch = [], [], [], []

for j in range(rows):
  for i in range(cols):
    cell = Cell(i,j)
    Cells.append(cell)

target = Cells[(rows//2)*cols + rows//2 - 1]
current = Cells[-3]
Cells_Maze.append(target)
nextcell = -1

def get_current():
  global Cells_Maze, Cells, nextcell
  try:
    temp = Cells[nextcell]
    if temp in Cells_Maze:
      nextcell -= 1
      return get_current()
    else:
      return temp
  except IndexError:
    return 0

def branch():
  global current, Cells_Maze, Branch, New_Branch

  if len(Branch) > 0:
    if current in Cells_Maze:
      Cells_Maze += Branch
      New_Branch = Branch
      New_Branch.append(current)
      remove_walls()
      New_Branch.clear()
      Branch.clear()
      current = get_current()
      if current == 0:
        return 0

  if current in Branch:
    for k,cell in enumerate(Branch):
      if cell == current:
        if k == 0:
          Branch.clear()
          break
        else:
          current = Branch[k-1]
          Branch = Branch[:k]
          break

  new = current.check_neighbours()
  if new != 0 and new != current:
    Branch.append(current)
    current = new

def index(x, y):
  if x < 0 or y < 0 or x > cols - 1 or y > rows - 1:
    return 0
  return x + y * cols

def remove_walls():
  global New_Branch
  for cell in range(0,len(New_Branch)-1):
    a = New_Branch[cell]
    b = New_Branch[cell+1]
    x = a.i - b.i
    if x == 1:
      a.wall[3] = False
      b.wall[1] = False
    elif x == -1:
      a.wall[1] = False
      b.wall[3] = False
    y = a.j - b.j
    if y == 1:
      a.wall[0] = False
      b.wall[2] = False
    elif y == -1:
      a.wall[2] = False
      b.wall[0] = False

clock = py.time.Clock()
game = True
while game:
    for event in py.event.get():
        if event.type == py.QUIT:
            game = False
            py.quit()
    screen.fill(black)

    pause = branch()
    if pause == 0:
      game = False
    for cell in Branch:
      cell.show(green)
    for cell in Cells_Maze:
      cell.show(red)
      cell.walls()

    py.display.update()
    clock.tick(120)

stack = []
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
colors = [tuple(255*mcolors.hsv_to_rgb(hsv)) for hsv,name in by_hsv]
colors = colors[5:]
temp = 0
def color(x):
  global temp, COLOR
  a, b = x.i, x.j
  stack.append(x)
  if not x.wall[0]:
    top = Cells[index(a, b - 1)]
    if top not in stack:
      top.show(COLOR)
      top.walls()
      py.display.update()
      clock.tick(30)
      color(top)
  if not x.wall[1]:
    right = Cells[index(a + 1, b)]
    if right not in stack:
      right.show(COLOR)
      right.walls()
      py.display.update()
      clock.tick(30)
      color(right)
  if not x.wall[2]:
    bottom = Cells[index(a, b + 1)]
    if bottom not in stack:
      bottom.show(COLOR)
      bottom.walls()
      py.display.update()
      clock.tick(30)
      color(bottom)
  if not x.wall[3]:
    left = Cells[index(a - 1, b)]
    if left not in stack:
      left.show(COLOR)
      left.walls()
      py.display.update()
      clock.tick(30)
      color(left)
  temp += 1
  try:
    COLOR = colors[temp]
  except:
    temp = 0
    COLOR = colors[temp]

COLOR = colors[0]
current = Cells[0]
while True:
  for event in py.event.get():
    if event.type == py.QUIT:
      py.quit()

  try:
    current.show(COLOR)
    current.walls()
    color(current)
  except:
    pass
