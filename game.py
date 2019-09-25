try:
  import js
except ImportError:
  import http.server
  import socketserver
  with socketserver.TCPServer(('', 8000), http.server.SimpleHTTPRequestHandler) as httpd:
    print('Running as http://localhost:8000/')
    httpd.serve_forever()

import sys
print(sys.version)

for s in js.document.getElementsByTagName('style'):
  s.remove()
def loadfont(name):
  link = js.document.createElement('link')
  link.setAttribute('rel', 'stylesheet')
  link.setAttribute('href', f'https://fonts.googleapis.com/css?family={name.replace(" ", "+")}&display=swap')
  js.document.head.appendChild(link)
style = js.document.createElement('style')
S = 2
COLORS = ['#8363ad', '#58a23c', '#5a4142', '#3e489d', '#c14867']
CS = len(COLORS)
color_styles = '\n'.join(f'.color-{i} {{ background: {c}; }}' for (i, c) in enumerate(COLORS))
style.innerHTML = f'''

body {{
  background: #a7b5ba;
  font-family: Metamorphous, sans-serif;
  font-size: 1vw;
  color: #f0e9cf;
  text-shadow: 0 1px 2px #0b0b0b80;
}}
h1 {{
  font-family: 'Cinzel Decorative', sans-serif;
  font-size: 5vw;
  text-align: center;
}}
h2 {{
  margin-top: -4vw;
  text-align: center;
}}

.box {{
  position: absolute;
  width: calc({S}vw - 1px);
  height: calc({S}vw - 1px);
  border: 1px solid #0b0b0b;
  border-radius: 0.3vw;
}}
.dot {{
  position: absolute;
  width: {S / 3}vw;
  height: {S / 3}vw;
  margin: {S / 3}vw;
  border: 1px solid #0b0b0b;
  border-radius: 0.3vw;
}}
.clicky {{
  cursor: pointer;
}}
{ color_styles }

.highlighted {{
  animation: blink 0.3s infinite alternate;
}}
@keyframes blink {{
  from {{ background-color: white; }}
  to {{ }}
}}

'''
js.document.head.appendChild(style)

js.document.body.innerHTML = ''
js.document.body.insertAdjacentHTML('beforeend', '''

<h1>Arx Maximus</h1>
<h2>How the world’s greatest citadel was built

''')

def setpos(e, x, y):
  e.setAttribute('style', f'left: {S * x}vw; top: {S * y}vw;')
  e.x = x
  e.y = y
nextid = 0
def add(cls, x, y, color):
  global nextid
  js.document.body.insertAdjacentHTML(
      'beforeend', f'<div class="{cls} color-{color}" id="{cls}-{nextid}"></div>')
  e = js.document.getElementById(f'{cls}-{nextid}')
  e.color = color
  setpos(e, x, y)
  nextid += 1
  return e

def addbox(x, y, color):
  return add('box', x, y, color)

def adddot(x, y, color):
  return add('dot', x, y, color)

import random

def randompattern(w):
  lastcolor = -1
  pattern = []
  while len(pattern) < w:
    c = random.randrange(CS)
    while c == lastcolor:
      c = random.randrange(CS)
    lastcolor = c
    l = random.randrange(5) + 1
    if len(pattern) + l > w:
      l = w - len(pattern)
    pattern += [c] * l
  return pattern

def package(size):
  cs = []
  for i in range(size * size):
    cs.append(random.randrange(CS))
  base = random.randrange(CS)
  cs.sort(key=lambda c: (c + base) % CS)
  return cs

