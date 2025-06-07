import pandas as pd
import json
import os
from datetime import datetime
import logging
from src.loggin import loggin_config
from cache.cache import cache_ventas 

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
            logger.error(f"Error al ejecutar el procedimiento {procedimiento}: {e}")
            raise

    def guardar_json(self, df, procedimiento):
        try:
            folder_path = 'informes_resultado'
            if not os.path.exists(folder_path):
                try:
                    os.makedirs(folder_path)
                except Exception as e:
                    logger.error(f"Error al crear la carpeta {folder_path}: {e}")
                    raise

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'informes_resultado/{procedimiento}_{timestamp}.json'

            records = df.to_dict(orient='records')
            json_data = json.dumps(records, default=str, indent=4)

            with open(file_name, 'w') as json_file:
                json.dump(json.loads(json_data), json_file, indent=4)

            logger.info(f"Informe JSON guardado en: {file_name}")

        except Exception as e:
            logger.error(f"Error al guardar el archivo JSON para {procedimiento}: {e}")
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


class InformeVentas(Informe):
    def ejecutar(self, session):
        # caché
        ventas = cache_ventas()
        if ventas:
            logger.info("Usando datos de ventas desde el caché.")
            columnas = ["SalesID", "CustomerID", "Quantity", "TotalPrice", "SalesDate"]
            return columnas, [(venta[0], venta[1], venta[2], venta[3], venta[4]) for venta in ventas]
        else:
            logger.info("no se encontraron ventas en caché, consultando la base de datos.")
            return super().ejecutar(session, 'informe_ventas')


class InformeFactory:
    @staticmethod
    def crear_informe(nombre: str):
        if nombre == "producto_ciudad":
            return InformeProductoCiudad()
        elif nombre == "top_clientes":
            return InformeTopClientes()
        elif nombre == "ventas_categoria":
            return InformeVentasCategoria()
        elif nombre == "ventas":
            return InformeVentas()
        else:
            return None
