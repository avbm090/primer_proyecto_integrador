from src.conexion.conexion_singleton import ConexionSingleton
from src.registros_insert.factory import InsercionFactory
from sql.consultas_sql import ejecutar_consulta
from src.informes.factory import InformeFactory
from src.loggin.loggin_config import configurar_logging
import logging

def main():
    configurar_logging()
    logging.info("Inicio del programa")

    conexion = ConexionSingleton()

    while True:
        print("\nOpciones:")
        print("1: insertar datos")
        print("2: ejecutar código SQL / llamar procedimientos")
        print("3: ejecutar informes predefinidos")
        print("4: informe ventas")
        print("5: salir")
        opcion = input("elige opción (1-5): ").strip()
        logging.info(f"opción elegida: {opcion}")

        if opcion == "1":
            tabla = input(
                "ingresar nombre de la tabla donde se va a insertar "
                "(Category, Country, City, Customer, Employee, Product, Sale): "
            ).strip().capitalize()
            logging.info(f"intento de insert en tabla: {tabla}")
            insercion = InsercionFactory.crear_insercion(tabla)
            if insercion:
                session = conexion.get_session()
                try:
                    insercion.ejecutar(session)
                    session.commit()
                    logging.info(f"insert OK {tabla}")
                except Exception as e:
                    session.rollback()
                    logging.error(f"error al hacer insert en tabla {tabla}: {e}", exc_info=True)
                    print(f"error en hacer insert: {e}")
                finally:
                    session.close()
            else:
                logging.warning(f"tabla no válida para insert: {tabla}")
                print("tabla no válida.")

        elif opcion == "2":
            session = conexion.get_session()
            try:
                logging.info("ejecutando consulta SQL / procedure almacenado")
                ejecutar_consulta(session)
                session.commit()
                logging.info("consulta SQL ejecutada con éxito")
            except Exception as e:
                session.rollback()
                if "doesn't exist" in str(e):
                    print("error: la tabla especificada no está en la base de datos.")
                else:
                    print(f"error al ejecutar consulta: {e}")
                logging.error(f"error al ejecutar consulta SQL: {e}", exc_info=True)
            finally:
                session.close()

        elif opcion == "3":
            print("\nInformes cargados:")
            print("1) informe Producto Ciudad")
            print("2) informe Top Clientes")
            print("3) informe Ventas por Categoría")
            informe_opcion = input("Elige informe (1-3): ").strip()
            logging.info(f"Informe seleccionado: {informe_opcion}")

            nombres_informes = {
                "1": "producto_ciudad",
                "2": "top_clientes",
                "3": "ventas_categoria"
            }

            nombre_informe = nombres_informes.get(informe_opcion)
            if not nombre_informe:
                logging.warning(f"opción de informe inválida: {informe_opcion}")
                print("informe no existe.")
                continue

            informe = InformeFactory.crear_informe(nombre_informe)
            if informe:
                session = conexion.get_session()
                try:
                    columnas, resultados = informe.ejecutar(session)
                    logging.info(f"informe {nombre_informe} ejecutado")
                    if resultados:
                        print("\t".join(columnas))
                        for fila in resultados:
                            print("\t".join(str(x) for x in fila))
                    else:
                        logging.info(f"no se encontraron resultados para el informe {nombre_informe}")
                        print("no se encontraron resultados para este informe.")
                except Exception as e:
                    logging.error(f"error al ejecutar informe {nombre_informe}: {e}", exc_info=True)
                    print(f"error al ejecutar informe: {e}")
                finally:
                    session.close()
            else:
                logging.warning(f"informe no encontrado: {nombre_informe}")
                print("informe no encontrado.")

        elif opcion == "4":
            nombre_informe = "ventas"
            informe = InformeFactory.crear_informe(nombre_informe)
            if informe:
                session = conexion.get_session()
                try:
                    columnas, resultados = informe.ejecutar(session)
                    logging.info(f"informe {nombre_informe} ejecutado OK")
                    if resultados:
                        print("\t".join(columnas))
                        for fila in resultados:
                            print("\t".join(str(x) for x in fila))
                    else:
                        logging.info(f"no se encontraron resultados para el informe {nombre_informe}")
                        print("no se encontraron resultados para este informe.")
                except Exception as e:
                    logging.error(f"error al ejecutar informe {nombre_informe}: {e}", exc_info=True)
                    print(f"error al ejecutar informe: {e}")
                finally:
                    session.close()
            else:
                logging.warning(f"informe no encontrado: {nombre_informe}")
                print("informe no encontrado.")

        elif opcion == "5":
            logging.info("programa cerrado")
            print("cerrado.")
            break

        else:
            logging.warning(f"opción inválida ingresada: {opcion}")
            print("opción inválida.")

if __name__ == "__main__":
    main()
