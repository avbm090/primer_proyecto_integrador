from .insert_category import InsertarCategoria
from .insert_countries import InsertarPais
from .insert_cities import InsertarCiudad
from .insert_customers import InsertarCliente
from .insert_employee import InsertarEmpleado
from .insert_product import InsertarProducto
from .insert_sales import InsertarVenta

class InsercionFactory:
    @staticmethod
    def crear_insercion(tabla):
        tabla = tabla.lower()
        if tabla == 'category':
            return InsertarCategoria()
        elif tabla == 'country':
            return InsertarPais()
        elif tabla == 'city':
            return InsertarCiudad()
        elif tabla == 'customer':
            return InsertarCliente()
        elif tabla == 'employee':
            return InsertarEmpleado()
        elif tabla == 'product':
            return InsertarProducto()
        elif tabla == 'sale':
            return InsertarVenta()
        else:
            return None
