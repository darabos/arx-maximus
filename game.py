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
for s in js.document.getElementsByTagName('link'):
  s.remove()
def loadfont(name):
  link = js.document.createElement('link')
  link.setAttribute('rel', 'stylesheet')
  link.setAttribute('href', f'https://fonts.googleapis.com/css?family={name.replace(" ", "+")}&display=swap')
  js.document.head.appendChild(link)
loadfont('Cinzel Decorative')
loadfont('Metamorphous')
style = js.document.createElement('style')
S = 2
style.innerHTML = f'''

body {{
  background: #786aff;
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

.color-0 {{
  background: #8363ad;
}}
.color-1 {{
  background: #58a23c;
}}
.color-2 {{
  background: #5a4142;
}}
.color-3 {{
  background: #3e489d;
}}
.color-4 {{
  background: #c14867;
}}

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

nextid = 0
def add(cls, x, y, color):
  global nextid
  js.document.body.insertAdjacentHTML(
      'beforeend', f'<div class="{cls} color-{color}" id="{cls}-{nextid}"></div>')
  e = js.document.getElementById(f'{cls}-{nextid}')
  e.setAttribute('style', f'left: {S * x}vw; top: {S * y}vw;')
  nextid += 1
  return e

def highlight(e):
  e.classList.add('highlighted')

def addbox(x, y, color):
  return add('box', x, y, color)

def adddot(x, y, color):
  return add('dot', x, y, color)

W = 6
import random

def randompattern():
  lastcolor = -1
  pattern = []
  while len(pattern) < W:
    c = random.randrange(5)
    while c == lastcolor:
      c = random.randrange(5)
    lastcolor = c
    l = random.randrange(W)
    if len(pattern) + l > W:
      l = W - len(pattern)
    pattern += [c] * l
  return pattern

p = randompattern()
for i, c in enumerate(p):
  b = adddot(10 + i, 10, c)
b = addbox(11, 11, 4)
b = addbox(12, 11, 3)
b = addbox(13, 11, 2)
b = addbox(14, 11, 1)
b = addbox(15, 11, 0)
highlight(b)
print(b)
