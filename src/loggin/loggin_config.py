import os
import logging

def configurar_logging():
    log_file = os.path.join('src', 'loggin', 'loggin_config.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
