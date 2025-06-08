import pytest
from unittest.mock import MagicMock, patch
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from cache.cache import cache_ventas
from src.conexion.conexion_singleton import ConexionSingleton

@pytest.fixture
def mock_session():

    mock_session = MagicMock() #se mockea la sesion
   #se configura lo que debería mostrar
    mock_session.query.return_value.all.return_value = [
        (1, 101, 2, 20.0, '2025-06-07'),
        (2, 102, 1, 10.0, '2025-06-07')
    ]
    return mock_session

@patch.object(ConexionSingleton, 'get_session') #se va a usar un mock de get_session de la conexión singleton
def test_cache_ventas(mock_get_session, mock_session): # el primer argumento es get_session mockeado

    mock_get_session.return_value = mock_session # cuando se invoque el método get_session, devolverá el mock_session

    ventas = cache_ventas()


    assert len(ventas) == 2  
    assert ventas[0] == (1, 101, 2, 20.0, '2025-06-07')  
    assert ventas[1] == (2, 102, 1, 10.0, '2025-06-07') 

    mock_session.query.return_value.all.assert_called_once()


@patch.object(ConexionSingleton, 'get_session')
def test_cache_ventas(mock_get_session, mock_session):
    mock_get_session.return_value = mock_session

    # primera llamada a cache_ventas, debería ir a la bbdd
    ventas_1 = cache_ventas()

    # la segunda llamada al caché debería devolver lo del caché
    ventas_2 = cache_ventas()

    # se corrobora si devuelven lo mismo
    assert ventas_1 == ventas_2

    # se corrobora que la bbdd fue consultada sólamente una vez
    mock_session.query.return_value.all.assert_called_once()
