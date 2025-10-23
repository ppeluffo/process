#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import datetime as dt
import pickle
import redis

class DatalineService:
    """
    """
    def __init__(self):
        self.unit = None
        self.d_dataline = None
        self.d_payload = None
        self.pk_dataline = None
        self.pk_datetime = None
        self.d_datastrct = None
        self.rh = redis.Redis('127.0.0.1')

    def save_dataline(self, unit=None, pk_dataline=None):
        """
        """
        try:
            _ = self.rh.hset( unit, 'PKLINE', pk_dataline )
        except Exception as e:
            print( f"Redis Error {e}")
            return False
        return True
        #
    
    def save_timestamp(self, unit=None, pk_timestamp=None):
        """
        Los timestamps se ponen en un hash, con clave la unit, y picleados
        """

        try:
            _ = self.rh.hset( 'TIMESTAMP', unit, pk_timestamp )
        except Exception as e:
            print( f"Redis Error {e}")
            return False
        # 
        return True
    
    def enqueue_dataline(self, unit=None, pk_datastruct=None):

        try:
            _ = self.rh.rpush( 'RXDATA_QUEUE', pk_datastruct)
        except Exception as e:
            print( f"Redis Error {e}")
            return False
        # 
        return True

    def process_dataline(self, unit=None, unit_type=None, d_dataline=None):
        """
        Al recibir un dataline se hacen 3 funciones:
        - Se guarda en el HSET de la unidad
        - Se guarda el timestamp en el HSET TIMESTAMP. Este nos permite saber cuando llegaron el ultimo dato de c/unidad
        - Se guarda en una cola de datos recibidos RXDATA_QUEUE.
        """

        self.unit = unit
        self.d_dataline = d_dataline

        print(f"d_dataline={d_dataline}")
        
        # Timestamp: Indica la fecha/hora de recibido el dato.
        timestamp = dt.datetime.now()
        try:
            self.pk_timestamp = pickle.dumps(timestamp)
        except Exception as e:
            print( f"DatalineService:process_dataline: {e}")
            return False
        #
        # pk_dataline: Los datos recibidos se guardan y encolan en forma serializada pickle
        self.d_payload = d_dataline.get('dataline',{})
        try:
            self.pk_dataline = pickle.dumps(self.d_payload)
        except Exception as e:
            print( f"DatalineService:process_dataline: {e}")
            return False
        #
        # pk_datastruct: Estructura de datos serializada que se encola en RXDATA_QUEUE
        self.d_datastruct = {'TYPE':unit_type, 'ID':unit, 'D_LINE':self.d_payload}
        try:
            self.pk_datastruct = pickle.dumps(self.d_datastruct)
        except Exception as e:
            print( f"DatalineService:process_dataline: {e}")
            return False
        #
        # Debemos hacer 3 operaciones en la redis:
        # 1. Guardamos los datos en el HSET de la unidad
        if not self.save_dataline(self.unit, self.pk_dataline): 
            return False
        
        # 2. Guardamos el timestamp
        if not self.save_timestamp(self.unit, self.pk_timestamp):
            return False
        
        # 3. Encolo todos los datos en RXDATA_QUEUE para luego procesarlos y pasarlos a pgsql.
        if not self.enqueue_dataline(self.unit, self.pk_datastruct):
            return False
        
        return True
