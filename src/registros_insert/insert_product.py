import logging
from sqlalchemy import text
from .base import InsercionBase
from datetime import datetime

class InsertarProducto(InsercionBase):
    def ejecutar(self, session):
        nombre = input("Ingrese nombre del producto: ")
        precio_str = input("Ingrese precio: ")
        nombre_categoria = input("Ingrese nombre de la categoría: ")
        clase = input("Ingrese clase: ")
        modificar_str = input("Ingrese hora de modificación (HH:MM:SS): ")
        resistente = input("Ingrese tipo de resistencia: ")
        alergico = input("¿Es alergénico? (Sí/No): ")
        vitalidad_str = input("Ingrese días de vitalidad: ")

        logging.info(f"Intentando insertar producto: {nombre}, Categoría: {nombre_categoria}")

        try:
            precio = float(precio_str)
            modificar = datetime.strptime(modificar_str, "%H:%M:%S").time()
            vitalidad = int(vitalidad_str)
        except ValueError:
            logging.warning("Error de formato en precio, hora o días de vitalidad")
            print("Error en formato de número o fecha/hora.")
            return

        try:
            resultado = session.execute(
                text("SELECT CategoryID FROM categories WHERE CategoryName = :nombre_categoria"),
                {'nombre_categoria': nombre_categoria}
            ).fetchone()

            if resultado is None:
                logging.warning(f"Categoría no encontrada: {nombre_categoria}")
                print(f"Error: categoría '{nombre_categoria}' no encontrada.")
                return

            category_id = resultado[0]

            session.execute(text("SET @resultado = '';"))
            session.execute(
                text("CALL InsertProduct(:nombre, :precio, :category_id, :clase, :modificar, :resistente, :alergico, :vitalidad, @resultado);"),
                {
                    'nombre': nombre,
                    'precio': precio,
                    'category_id': category_id,
                    'clase': clase,
                    'modificar': modificar,
                    'resistente': resistente,
                    'alergico': alergico,
                    'vitalidad': vitalidad
                }
            )
            resultado = session.execute(text("SELECT @resultado;")).fetchone()[0]

            session.commit()
            logging.info(f"Producto insertado: {nombre}. Mensaje: {resultado}")
            print(resultado)

        except Exception as e:
            session.rollback()
            logging.error(f"Error al insertar producto '{nombre}': {e}", exc_info=True)
            print(f"Error al insertar producto: {e}")
