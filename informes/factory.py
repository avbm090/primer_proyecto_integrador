class InformeProductoCiudad:
    def ejecutar(self, session):
        conn = session.connection().connection
        cursor = conn.cursor()
        cursor.callproc('informe_producto_ciudad_resumen')
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        return columnas, resultados

class InformeTopClientes:
    def ejecutar(self, session):
        conn = session.connection().connection
        cursor = conn.cursor()
        cursor.callproc('informe_top_clientes')
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        return columnas, resultados

class InformeVentasCategoria:
    def ejecutar(self, session):
        conn = session.connection().connection
        cursor = conn.cursor()
        cursor.callproc('informe_ventas_categoria')
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        return columnas, resultados

class InformeFactory:
    @staticmethod
    def crear_informe(nombre: str):
        if nombre == "producto_ciudad":
            return InformeProductoCiudad()
        elif nombre == "top_clientes":
            return InformeTopClientes()
        elif nombre == "ventas_categoria":
            return InformeVentasCategoria()
        else:
            return None