def makepackage(x, y, size):
  p = package(size)
  boxes = []
  for i, c in enumerate(p):
    if (i // size) % 2 == 0:
      b = addbox(x + i // size, y + 1 - size + i % size, c)
    else:
      b = addbox(x + i // size, y - i % size, c)
    b.onmouseenter = lambda _, c=c: highlight(c, boxes)
    b.onmouseleave = lambda _, c=c: unhighlight(c, boxes)
    b.onclick = lambda _, c=c: click(c, boxes)
    b.classList.add('clicky')
    boxes.append(b)
  return boxes

def highlight(c, bs):
  for b in bs + dots:
    if b.color == c:
      b.classList.add('highlighted')
def unhighlight(c, bs):
  for b in bs + dots:
    if b.color == c:
      b.classList.remove('highlighted')

def click(c, bs):
  if bs in caravan_boxes:
    caravan_boxes.remove(bs)
  unhighlight(c, bs + dots)
  matching = 0
  for b in bs:
    b.remove()
    if b.color == c:
      matching += 1
    else:
      stacks[int(b.color)] += 1
  update_stacks()
  for d in dots[:]:
    if d.color == c and matching:
      d.remove()
      dots.remove(d)
      matching -= 1
      t = addbox(d.x, d.y, c)
      tower.append(t)
      ds, _, _ = dotspan(int(d.index))
      for d in ds:
        d.classList.remove('clicky')
        d.onclick = None
        d.onmouseenter = None
        d.onmouseleave = None
  global garbage
  garbage += matching
  update_garbage()
  if not dots:
    new_floor()
  check_caravan()

def check_caravan():
  if garbage == 0 and not caravan_boxes and sum(stacks) == 0:
    new_caravan()

garbage = 0
garbage_boxes = []
stacks = [0] * CS
stack_boxes = [[] for _ in range(CS)]
tower = []

def update_pile(pile, x, y, count, color):
  for b in pile:
    b.remove()
  del pile[:]
  for i in range(count):
    b = addbox(x, y - i, color)
    if isinstance(color, str):
      b.setAttribute('style', b.getAttribute('style') + f' background-color: {color};')
    pile.append(b)

def update_stacks():
  for c, count in enumerate(stacks):
    update_pile(stack_boxes[c], x + c, 11, count, c)
    for b in stack_boxes[c]:
      b.classList.add('clicky')
      b.onmouseenter = lambda _, c=c: highlight(c, stack_boxes[c] + dots)
      b.onmouseleave = lambda _, c=c: unhighlight(c, stack_boxes[c] + dots)
      b.onclick = lambda _, c=c: clearandclick(c)
  def clearandclick(c):
    stacks[c] = 0
    click(c, stack_boxes[c])

def update_garbage():
  update_pile(garbage_boxes, 1, 11, garbage, '#566262')
  for b in garbage_boxes:
    b.classList.add('clicky')
    b.onmouseenter = lambda _, b=b: b.classList.add('highlighted')
    b.onmouseleave = lambda _, b=b: b.classList.remove('highlighted')
    b.onclick = lambda _: pop_garbage()
  def pop_garbage():
    global garbage
    garbage -= 1
    update_garbage()
    check_caravan()

tower_width = 10

dots = []
pattern = []
def new_floor():
  for t in tower:
    setpos(t, t.x, t.y + 1)
  x = 3
  global pattern
  pattern = randompattern(tower_width)
  for i, c in enumerate(pattern):
    d = adddot(x, 11, c)
    d.color = c
    d.index = i
    d.onclick = lambda _, i=i: changedot(i)
    d.onmouseenter = lambda _, i=i: highlightdot(i)
    d.onmouseleave = lambda _, i=i: unhighlightdot(i)
    d.classList.add('clicky')
    dots.append(d)
    x += 1

def dotspan(i):
  c = pattern[i]
  span = []
  before = -1
  after = -1
  for j, p in enumerate(pattern):
    if p == c:
      span.append(j)
    elif j < i:
      span = []
      before = p
    else:
      after = p
      break
  c2 = (c + 1) % CS
  while c2 == before or c2 == after:
    c2 = (c2 + 1) % CS
  ds = [d for d in dots if d.index in span]
  return ds, c, c2

def changedot(i):
  ds, c, c2 = dotspan(i)
  for d in ds:
    pattern[int(d.index)] = c2
    d.color = c2
    d.classList.remove(f'color-{c}')
    d.classList.add(f'color-{c2}')
def highlightdot(i):
  ds, _, _ = dotspan(i)
  for d in ds:
    d.classList.add('highlighted')
def unhighlightdot(i):
  ds, _, _ = dotspan(i)
  for d in ds:
    d.classList.remove('highlighted')

package_sizes = [3, 2, 2]
caravan_boxes = []

def new_caravan():
  x = 6 + tower_width
  for s in package_sizes:
    caravan_boxes.append(makepackage(x, 10, s))
    x += s + 2

new_floor()
new_caravan()
