from functools import lru_cache
from src.conexion.conexion_singleton import ConexionSingleton
from src.modelos.modelos import Sale

conexion = ConexionSingleton()

@lru_cache(maxsize=1)  # tamaño máximo 1 porque son sólo 600 registros aprox
def cache_ventas():
    session = conexion.get_session()
    try:

        ventas = session.query(Sale.SalesID, Sale.CustomerID, Sale.Quantity, Sale.TotalPrice, Sale.SalesDate).all()
        return ventas
    finally:
        session.close()
