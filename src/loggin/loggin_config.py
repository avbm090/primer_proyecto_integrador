import os
import logging

def configurar_logging():
    # Crear carpeta "logs" en la raíz del proyecto
    log_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))
    os.makedirs(log_folder, exist_ok=True)

    # Ruta del archivo de log
    log_file = os.path.join(log_folder, 'app.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
