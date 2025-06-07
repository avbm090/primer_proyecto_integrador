from src.loggin.loggin_config import configurar_logging
from sqlalchemy import text
import logging

configurar_logging()

class ConsultaStrategy:
    def ejecutar(self, session, consulta):
        raise NotImplementedError()

class ConsultaSelect(ConsultaStrategy):
    def ejecutar(self, session, consulta):
        logging.info(f"ejecutando consulta SELECT: {consulta}")  
        resultado = session.execute(text(consulta))
        filas = resultado.fetchall()
        if filas:
            for fila in filas:
                print(fila)
        else:
            logging.info("no se encontraron resultados.")  
            print("no se encontraron resultados.")

class ConsultaCallProcedure(ConsultaStrategy):
    def ejecutar(self, session, consulta):
        logging.info(f"ejecutando procedure: {consulta}")  
        session.execute(text(consulta))  
        print("procedure ejecutado OK.")

class ConsultaDefault(ConsultaStrategy):
    def ejecutar(self, session, consulta):
        logging.warning(f"tipo de query no permitida: {consulta}") 
        print("error: sólo se permiten consultas SELECT o CALL para procedures.")
        raise ValueError("1uery no permitida. Solo SELECT o CALL son válidas.")

def elegir_strategy(consulta):
    consulta_lc = consulta.strip().lower()
    if consulta_lc.startswith("select"):
        logging.info("estrategia: SELECT")
        return ConsultaSelect()
    elif consulta_lc.startswith("call"):
        logging.info("estrategia: CALL PROCEDURE")
        return ConsultaCallProcedure()
    else:
        logging.info("estrategia: DEFAULT")
        return ConsultaDefault()

def ejecutar_consulta(session):
    consulta = input("SQL> ").strip()
    if not consulta:
        logging.warning("consulta vacía.") 
        print("consulta vacía.")
        return

    strategy = elegir_strategy(consulta)
    try:
        strategy.ejecutar(session, consulta)
        logging.info("consulta ejecutada.")
    except Exception as e:
        session.rollback() 
        logging.error(f"error al ejecutar query: {e}")  
        print(f"error al ejecutar query: {e}")
