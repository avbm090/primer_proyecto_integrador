import pandas as pd
import json
import os
from datetime import datetime
import logging
from src.loggin import loggin_config
from cache.cache import cache_ventas 
from sqlalchemy import text 

loggin_config.configurar_logging()
logger = logging.getLogger()

class Informe:
    def ejecutar(self, session, procedimiento: str):
        try:
            conn = session.connection().connection
            cursor = conn.cursor()
            cursor.callproc(procedimiento)
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            cursor.close()

            df = pd.DataFrame(resultados, columns=columnas)

            logger.info(f"Resultados de {procedimiento}:")
            logger.info(df)

            self.guardar_json(df, procedimiento)

            return df.columns.tolist(), df.values.tolist()

        except Exception as e:
            logger.error(f"error al ejecutar el procedimiento {procedimiento}: {e}")
            raise

    def guardar_json(self, df, procedimiento):
        try:
            folder_path = 'src/informes_resultado'

            os.makedirs(folder_path, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'{folder_path}/{procedimiento}_{timestamp}.json'

            records = df.to_dict(orient='records')
            json_data = json.dumps(records, default=str, indent=4)

            with open(file_name, 'w') as json_file:
                json.dump(json.loads(json_data), json_file, indent=4)

            logger.info(f"informe JSON guardado en: {file_name}")

        except Exception as e:
            logger.error(f"error al guardar el archivo JSON para {procedimiento}: {e}")
            raise


class InformeProductoCiudad(Informe):
    def ejecutar(self, session):
        return super().ejecutar(session, 'informe_producto_ciudad_resumen')


class InformeTopClientes(Informe):
    def ejecutar(self, session):
        return super().ejecutar(session, 'informe_top_clientes')


class InformeVentasCategoria(Informe):
    def ejecutar(self, session):
        return super().ejecutar(session, 'informe_ventas_categoria')


class InformeVentasHistorico(Informe):
    def ejecutar(self, session):
        ventas = cache_ventas()
        if ventas:
            logger.info("Usando datos de ventas desde el caché.")
            columnas = ["SalesID", "CustomerID", "Quantity", "TotalPrice", "SalesDate"]

            df = pd.DataFrame(ventas, columns=columnas)
            self.guardar_json(df, 'informe_ventas_historico')
            return columnas, [(venta[0], venta[1], venta[2], venta[3], venta[4]) for venta in ventas]
        else:
            logger.info("No se encontraron ventas en caché, consultando la base de datos.")
            return super().ejecutar(session, 'informe_ventas_historico')


class InformeVentas(Informe):
    def ejecutar(self, session):
        query = """
            SELECT SalesID, SalesPersonID, CustomerID, ProductID, Quantity, Discount, TotalPrice, SalesDate, TransactionNumber
            FROM sales_log
        """
        resultado = session.execute(text(query))
        columnas = resultado.keys()
        filas = resultado.fetchall()

        df = pd.DataFrame(filas, columns=columnas)
        self.guardar_json(df, 'informe_ventas_auditoria')

        return columnas, filas


class InformeFactory:

    informes = {
        "producto_ciudad": InformeProductoCiudad,
        "top_clientes": InformeTopClientes,
        "ventas_categoria": InformeVentasCategoria,
        "ventas": InformeVentas,
        "ventas_historico": InformeVentasHistorico
    }

    @staticmethod
    def crear_informe(nombre: str):

        informe_clase = InformeFactory.informes.get(nombre, None)
        if informe_clase:
            return informe_clase()
        return None
