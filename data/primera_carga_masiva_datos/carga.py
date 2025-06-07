import os
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from src.conexion.conexion_singleton import ConexionSingleton
from dotenv import load_dotenv
import logging
from src.loggin.loggin_config import configurar_logging


load_dotenv()
configurar_logging()
logger = logging.getLogger(__name__)

path = os.getenv("RUTA_BASE")

tablas = {
    "countries": "CountryID",
    "cities": "CityID",
    "categories": "CategoryID",
    "customers": "CustomerID",
    "employees": "EmployeeID",
    "products": "ProductID",
    "sales": "SalesID"
}

def cargar_datos_y_ajustar_autoincrement():
    conexion = ConexionSingleton()
    engine = conexion.engine
    try:
        with engine.connect() as conn:
            for tabla, columna_id in tablas.items():
                archivo_csv = os.path.join(path, f"{tabla}.csv")
                if not os.path.exists(archivo_csv):
                    logger.error(f"no se encontró el archivo: {archivo_csv}")
                    continue
                
                logger.info(f"cargando datos del archivo {archivo_csv} en la tabla {tabla}...")
                
                df = pd.read_csv(archivo_csv) # esto se deja en caso de que más adelante sea necesario relaizar limpieza de datos.
                
                df.to_sql(tabla, con=engine, if_exists='append', index=False)
                logger.info(f"datos cargados en {tabla}.")
                
                max_id_query = text(f"SELECT MAX({columna_id}) FROM {tabla}")
                max_id = conn.execute(max_id_query).scalar() or 0
                next_id = max_id + 1
                
                alter_query = text(f"ALTER TABLE {tabla} AUTO_INCREMENT = {next_id}")
                conn.execute(alter_query)
                logger.info(f"AUTO_INCREMENT de {tabla} seteado a {next_id}\n")
    except SQLAlchemyError as e:
        logger.error(f"Error durante la carga o ajuste: {e}")

if __name__ == "__main__":
    try:
        cargar_datos_y_ajustar_autoincrement()
    except Exception as e:
        logger.error(f"error en la carga, carga KO: {e}")
