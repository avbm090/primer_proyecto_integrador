import logging
from sqlalchemy import text
from .base import InsercionBase

class InsertarCiudad(InsercionBase):
    def ejecutar(self, session):
        nombre = input("Ingrese nombre de la ciudad: ")
        zipcode = input("Ingrese código postal: ")
        nombre_pais = input("Ingrese nombre del país: ")

        logging.info(f"Insertando ciudad: {nombre}, CP: {zipcode}, País: {nombre_pais}")

        try:
            resultado = session.execute(
                text("SELECT CountryID FROM countries WHERE CountryName = :nombre_pais"),
                {'nombre_pais': nombre_pais}
            ).fetchone()

            if resultado is None:
                logging.warning(f"País '{nombre_pais}' no encontrado en la base de datos")
                print(f"Error: país '{nombre_pais}' no encontrado.")
                return

            country_id = resultado[0]
            logging.info(f"ID del país '{nombre_pais}' encontrado: {country_id}")

            result = session.execute(
                text("CALL InsertCity(:nombre, :zipcode, :country_id, @p_ResultMessage); SELECT @p_ResultMessage;"),
                {'nombre': nombre, 'zipcode': zipcode, 'country_id': country_id}
            )
            mensaje = result.fetchone()[0]
            session.commit()
            logging.info(f"Ciudad '{nombre}' insertada. Mensaje: {mensaje}")
            print(mensaje)

        except Exception as e:
            session.rollback()
            logging.error(f"Error al insertar ciudad '{nombre}': {e}", exc_info=True)
            print(f"Error al insertar ciudad: {e}")
