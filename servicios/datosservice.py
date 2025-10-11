#!/home/pablo/Spymovil/python/proyectos/API_SPYAPP/.venv/bin/python3
"""
"""

import datetime as dt
import time
import json

class DatosService:

    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    """
    def separar_por_tipo_dispositivo(self, l_datos):
  
        Cada elemento es del tipo: {'TYPE':args['type'], 'ID':args['unit'], 'D_LINE':d_params}.
        Los separo por TYPE y almaceno en 3 listas individuales

        self.logger.debug("")

        dlg_list = []
        plc_list = []
        oceanus_list = []
            
        # Separo los datos de c/tipo en una lista distinta
        sfechasys = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for element in l_datos:
            tipo = element.get('TYPE','UNKNOWN')
            id = element.get('ID','UNKNOWN')
            d_line = element.get('D_LINE',{})
            #
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
                self.logger.error( f"{tipo}:{key}:{value}")

                if 'DLG' in tipo:
                    dlg_list.append((sfechadata, sfechasys, id, key, value,))
                elif 'PLC' in tipo:
                    plc_list.append((sfechadata, sfechasys, id, key, value,))
                elif 'OCEANUS' in tipo:
                    oceanus_list.append((sfechadata, sfechasys, id, key, value,))

        return { 'l_dlg':dlg_list, 'l_plc':plc_list, 'l_oceanus': oceanus_list }
    """
    def leer_datos_encolados(self):
        """
        Devuelve siempre una lista.
        Si el repositorio indico que no hay datos (204), devuelve una lista vacia.
        """
        self.logger.debug("")

        d_rsp = self.repo.leer_datos_encolados()

        if d_rsp.get('status_code',0) == 200:
            l_datastruct = d_rsp.get('l_datastruct',[])
        else:
            l_datastruct = []
            
        #self.logger.info(f"Procesando: {len(l_datastruct)} frames.")
        #self.logger.debug(f"l_datastruct = {l_datastruct}")
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
            #print(f"ELEMENTO={element}")
            tipo = element.get('TYPE','UNKNOWN')
            id = element.get('ID','UNKNOWN')
            d_line = element.get('D_LINE',{})
            #
            #print(f"DLINE={d_line}")
            
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
                #self.logger.error( f"{tipo}:{key}:{value}")
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

        #self.logger.info(f"Procesando: {len(l_datos_formateados)} rcds.")
        return self.repo.insertar_datos_bulk(l_datos_formateados)

    def do_housekeeping(self):
        """
        """
        self.logger.debug("")

        return self.repo.do_housekeeping()
    
    
