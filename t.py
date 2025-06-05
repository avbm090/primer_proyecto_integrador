from conexion.conexion_singleton import ConexionSingleton
from modelos.modelos import Base

if __name__ == "__main__":
    conexion = ConexionSingleton()
    Base.metadata.drop_all(conexion.engine)
    print("Todas las tablas fueron eliminadas.")
