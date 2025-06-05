import logging

def configurar_logging():
    logging.basicConfig(
        filename='log.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
