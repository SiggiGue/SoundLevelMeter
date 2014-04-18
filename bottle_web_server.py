from bottle import route, run, template
import socket

@route('/slm')
def index():
    with open('slm.html') as f:
        filestring = f.read()
        filestring = filestring.replace('localhost', socket.gethostbyname(socket.gethostname()))
        return filestring


run(host='0.0.0.0', port=9090)  # listens on all ip-addresses in the LAN
# run(host='localhost', port=9090)  #listens only on own ip address (localhost)
