#!/home/pablo/Spymovil/python/proyectos/API_SPYAPP/.venv/bin/python3
"""
"""

import datetime as dt
import time
import json
import pickle

class DatosService:

    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def pop_rxlines(self):
        """
        Devuelve siempre una lista.
        Si el repositorio indico que no hay datos (204), devuelve una lista vacia.
        """
        self.logger.debug("")

        d_rsp = self.repo.pop_rxlines()

        if d_rsp.get('status_code',0) == 200:
            l_pk_datastruct = d_rsp.get('l_pk_datastruct',[])
        else:
            l_pk_datastruct = []
            
        l_datastruct = []
        for pk_element in l_pk_datastruct:
            element = pickle.loads(pk_element)
            l_datastruct.append(element)

        #self.logger.debug(f"Procesando: {len(l_datastruct)} frames.")
        self.logger.debug(f"l_datastruct = {l_datastruct}")
        return l_datastruct
    
    def formatear_lista_datos(self, l_datos):
        """
        Tengo una lista de datos en el cual c/u tiene un formato:
        {'TYPE':args['type'], 'ID':args['unit'], 'D_LINE':d_params}

        Genero una nueva lista donde c/elemento va a tener un formato:
        (sfechadata, sfechasys, id, key, value)

        """
        self.logger.debug("")
        
        l_datos_formateados = []
        sfechasys = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for element in l_datos:
            #self.logger.debug(f"ELEMENTO={element}")
            tipo = element.get('TYPE','UNKNOWN')
            id = element.get('ID','UNKNOWN')
            d_line = element.get('D_LINE',{})
            #
            self.logger.debug(f"DLINE={d_line}")
            
            # Procesmos la linea de datos (d_line)
            # Como insertamos datetime pero los equipos envian date, time, debemos convertirlos
            ddate = d_line.pop('DATE',None)
            dtime = d_line.pop('TIME',None)
            if ddate and dtime:
                sfechadata = f'{ddate} {dtime}'
                try:
                    fechadata = dt.datetime.strptime(sfechadata, '%y%m%d %H%M%S')
                    sfechadata = fechadata.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    self.logger.error( f"Error-> {e}")
                    continue
            else:
                sfechadata = sfechasys
            #
            # Ahora procesamos los tag:value
            for key in d_line:
                value = d_line[key]
                #self.logger.debug( f"{tipo}:{key}:{value}")
                l_datos_formateados.append( {'fechadata':sfechadata,
                                             'fechasys':sfechasys,
                                             'equipo': id,
                                             'tag': key,
                                             'valor': value } )

        # Los jsonifico para poder enviarlo a que se inserten
        #keys = ['fechadata', 'fechasys', 'equipo', 'tag', 'valor']
        # Convierto la lista de tuplas en lista de diccionarios
        #l_datos_bulk_dicts = [dict(zip(keys, t)) for t in l_datos_bulk]

        return l_datos_formateados

    def insertar_datos_bulk(self, l_datos_formateados):
        """
        """
        self.logger.debug("")

        _ = self.repo.insertar_datos_bulk_online(l_datos_formateados)
        _ = self.repo.insertar_datos_bulk_historica(l_datos_formateados)

    def do_housekeeping(self):
        """
        """
        self.logger.debug("")

        return self.repo.do_housekeeping()
    
    
