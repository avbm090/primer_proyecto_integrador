import logging
from sqlalchemy import text
from .base import InsercionBase

class InsertarCliente(InsercionBase):
    def ejecutar(self, session):
        nombre = input("Ingrese nombre: ")
        inicial = input("Ingrese inicial del segundo nombre (o deje vacío): ")
        apellido = input("Ingrese apellido: ")
        nombre_ciudad = input("Ingrese nombre de la ciudad: ")

        logging.info(f"Insertando cliente: {nombre} {inicial} {apellido}, Ciudad: {nombre_ciudad}")

        try:
            resultado = session.execute(
                text("SELECT CityID FROM cities WHERE CityName = :nombre_ciudad"),
                {'nombre_ciudad': nombre_ciudad}
            ).fetchone()

            if resultado is None:
                logging.warning(f"Ciudad no encontrada: {nombre_ciudad}")
                print(f"Error: ciudad '{nombre_ciudad}' no encontrada.")
                return

            city_id = resultado[0]
            direccion = input("Ingrese dirección: ")

            session.execute(text("SET @resultado = '';"))
            session.execute(
                text("CALL InsertCustomer(:nombre, :inicial, :apellido, :city_id, :direccion, @resultado);"),
                {
                    'nombre': nombre,
                    'inicial': inicial if inicial else None,
                    'apellido': apellido,
                    'city_id': city_id,
                    'direccion': direccion
                }
            )
            resultado = session.execute(text("SELECT @resultado;")).fetchone()[0]

            session.commit()
            logging.info(f"Cliente insertado: {nombre} {apellido}. Mensaje: {resultado}")
            print(resultado)

        except Exception as e:
            session.rollback()
            logging.error(f"Error al insertar cliente '{nombre} {apellido}': {e}", exc_info=True)
            print(f"Error al insertar cliente: {e}")
