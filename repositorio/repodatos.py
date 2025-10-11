

class RepoDatos:

    def __init__(self, ds_sourcedata, ds_destdata, logger):
        self.ds_source = ds_sourcedata
        self.ds_dest = ds_destdata
        self.logger = logger
        
    def leer_datos_encolados(self):
        """
        Los datos encolados están en la REDIS( source )
        """
        self.logger.debug("")

        return self.ds_source.leer_datos_encolados()

    def insertar_datos_bulk(self, l_datos_formateados):
        """
        """
        self.logger.debug("")

        return self.ds_dest.insertar_datos_bulk(l_datos_formateados)

    def do_housekeeping(self):
        """
        """
        self.logger.debug("")

        return self.ds_dest.do_housekeeping()
    

