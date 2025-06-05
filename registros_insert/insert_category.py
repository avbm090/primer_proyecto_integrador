from sqlalchemy import text
from .base import InsercionBase


class InsertarCategoria(InsercionBase):
    def ejecutar(self, session):
        nombre = input("Ingrese nombre de la categoría: ")

        session.execute(text("SET @resultado = '';"))
        session.execute(text("CALL InsertCategory(:nombre, @resultado);"), {'nombre': nombre})
        
        resultado = session.execute(text("SELECT @resultado;")).fetchone()[0]
        
        session.commit()
        
        print(resultado)
