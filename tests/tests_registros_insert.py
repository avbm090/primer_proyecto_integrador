import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from loggin.loggin_config import configurar_logging

load_dotenv()

configurar_logging()

# se crea una conexión singleton aunque ya existe una 
class ConexionSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASS")
            host = os.getenv("DB_HOST")
            db = os.getenv("DB_NAME")
            puerto = os.getenv("DB_PORT")
            

            if not all([user, password, host, db, puerto]):
                logging.error("Faltan algunas variables de entorno para la conexión.")
                raise ValueError("Faltan variables de entorno necesarias.")
            
            logging.info("Iniciando conexión a la base de datos...")

            connection_string = f"mysql+pymysql://{user}:{password}@{host}:{puerto}/{db}?local_infile=1"
            try:
                cls._instance.engine = create_engine(connection_string, echo=True)

                cls._instance.engine.connect() 
                logging.info("Conexión a la base de datos OK.")
                cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            except SQLAlchemyError as e:
                logging.error(f"Error en la conexión a la base de datos: {e}")
                cls._instance = None
        return cls._instance

    def get_session(self):
        if self._instance is None:
            logging.error("Se intentó obtener una sesión sin una conexión válida.")
            raise Exception("No hay conexión disponible.")
        logging.info("Sesión de base de datos OK.")
        return self.Session()


def insertar_datos(tabla, **datos):

    conexion = ConexionSingleton()
    session = conexion.get_session()
    
    try:
        # Crear la query de inserción
        columns = ', '.join(datos.keys())
        values = ', '.join([f"'{v}'" for v in datos.values()])
        query = f"INSERT INTO {tabla} ({columns}) VALUES ({values})"
        
        # Ejecutar la query
        session.execute(text(query))
        session.commit()
        logging.info(f"Datos insertados en la tabla {tabla}")
    except Exception as e:
        session.rollback()
        logging.error(f"Error al insertar datos en {tabla}: {e}", exc_info=True)
        print(f"Error al insertar datos en {tabla}: {e}")
    finally:

        session.close()


#  InsertarCategoria
def test_insertar_categoria():
    datos = {'CategoryName': 'Electronics'}
    tabla = 'categories'
    insertar_datos(tabla, **datos)

    conexion = ConexionSingleton()
    session = conexion.get_session()
    result = session.execute(text("SELECT * FROM categories WHERE CategoryName = :nombre"), {'nombre': datos['CategoryName']}).fetchone()
    
    session.close()
    
    assert result is not None, f"Category '{datos['CategoryName']}' no fue insertada correctamente."


# InsertarCiudad
def test_insertar_ciudad():
    datos = {'CityName': 'New York', 'Zipcode': '10001', 'CountryID': 1}
    tabla = 'cities'
    insertar_datos(tabla, **datos)

    conexion = ConexionSingleton()
    session = conexion.get_session()
    result = session.execute(text("SELECT * FROM cities WHERE CityName = :nombre_ciudad"), {'nombre_ciudad': datos['CityName']}).fetchone()
    session.close()
    
    assert result is not None, f"City '{datos['CityName']}' no fue insertada correctamente."


# InsertarPais
def test_insertar_pais():
    datos = {'CountryName': 'Mexico', 'CountryCode': 'MX'}
    tabla = 'countries'
    insertar_datos(tabla, **datos)

    conexion = ConexionSingleton()
    session = conexion.get_session()
    result = session.execute(text("SELECT * FROM countries WHERE CountryName = :nombre"), {'nombre': datos['CountryName']}).fetchone()
    session.close()
    
    assert result is not None, f"Country '{datos['CountryName']}' no fue insertada correctamente."


# InsertarProducto
def test_insertar_producto():
    datos = {'ProductName': 'Laptop', 'Price': 1000.0, 'CategoryID': 1}
    tabla = 'products'
    insertar_datos(tabla, **datos)

    conexion = ConexionSingleton()
    session = conexion.get_session()
    result = session.execute(text("SELECT * FROM products WHERE ProductName = :nombre"), {'nombre': datos['ProductName']}).fetchone()
    session.close()

    assert result is not None, f"Product '{datos['ProductName']}' no fue insertado correctamente."


# InsertarEmpleado
def test_insertar_empleado():
    datos = {'FirstName': 'John', 'MiddleInitial': 'D', 'LastName': 'Doe', 'BirthDate': '1990-01-01', 'Gender': 'M', 'CityID': 1, 'HireDate': '2025-06-07'}
    tabla = 'employees'
    insertar_datos(tabla, **datos)

    conexion = ConexionSingleton()
    session = conexion.get_session()
    result = session.execute(text("SELECT * FROM employees WHERE FirstName = :nombre"), {'nombre': datos['FirstName']}).fetchone()
    session.close()

    assert result is not None, f"Employee '{datos['FirstName']}' no fue insertado correctamente."


# InsertarCliente
def test_insertar_cliente():
    datos = {'FirstName': 'Alice', 'MiddleInitial': 'S', 'LastName': 'Smith', 'CityID': 1, 'Address': '123 Main St'}
    tabla = 'customers'
    insertar_datos(tabla, **datos)

    conexion = ConexionSingleton()
    session = conexion.get_session()
    result = session.execute(text("SELECT * FROM customers WHERE FirstName = :nombre"), {'nombre': datos['FirstName']}).fetchone()
    session.close()

    assert result is not None, f"Customer '{datos['FirstName']}' no fue insertado correctamente."


# InsertarVenta
def test_insertar_venta():
    datos = {'SalesPersonID': 1, 'CustomerID': 1, 'ProductID': 1, 'Quantity': 2, 'Discount': 0.1, 'TotalPrice': 1800.0, 'SalesDate': '12:00:00', 'TransactionNumber': 'TX123'}
    tabla = 'sales'
    insertar_datos(tabla, **datos)

    conexion = ConexionSingleton()
    session = conexion.get_session()
    result = session.execute(text("SELECT * FROM sales WHERE TransactionNumber = :txn"), {'txn': datos['TransactionNumber']}).fetchone()
    session.close()

    assert result is not None, f"venta con transacción '{datos['TransactionNumber']}' no fue insertada correctamente."

