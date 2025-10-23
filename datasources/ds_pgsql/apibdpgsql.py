#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""

"""
from .models import Usuarios, Configuraciones, Online, RecoverId, Historica
from sqlalchemy import text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import insert

from datetime import datetime, timedelta

from config import settings

class ApiBdPgsql:

    def __init__(self, session_factory, logger):
        self.session_factory = session_factory
        self.logger = logger
  
    def insertar_datos_bulk_historica(self, l_datos_bulk=None):
        """
        l_datos_bulk es una lista de tuplas (sfechadata, sfechasys, id, key, value)
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                session.bulk_insert_mappings(Historica, l_datos_bulk)
                session.commit()
                d_rsp = { 'status_code': 200}        

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp 
    
    def insertar_datos_bulk_online(self, l_datos_bulk=None):
        """
        l_datos_bulk es una lista de tuplas (sfechadata, sfechasys, id, key, value)
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                session.bulk_insert_mappings(Online, l_datos_bulk)
                session.commit()
                d_rsp = { 'status_code': 200}        

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp   
    
    def achicar_tb_online(self, min_ptr=None):
        """
        Acorta la tabla online para que queden registros a partir de min_ptr
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                session.query(Online).filter(Online.id < min_ptr).delete(synchronize_session=False)
                session.commit()
                d_rsp = {'status_code': 200}        

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp
