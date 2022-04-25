import sqlite3

class Sql():
    __cnx = None
    def __init__(self,bd) -> None:
        self.__bd = bd
    
    def conectar(self):
        if self.__cnx is None:
            self.__cnx = sqlite3.connect(self.__bd)
        return self.__cnx

    def insert(self, articulo):
        cnx = self.conectar()
        cur= cnx.cursor()
        consulta = self.prepara_insert(articulo)
        cur.execute(consulta)
        new_id = cur.lastrowid
        cnx.commit()
        return new_id
    
    def select(self, consulta):
        cnx = self.conectar()
        cur = cnx.cursor()
        cur.execute(consulta)
        filas = cur.fetchall()
        return filas

    def delete(self,articulo):
        tabla = type(articulo).__name__.lower()
        consulta = f'delete from {tabla} where id="{articulo.id}"'
        cnx = self.conectar()
        cur = cnx.cursor()
        cur.execute(consulta)
        cnx.commit()
    
    def update(self,articulo):
        consulta = self.prepara_update(articulo)
        cnx = self.conectar()
        cur = cnx.cursor()
        cur.execute(consulta)
        cnx.commit()

    def prepara_insert(self,articulo):
        tabla = type(articulo).__name__.lower()
        campos = tuple(vars(articulo).keys())
        datos = vars(articulo)
        valores = ''
        campos = ''
        for k,v in datos.items():
            if k != 'id':
                valores += f"'{str(v)}',"
                campos += f'{k},'
        consulta = f"insert into {tabla}({campos[:-1]}) values ({valores[:-1]});"
        return consulta
        
    def prepara_update(self,articulo):
        tabla = type(articulo).__name__.lower()
        campos = vars(articulo)
        valores = ''
        for k,v in campos.items():
            if k != 'id':
                valores += f"{k}='{str(v)}',"
        consulta = f"update {tabla} set {valores[:-1]} where id = '{articulo.id}';"
        return consulta