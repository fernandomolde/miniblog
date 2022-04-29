from bottle import static_file,route,run,jinja2_view,TEMPLATE_PATH
from settings import STATIC_FILES,BD,TEMPLATES
from sql import Sql



TEMPLATE_PATH.append(TEMPLATES)

def modifica_fecha(lista_tuplas):
    salida = []
    tmp_tupla = ()
    for t in lista_tuplas:
        cadena_fecha = ''
        partes = t[1].split('-')
        cadena_fecha = partes[2] + ' de ' + partes[1] + 'de ' + partes[0]
        tmp_tupla = (t[0], cadena_fecha, t[2],t[3],t[4])
        salida.append(tmp_tupla)
    return salida
        

@route('/static/<filename:path>')
def server_static(filename):
    archivo = static_file(filename, root=STATIC_FILES)
    return archivo

@route('/')
@jinja2_view('index.html')
def home():
    bdatos = Sql(BD)
    resp = bdatos.select('select * from posts')
    resp = modifica_fecha(resp)
    return {'posts' : resp}


@route('/post/<id:int>')
@jinja2_view('post.html')
def ver_post(id):
    bdatos = Sql(BD)
    resp = bdatos.select(f'select * from posts where id ={id}')
    return {'post' : resp[0]}




run(host='localhost', port=8000,debug=True,reloader=True)

