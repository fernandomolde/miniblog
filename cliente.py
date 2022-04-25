from bottle import static_file,route,run,jinja2_view,TEMPLATE_PATH
from settings import STATIC_FILES,BD,TEMPLATES
from sql import Sql



TEMPLATE_PATH.append(TEMPLATES)

@route('/static/<filename:path>')
def server_static(filename):
    archivo = static_file(filename, root=STATIC_FILES)
    return archivo

@route('/')
@jinja2_view('index.html')
def home():
    bdatos = Sql(BD)
    resp = bdatos.select('select * from posts')
    return {'posts' : resp}


@route('/post/<id:int>')
@jinja2_view('post.html')
def ver_post(id):
    bdatos = Sql(BD)
    resp = bdatos.select(f'select * from posts where id ={id}')
    return {'post' : resp[0]}




run(host='localhost', port=8000,debug=True,reloader=True)

