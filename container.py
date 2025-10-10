#!/home/pablo/Spymovil/python/proyectos/API_SPYAPP/.venv/bin/python3

from dependency_injector import containers, providers

from servicios.datosservice import DatosService
from repositorio.repodatos import RepoDatos

from datasources.ds_destination.api_destdata import ApiDestinationData
from datasources.ds_source.api_sourcedata import ApiSourceData

from utilidades.login_config import configure_logger

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(
        modules=["servicios.datosservice", 
                 "repositorio.repodatos",
                 "datasources.ds_destination.api_destdata",
                 "datasources.ds_source.api_sourcedata" 
                 ]
    )
    
    # Logger (singleton compartido)
    logger = providers.Singleton(configure_logger, name="app-process")

    # Datasources
    ds_sourcedata = providers.Factory(ApiSourceData, logger=logger)
    ds_destdata = providers.Factory(ApiDestinationData, logger=logger )
    
    # Repositorios
    repo = providers.Factory(RepoDatos,ds_sourcedata=ds_sourcedata, ds_destdata=ds_destdata, logger=logger)
    
    # Servicios
    datos_service =  providers.Factory(DatosService, repositorio=repo, logger=logger)


