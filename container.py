#!/home/pablo/Spymovil/python/proyectos/API_SPYAPP/.venv/bin/python3

from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from servicios.datosservice import DatosService
from repositorio.repodatos import RepoDatos

from datasources.ds_pgsql.apibdpgsql import ApiBdPgsql
from datasources.ds_redis.apibdredis import ApiBdRedis

from utilidades.login_config import configure_logger

from config import settings

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

    # Engine y session factory BDLOCAL
    engine_pgsql = providers.Singleton(
        create_engine,
        url=settings.PGSQL_URL, 
        echo=False, 
        isolation_level="AUTOCOMMIT", 
        connect_args={'connect_timeout': 5}
    )

    session_pgsql = providers.Singleton(
        sessionmaker,
        bind = engine_pgsql
    )
    
    # Datasources
    ds_redis = providers.Factory(ApiBdRedis, logger=logger)
    ds_pgsql = providers.Factory( ApiBdPgsql, session_factory = session_pgsql, logger=logger )
    
    # Repositorios
    repo = providers.Factory(RepoDatos,ds_redis=ds_redis, ds_pgsql=ds_pgsql, logger=logger)
    
    # Servicios
    datos_service =  providers.Factory(DatosService, repositorio=repo, logger=logger)


