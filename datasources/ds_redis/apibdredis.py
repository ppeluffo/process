#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""

"""

import redis
from config import settings

class ApiBdRedis:

    def __init__(self, logger):
        self.logger = logger
        self.rh = redis.Redis( settings.BDREDIS_HOST, settings.BDREDIS_PORT,settings.BDREDIS_DB, socket_connect_timeout=1)

    def pop_rxlines(self):
        """
        Si la lista no existe, redis devuelve un None.
        Si la lista existe y está vacia, devuelve None.
        """

        try:
            l_pk_datastruct = self.rh.lpop('RXDATA_QUEUE', settings.MAX_DEQUEUE_FRAMES)
            #self.logger.debug(f"l_pk_datastruct={l_pk_datastruct}")
            if l_pk_datastruct is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = { 'status_code': 200, 'l_pk_datastruct': l_pk_datastruct }

        except Exception as e:
            #self.logger.debug( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        #self.logger.debug(f"d_rsp={d_rsp}")
        return d_rsp