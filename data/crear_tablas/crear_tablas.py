from conexion.conexion_singleton import ConexionSingleton
from modelos.modelos import Base

if __name__ == "__main__":
    conexion = ConexionSingleton()
    Base.metadata.create_all(conexion.engine)
    print("tablas creadas OK.")
