import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from src.loggin.loggin_config import configurar_logging  

load_dotenv()

configurar_logging()

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
            logging.info("iniciando conexión a la base de datos...")
            connection_string = f"mysql+pymysql://{user}:{password}@{host}:{puerto}/{db}?local_infile=1"
            try:
                cls._instance.engine = create_engine(connection_string, echo=True)
                with cls._instance.engine.connect() as conn:
                    logging.info("conexión base de datos OK.")
                cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            except SQLAlchemyError as e:
                logging.error(f"conexion a la base de datos KO: {e}")
                cls._instance = None
        return cls._instance

    def get_session(self):
        if self._instance is None:
            logging.error("se intentió obtener una session sin conexión válida.")
            raise Exception("no hay conexión disponible.")
        logging.info("sesión de base de datos OK.")
        return self.Session()
