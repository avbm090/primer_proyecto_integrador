from sqlalchemy import text
import logging
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConsultaStrategy:
    def ejecutar(self, session, consulta):
        raise NotImplementedError()

class ConsultaSelect(ConsultaStrategy):
    def ejecutar(self, session, consulta):
        resultado = session.execute(text(consulta))
        filas = resultado.fetchall()
        if filas:
            for fila in filas:
                print(fila)
        else:
            print("No se encontraron resultados.")

class ConsultaInsertUpdateDelete(ConsultaStrategy):
    def ejecutar(self, session, consulta):
        session.execute(text(consulta))
        session.commit()
        print("Consulta ejecutada correctamente.")

class ConsultaCallProcedure(ConsultaStrategy):
    def ejecutar(self, session, consulta):
        session.execute(text(consulta))
        session.commit()
        print("Procedimiento almacenado ejecutado correctamente.")

class ConsultaDefault(ConsultaStrategy):
    def ejecutar(self, session, consulta):
        session.execute(text(consulta))
        session.commit()
        print("Consulta ejecutada correctamente.")

def elegir_strategy(consulta):
    consulta_lc = consulta.strip().lower()
    if consulta_lc.startswith("select"):
        logging.info("Estrategia: SELECT")
        return ConsultaSelect()
    elif consulta_lc.startswith(("insert", "update", "delete")):
        logging.info("Estrategia: INSERT/UPDATE/DELETE")
        return ConsultaInsertUpdateDelete()
    elif consulta_lc.startswith("call"):
        logging.info("Estrategia: CALL PROCEDURE")
        return ConsultaCallProcedure()
    else:
        logging.info("Estrategia: DEFAULT")
        return ConsultaDefault()

def ejecutar_consulta(session):
    consulta = input("SQL> ").strip()
    if not consulta:
        print("Consulta vacía.")
        return

    strategy = elegir_strategy(consulta)
    try:
        strategy.ejecutar(session, consulta)
    except Exception as e:
        session.rollback()
        print(f"Error al ejecutar consulta: {e}")
