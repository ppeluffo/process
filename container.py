#!/home/pablo/Spymovil/python/proyectos/API_SPYAPP/.venv/bin/python3

from dependency_injector import containers, providers

from servicios.datosservice import DatosService
from repositorio.repodatos import RepoDatos

from datasources.ds_pgsql.apibdpgsql import ApiBdPgsql
from datasources.ds_redis.apibdredis import ApiBdRedis

from utilidades.login_config import configure_logger

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(
        modules=["servicios.datosservice", 
                 "repositorio.repodatos",
                 "datasources.ds_pgsql.apibdpgsql",
                 "datasources.ds_redis.apibdredis" 
                 ]
    )
    
    # Logger (singleton compartido)
    logger = providers.Singleton(configure_logger, name="app-process")

    # Datasources
    ds_bdredis = providers.Factory(ApiBdRedis, logger=logger)
    ds_bdpgsql = providers.Factory(ApiBdPgsql, logger=logger )
    
    # Repositorios
    repo = providers.Factory(RepoDatos,ds_bdredis=ds_bdredis, ds_bdpgsql=ds_bdpgsql, logger=logger)
    
    # Servicios
    datos_service =  providers.Factory(DatosService, repositorio=repo, logger=logger)


