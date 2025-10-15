

class RepoDatos:

    def __init__(self, ds_bdredis, ds_bdpgsql, logger):
        self.ds_bdredis = ds_bdredis
        self.ds_bdpgsql = ds_bdpgsql
        self.logger = logger
        
    def leer_datos_encolados(self):
        """
        Los datos encolados están en la REDIS( source )
        """
        self.logger.debug("")

        return self.ds_bdredis.leer_datos_encolados()

    def insertar_datos_bulk(self, l_datos_formateados):
        """
        """
        self.logger.debug("")

        return self.ds_bdpgsql.insertar_datos_bulk(l_datos_formateados)

    def do_housekeeping(self):
        """
        """
        self.logger.debug("")

        return self.ds_bdpgsql.do_housekeeping()
    

