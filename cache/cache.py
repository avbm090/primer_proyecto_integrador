from functools import lru_cache
from conexion.conexion_singleton import ConexionSingleton
from modelos import Sale

conexion = ConexionSingleton()

@lru_cache(maxsize=1) #se pone 1 porque son solamente 600 registros iniciales, si crecieran los registros se modifica 
def cache_ventas():
    session = conexion.get_session()
    try:
        ventas = session.query(Sale).all()
        return ventas
    finally:
        session.close()
