import os
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from conexion.conexion_singleton import ConexionSingleton


ruta_base = "C:/Users/Usuario/Desktop/H/proyecto/data"


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
                archivo_csv = os.path.join(ruta_base, f"{tabla}.csv")
                if not os.path.exists(archivo_csv):
                    print(f"no se encontró el archivo: {archivo_csv}")
                    continue
                
                print(f"cargando datos del archivo {archivo_csv} en la tabla {tabla}...")
                
                df = pd.read_csv(archivo_csv)
                
                df.to_sql(tabla, con=engine, if_exists='append', index=False)
                print(f"datos cargados en {tabla}.")
                
                max_id_query = text(f"SELECT MAX({columna_id}) FROM {tabla}")
                max_id = conn.execute(max_id_query).scalar() or 0
                next_id = max_id + 1
                
                alter_query = text(f"ALTER TABLE {tabla} AUTO_INCREMENT = {next_id}")
                conn.execute(alter_query)
                print(f"AUTO_INCREMENT de {tabla} seteado a {next_id}\n")
    except SQLAlchemyError as e:
        print(f"Error durante la carga o ajuste: {e}")

if __name__ == "__main__":
    cargar_datos_y_ajustar_autoincrement()
