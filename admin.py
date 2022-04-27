from bottle import static_file,route,run,jinja2_view,TEMPLATE_PATH,request
from settings import STATIC_FILES,TEMPLATES,BD
from sql import Sql
from clase_post import Posts


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
@jinja2_view('admin_index.html')
def home():
    bdatos = Sql(BD)
    resp = bdatos.select('select p.id, p.fecha,p.autor,p.titulo,p.cuerpo from posts p ')
    resp = modifica_fecha(resp)
    return {'posts' : resp}

@route('/editar')
@route('/editar/<id:int>')
@jinja2_view('form_post.html')
def mi_form(id=None):
    bdatos = Sql(BD)
    if id:
        resp = bdatos.select(f'select p.id, p.fecha,p.autor,p.titulo,p.cuerpo from posts p where id = {id}')
    
    #resp = modifica_fecha(resp)
    return {'posts' : resp[0]}


@route('/guardar', method='POST')
def guardar(): 
    if request.POST.id:
        id = request.POST.id
    else:
        id = None

    fecha = request.POST.fecha
    autor = request.POST.autor
    titulo = request.POST.titulo
    cuerpo = request.POST.cuerpo
   
    p = Posts(id,fecha,autor,titulo,cuerpo)
    
    bdatos = Sql(BD)
    if request.POST.id:
        resp = bdatos.update(p)
    else:
        resp = bdatos.insert(p)

    return resp


run(host='localhost', port=8000,debug=True,reloader=True)

