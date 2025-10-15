#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import logging
import threading
import time
import sys

from config import settings

def set_log_level(level=None, timeout=60):
    """
    Cambia el nivel de log de un equipo en runtime.
    Si timeout está definido, revierte automáticamente a INFO luego de ese tiempo.
    """

    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Nivel inválido: {level}")

    logger = logging.getLogger('app-process')
    logger.setLevel(getattr(logging, level))

    print(f"[LOGGER] Nivel revertido a {level}")

    # Si hay timeout, crear un hilo que lo revierta
    if timeout and timeout > 0:
        threading.Thread(
            target=_revert_after_timeout,
            args=(timeout,),
            daemon=True
        ).start()

    return

def _revert_after_timeout(timeout):
    """
    Espera 'timeout' segundos y revierte el nivel a INFO.
    """
    time.sleep(timeout)
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    print(f"[LOGGER] Nivel revertido automáticamente a INFO después de {timeout} s")

def configure_logger(name="app-process", level=settings.LOG_LEVEL):
    
    logger = logging.getLogger(name)
    if not logger.handlers:  # evitar duplicar handlers si se configura varias veces
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger


