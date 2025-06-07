import pandas as pd

class InformeProductoCiudad:
    def ejecutar(self, session):
        conn = session.connection().connection
        cursor = conn.cursor()
        cursor.callproc('informe_producto_ciudad_resumen')
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        df = pd.DataFrame(resultados, columns=columnas)
        return df.columns.tolist(), df.values.tolist()


class InformeTopClientes:
    def ejecutar(self, session):
        conn = session.connection().connection
        cursor = conn.cursor()
        cursor.callproc('informe_top_clientes')
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        df = pd.DataFrame(resultados, columns=columnas)
        return df.columns.tolist(), df.values.tolist()

class InformeVentasCategoria:
    def ejecutar(self, session):
        conn = session.connection().connection
        cursor = conn.cursor()
        cursor.callproc('informe_ventas_categoria')
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        df = pd.DataFrame(resultados, columns=columnas)
        return df.columns.tolist(), df.values.tolist()

class InformeVentas:
    def ejecutar(self, session):
        conn = session.connection().connection
        cursor = conn.cursor()
        cursor.callproc('informe_ventas')
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        df = pd.DataFrame(resultados, columns=columnas)
        return df.columns.tolist(), df.values.tolist()

class InformeFactory:
    @staticmethod
    def crear_informe(nombre: str):
        if nombre == "producto_ciudad":
            return InformeProductoCiudad()
        elif nombre == "top_clientes":
            return InformeTopClientes()
        elif nombre == "ventas_categoria":
            return InformeVentasCategoria()
        elif nombre == "ventas":
            return InformeVentas()
        else:
            return None