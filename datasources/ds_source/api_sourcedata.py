#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""

"""

from config import settings
import requests


class ApiSourceData:

    def __init__(self, logger):
        self.logger = logger
        self.BASE_URL = settings.API_REDIS_URLBASE

    def leer_datos_encolados(self):
        """
        Le pedimos a la apiredis los datos que hay encolados en RXDATA_QUEUE
        """
        self.logger.debug("")
        
        try:
            params = {'count': settings.MAX_DEQUEUE_FRAMES }
            r = requests.get(f"{self.BASE_URL}/dequeuerxlines", params=params, timeout=10 )
            d_rsp = {'status_code': r.status_code }

        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        
        if r.status_code == 200:
            # Cada elemento es del tipo: {'TYPE':args['type'], 'ID':args['unit'], 'D_LINE':d_params}.
            payload = r.json()
            l_datastruct = payload.get('l_datastruct',[])
            d_rsp = {'status_code': 200,  'l_datastruct':l_datastruct }

        #self.logger.debug(f"DEBUG: D_RSP={d_rsp}")
        #self.logger.debug(f"DEBUG: {type(d_rsp)}")
        return d_rsp
    
