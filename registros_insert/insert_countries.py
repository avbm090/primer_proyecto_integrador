import logging
from sqlalchemy import text
from .base import InsercionBase

class InsertarPais(InsercionBase):
    def ejecutar(self, session):
        nombre = input("Ingrese nombre del país: ")
        codigo = input("Ingrese código del país: ")

        logging.info(f"Insertando país: {nombre} (Código: {codigo})")

        try:
            session.execute(text("SET @resultado = '';"))
            session.execute(
                text("CALL InsertCountry(:nombre, :codigo, @resultado);"),
                {'nombre': nombre, 'codigo': codigo}
            )
            resultado = session.execute(text("SELECT @resultado;")).fetchone()[0]

            session.commit()
            logging.info(f"País '{nombre}' insertado. Mensaje: {resultado}")
            print(resultado)

        except Exception as e:
            session.rollback()
            logging.error(f"Error al insertar país '{nombre}': {e}", exc_info=True)
            print(f"Error al insertar país: {e}")
