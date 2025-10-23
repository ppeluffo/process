#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Cada 60 segundos se conecta como cliente de la apidatos y lee los datos
generados en la BD online del servidor de comunicaciones y los recrea en 
una base local.
Para conectarse a la redis y a la PSQL usa las correspondientes APIs

"""

import sys
import time
import schedule
import signal

from config import settings

from container import Container

def clt_C_handler(signum, frame):
    sys.exit(0)

logger = Container.logger()
    
def main_task():
    """
    Esta tarea se encarga de leer los datos de la base remota
    e insertarlos en la base local.
    Luego borra todos los registros con mas de 72 hs
    """

    t1_start = time.time()
 
    # Desencolo datos de la Redis.
    # Cada elemento es del tipo: {'TYPE':args['type'], 'ID':args['unit'], 'D_LINE':d_params}.
    # Tengo una lista de diccionarios
    t2_start = time.time()
    l_datastruct = container.datos_service().pop_rxlines()
    t2_end = time.time()
    elapsed_t2 = (t2_end - t2_start) * 1000
    #logger.info(f"dtime: pop_rxlines={elapsed_t2}")

    if len(l_datastruct) > 0:

        # Formateamos los datos para que puedan insertarse en modo bulk
        t3_start = time.time()
        l_datos_formateados = container.datos_service().formatear_lista_datos(l_datastruct)
        logger.debug(f"l_datos_formateados={l_datos_formateados}")
        t3_end = time.time()
        elapsed_t3 = (t3_end - t3_start) * 1000
        #logger.info(f"dtime: formatear_lista_datos={elapsed_t3}")
    
        # Envio los datos para que se inserten bulk
        t4_start = time.time()
        container.datos_service().insertar_datos_bulk(l_datos_formateados)
        t4_end = time.time()
        elapsed_t4 = (t4_end - t4_start) * 1000
        #logger.info(f"dtime: insertar_datos_bulk={elapsed_t4}")

        # Mantenemos la tabla online acotada
        #container.datos_service().do_housekeeping()

    else:
        l_datos_formateados = []
        elapsed_t3 = 0
        elapsed_t4 = 0
        
    t1_end = time.time()
    elapsed_t1 = (t1_end - t1_start) * 1000
    logger.info(f"Procesando: {len(l_datastruct)} frames, {len(l_datos_formateados)} rcds. en {elapsed_t1:.2f} msecs.")
    logger.info(f"            T_redis={elapsed_t2:.2f} ms, T_process={elapsed_t3:.2f} ms, T_pgsql={elapsed_t4:.2f} ms.")


if __name__ == '__main__':

    signal.signal(signal.SIGINT, clt_C_handler)

    sleep_time = settings.SLEEP_TIME

    logger.info(f" Starting...")
    logger.info(f" SLEEP_TIME={sleep_time}")

    # Creo todas las dependencias
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    
    # Programar tarea cada SLEEP_TIME segundos
    schedule.every(sleep_time).seconds.do(main_task)

    while True:
        schedule.run_pending()
        #
        time.sleep(1)
        #
