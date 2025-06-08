import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.conexion.conexion_singleton import ConexionSingleton
from src.modelos.modelos import Base
from sqlalchemy.exc import SQLAlchemyError

# mock de la conexión a la base de datos
@pytest.fixture
def mock_conexion():
    mock_conexion = MagicMock()
    mock_conexion.engine = MagicMock()
    return mock_conexion

# test cuando todo sale bien
@patch('src.modelos.modelos.Base.metadata.create_all')  # se mockeala función que crea las tablas
def test_creacion_tablas_exitosa(mock_create_all, mock_conexion):
    # se supone que la creacion de la tabla no da error
    mock_create_all.return_value = None

    # se verifica que la tablas hayan sido creadas
    conexion = ConexionSingleton()
    Base.metadata.create_all(conexion.engine)

    # se verifica que 'create_all' fue llamado con el engine de la conexión mock
    mock_create_all.assert_called_once_with(mock_conexion.engine)

# test cuando algo sale mal (se simula un error en la creación de las tablas)
@patch('src.modelos.modelos.Base.metadata.create_all', side_effect=SQLAlchemyError("Error en la base de datos"))
def test_error_creacion_tablas(mock_create_all, mock_conexion):
    # se simula error en la creación de las tablas
    try:
        conexion = ConexionSingleton()
        Base.metadata.create_all(conexion.engine)
    except SQLAlchemyError as e:
        # si hay error se pasa el test
        pass

    # se corrobora que el create_all haya sido llamado
    mock_create_all.assert_called_once_with(mock_conexion.engine)
