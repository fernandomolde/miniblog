from bottle import static_file,route,run
from settings import STATIC_FILES

@route('/static/<filename:path>')
def server_static(filename):
    archivo = static_file(filename, root=STATIC_FILES)
    return archivo

@route('/')
def home():
    return 'Hola Mundo'







run(host='localhost', port=8000,debug=True,reloader=True)

