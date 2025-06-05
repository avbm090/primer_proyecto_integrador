import logging
from sqlalchemy import text
from .base import InsercionBase
from datetime import datetime

class InsertarVenta(InsercionBase):
    def ejecutar(self, session):
        nombre_vendedor = input("nombre del vendedor: ")
        nombre_cliente = input("nombre del cliente: ")
        nombre_producto = input("nombre del producto: ")

        logging.info(f"Intentando insertar venta - Vendedor: {nombre_vendedor}, Cliente: {nombre_cliente}, Producto: {nombre_producto}")

        while True:
            cantidad_str = input("cantidad: ")
            try:
                cantidad = int(cantidad_str)
                if cantidad < 0:
                    print("La cantidad debe ser un número positivo.")
                    continue
                break
            except ValueError:
                logging.warning("Cantidad inválida ingresada.")
                print("Error: la cantidad debe ser un número entero.")

        while True:
            descuento_str = input("descuento (por ejemplo 0.10 para 10%, dejar vacío para 0): ").strip()
            if descuento_str == "":
                descuento = 0.0
                break
            try:
                descuento = float(descuento_str)
                if not (0 <= descuento <= 1):
                    print("El descuento debe ser un número entre 0 y 1.")
                    continue
                break
            except ValueError:
                logging.warning("Descuento inválido ingresado.")
                print("Error: el descuento debe ser un número decimal.")

        while True:
            total_str = input("precio total: ")
            try:
                total = float(total_str)
                if total < 0:
                    print("El precio total debe ser un número positivo.")
                    continue
                break
            except ValueError:
                logging.warning("Precio total inválido ingresado.")
                print("Error: el precio total debe ser un número decimal.")

        while True:
            fecha_str = input("hora de venta (HH:MM:SS): ")
            try:
                fecha = datetime.strptime(fecha_str, "%H:%M:%S").time()
                break
            except ValueError:
                logging.warning("Hora de venta con formato incorrecto.")
                print("Error: formato incorrecto en hora (debe ser HH:MM:SS).")

        transaccion = input("número de transacción: ")

        try:
            session.execute(text("SET @resultado = '';"))
            session.execute(
                text("""CALL InsertSale(
                            :nombre_vendedor, :nombre_cliente, :nombre_producto,
                            :cantidad, :descuento, :total, :fecha, :transaccion, @resultado
                    );"""),
                {
                    'nombre_vendedor': nombre_vendedor,
                    'nombre_cliente': nombre_cliente,
                    'nombre_producto': nombre_producto,
                    'cantidad': cantidad,
                    'descuento': descuento,
                    'total': total,
                    'fecha': fecha,
                    'transaccion': transaccion
                }
            )
            resultado = session.execute(text("SELECT @resultado;")).fetchone()[0]
            session.commit()
            logging.info(f"Venta insertada exitosamente. Resultado: {resultado}")
            print(resultado)

        except Exception as e:
            session.rollback()
            logging.error(f"Error al insertar venta: {e}", exc_info=True)
            print(f"Error al insertar venta: {e}")
