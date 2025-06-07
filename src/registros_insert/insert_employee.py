import logging
from sqlalchemy import text
from .base import InsercionBase
from datetime import datetime

class InsertarEmpleado(InsercionBase):
    def ejecutar(self, session):
        nombre = input("Ingrese nombre: ")
        inicial = input("Ingrese inicial del segundo nombre (o deje vacío): ")
        apellido = input("Ingrese apellido: ")
        nacimiento_str = input("Ingrese fecha de nacimiento (YYYY-MM-DD): ")
        genero = input("Ingrese género (M/F): ")
        nombre_ciudad = input("Ingrese nombre de la ciudad: ")
        contrato_str = input("Ingrese fecha de contratación (YYYY-MM-DD): ")

        logging.info(f"Intentando insertar empleado: {nombre} {inicial} {apellido}, Ciudad: {nombre_ciudad}")

        try:
            nacimiento = datetime.strptime(nacimiento_str, "%Y-%m-%d")
            contrato = datetime.strptime(contrato_str, "%Y-%m-%d")
        except ValueError:
            logging.warning("Formato de fecha incorrecto")
            print("Error: formato de fecha incorrecto.")
            return

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

            session.execute(text("SET @resultado = '';"))
            session.execute(
                text("CALL InsertEmployee(:nombre, :inicial, :apellido, :nacimiento, :genero, :city_id, :contrato, @resultado);"),
                {
                    'nombre': nombre,
                    'inicial': inicial if inicial else None,
                    'apellido': apellido,
                    'nacimiento': nacimiento,
                    'genero': genero,
                    'city_id': city_id,
                    'contrato': contrato
                }
            )
            resultado = session.execute(text("SELECT @resultado;")).fetchone()[0]

            session.commit()
            logging.info(f"Empleado insertado: {nombre} {apellido}. Mensaje: {resultado}")
            print(resultado)

        except Exception as e:
            session.rollback()
            logging.error(f"Error al insertar empleado '{nombre} {apellido}': {e}", exc_info=True)
            print(f"Error al insertar empleado: {e}")
