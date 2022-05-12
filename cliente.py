from bottle import static_file,route,run,jinja2_view,TEMPLATE_PATH,request,redirect
from settings import STATIC_FILES,BD,TEMPLATES
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
        
def tupla_a_lista(mi_lista_tupla):
    salida = []
    for t in mi_lista_tupla:
        salida.append(t[0]) #Suponemos que el id está en el primer lugar
    
    return salida

def cadena_a_lista(mi_cadena):
    return mi_cadena.split(',')

def conjunto_partes(lista_etq):
    """
    
    Recibe la cadena de etiquetas o categorias,
    la parte con cadena_a_lista y devuelve un conjunto en forma de lista.
    
    """
    lista_total = []
    for etq in lista_etq:
        lista = cadena_a_lista(etq[0])
        lista_total += lista
    return list(set(lista_total))





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
    return {'post' : resp[0],
            'etiquetas': cadena_a_lista(resp[0][6]),
            'categorias':cadena_a_lista(resp[0][5])}


@route('/filtro/<etiqueta>')
@jinja2_view('index.html')
def ver_post(etiqueta):
    bdatos = Sql(BD)
    resp = bdatos.select(f'select * from posts p Where etiquetas like "%{etiqueta}%"')
    return {'posts': resp}

@route('/etiquetas')
@jinja2_view('etiquetas.html')
def ver_etiquetas():
    bdatos = Sql(BD)
    resp = bdatos.select(f'select p.etiquetas from posts p')
    conjunto = conjunto_partes(resp)
    return {}

# Parte de Administración

@route('/admin/')
@jinja2_view('admin_index.html')
def home():
    bdatos = Sql(BD)
    resp = bdatos.select('select p.id, p.fecha,p.autor,p.titulo,p.cuerpo,p.etiquetas,p.categorias from posts p ')
    resp = modifica_fecha(resp)
    return {'posts' : resp}

@route('/admin/editar')
@route('/admin/editar/<id:int>')
@jinja2_view('form_post.html')
def mi_form(id=None):
    bdatos = Sql(BD)
    posts = None
    # etiquetas = bdatos.select('select id,nombre from T_etiquetas;')
    # categorias = bdatos.select('select id,nombre from T_categorias;')
    if id: #Estamos editando el post
        posts = bdatos.select(f'select p.id, p.fecha,p.autor,p.titulo,p.cuerpo,p.etiquetas,p.categorias from posts p where id = {id};')
        # post_etiquetas = bdatos.select(f'select id_etiqueta from posts p join post_etiquetas pe on p.id = pe.id_post where p.id = {id};')
        # post_categorias = bdatos.select(f'select pc.id_categoria from posts p join post_categorias pc on p.id = pc.id_post where p.id = {id};')

        # mis_categorias = tupla_a_lista(post_categorias)
        # mis_etiquetas = tupla_a_lista(post_etiquetas)
    
    #resp = modifica_fecha(resp)

        if posts:
    #     return {'post' : posts[0], 
    #             'etiquetas' : etiquetas,
    #             'categorias': categorias,
    #             'mis_etiquetas' : mis_etiquetas, 
    #             'mis_categorias': mis_categorias}
            return {'post' : posts[0]}
    else:
        # return {'post' : '', 
        #         'etiquetas' : etiquetas,
        #         'categorias': categorias}
        return {'post': ''}

@route('/admin/guardar', method='POST')
def guardar(): 
    if request.POST.id:
        id = request.POST.id
    else:
        id = None

    fecha = request.POST.fecha
    autor = request.POST.autor
    titulo = request.POST.titulo
    cuerpo = request.POST.cuerpo
    categorias = request.POST.categorias
    etiquetas = request.POST.etiquetas
    
   
    p = Posts(id,fecha,autor,titulo,cuerpo,categorias,etiquetas)
    
    bdatos = Sql(BD)
    if request.POST.id:
        resp = bdatos.update(p)
    else:
        resp = bdatos.insert(p)

    redirect('/admin/')


@route('/admin/borrar')
@route('/admin/borrar/<id:int>')
def borrar(id):
    p = Posts(id=id)
    bdatos = Sql(BD)
    bdatos.delete(p)

    redirect('/admin/')

@route('/admin/post')
@route('/admin/post/<id:int>')
@jinja2_view('form_post.html')
def ver_post(id=None):
    if id:
        bdatos = Sql(BD)
        resp = bdatos.select(f'select * from posts where id ={id}')
        return {'post' : resp[0]}
    else:
        return {'post':None}


run(host='localhost', port=8000,debug=True,reloader=True)

