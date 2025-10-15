#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""

"""
from config import settings
import requests
import json

class ApiBdPgsql:

    def __init__(self, logger):
        self.logger = logger
        self.BASE_URL = settings.API_PGSQL_URLBASE

    def insertar_datos_bulk(self, l_datos_formateados):
        """
        Le enviamos a apidatos
        """
        self.logger.debug("")

        payload = l_datos_formateados
        #self.logger.debug(f"payload={payload}")
        try:
            r = requests.post(f"{self.BASE_URL}/insertdatosbulk", json=payload, timeout=10 )
            d_rsp = {'status_code': r.status_code }

        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        #self.logger.debug(f"D_RSP={d_rsp}")
        return d_rsp
    
    def do_housekeeping(self):
        """
        Le enviamos a apidatos
        """
        self.logger.debug("")

        try:
            r = requests.get(f"{self.BASE_URL}/housekeeping", timeout=10 )
            d_rsp = {'status_code': r.status_code }

        except Exception as e: 
            self.logger.error( f"Error-> {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp