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

    start = time.time()
 
    # Desencolo datos de la Redis.
    # Cada elemento es del tipo: {'TYPE':args['type'], 'ID':args['unit'], 'D_LINE':d_params}.
    # Tengo una lista de diccionarios
    l_datastruct = container.datos_service().leer_datos_encolados()
    
    if len(l_datastruct) > 0:

        # Formateamos los datos para que puedan insertarse en modo bulk
        l_datos_formateados = container.datos_service().formatear_lista_datos(l_datastruct)
        #print(f"l_datos_formateados={l_datos_formateados}")
    
        # Envio los datos para que se inserten bulk
        container.datos_service().insertar_datos_bulk(l_datos_formateados)
        
        # Mantenemos la tabla online acotada
        #container.datos_service().do_housekeeping()

    else:
        l_datos_formateados = []
        
    end = time.time()
    elapsed_time = (end - start) * 1000
    logger.info(f"Procesando {len(l_datastruct)} frames, {len(l_datos_formateados)} rcds. en {elapsed_time:.2f} msecs.")
    #print(f"INFO,{__name__}:Procesando {len(l_datastruct)} frames, {len(l_datos_formateados)} rcds. en {elapsed_time:.2f} msecs.")


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
