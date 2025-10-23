

class RepoDatos:

    def __init__(self, ds_redis, ds_pgsql, logger):
        self.ds_redis = ds_redis
        self.ds_pgsql = ds_pgsql
        self.logger = logger
        
    def pop_rxlines(self):
        """
        Los datos encolados están en la REDIS( source )
        """
        self.logger.debug("")

        return self.ds_redis.pop_rxlines()

    def insertar_datos_bulk_online(self, l_datos_bulk=None):
        """
        """
        self.logger.debug("")
        return self.ds_pgsql.insertar_datos_bulk_online(l_datos_bulk)
        
    def insertar_datos_bulk_historica(self, l_datos_bulk=None):
        """
        """
        self.logger.debug("")
        return self.ds_pgsql.insertar_datos_bulk_historica(l_datos_bulk)
       
    def do_housekeeping(self):
        """
        """
        self.logger.debug("")

        return self.ds_pgsql.achicar_tb_online()
    

