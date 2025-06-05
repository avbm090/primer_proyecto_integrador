import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv


load_dotenv() 

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
            
            connection_string = f"mysql+pymysql://{user}:{password}@{host}:{puerto}/{db}?local_infile=1"

            try:
                cls._instance.engine = create_engine(connection_string, echo=True)
                with cls._instance.engine.connect() as conn:
                    print("conexión ok.")
                cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            except SQLAlchemyError as e:
                print(f"error al conectar: {e}")
                cls._instance = None  
        return cls._instance

    def get_session(self):
        if self._instance is None:
            raise Exception("no hay conexión disponible")
        return self.Session()
