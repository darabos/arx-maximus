try:
  import js
except ImportError:
  import http.server
  import socketserver
  with socketserver.TCPServer(('', 8000), http.server.SimpleHTTPRequestHandler) as httpd:
    print('Running as http://localhost:8000/')
    httpd.serve_forever()

import sys
js.console.log(sys.version)
js.document.body.innerHTML = ''
js.document.body.insertAdjacentHTML('beforeend', '<h1 id="hello">hello</h1>')
e = js.document.getElementById('hello')
try:
  js.window.cancelAnimationFrame(nextAnimationFrame)
except:
  pass
count = 0
def anim(t):
  global count, nextAnimationFrame
  count += 1
  e.innerText = f'hello {count}'
  nextAnimationFrame = js.window.requestAnimationFrame(anim)
nextAnimationFrame = js.window.requestAnimationFrame(anim)
