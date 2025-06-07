from src.conexion.conexion_singleton import ConexionSingleton
from src.modelos.modelos import Base
import logging
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    try:
        conexion = ConexionSingleton()
        Base.metadata.create_all(conexion.engine)
        
        logging.info("tablas creadas OK.")
    except SQLAlchemyError as e:
        logging.error(f"error tablas no creadas: {e}")
