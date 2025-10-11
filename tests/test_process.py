#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Este script genera datos que inserta en la redis simulando al servidor APICOMMS
Debemos poder controlar cuantos datos insertamos por minuto de modo de simular
la carga de muchos equipos.
En una primera instancia NO voy a usar multiproceso.
"""
from datetime import datetime
import random
import requests
import time
import argparse

FRAMES_X_MINUTO = 200

URL_REDIS = "http://localhost:5100/apiredis/"

l_equipos = [ "UYTAC014","CCPRES004","KYTQTEST","UYPAY026","UYCDP033","UYCOL524","RIVTQ005","PSTCAU02","DNOTQ004"]
l_tags = ["PA","PB","Q0","Q1","bt12v","H1","NT"]

def gen_new_frame():
    """
    Genero un frame con el formato:
    {'TYPE':args['type'], 'ID':args['unit'], 'D_LINE':d_params}.

    """
    # Elijo un equipo aleatoriamente de la lista
    equipo_id = random.choice(l_equipos)
    # Elijo 4 tags aleatorios sin repeticion de la lista
    tags = random.sample(l_tags, 4)

    date = datetime.now().strftime("%y%m%d")
    time = datetime.now().strftime("%H%M%S")

    # Armo la linea de parámetros
    d_params = {'DATE': date, 'TIME':time}
    for tag in tags:
        d_params[tag] = random.uniform(0, 10)
    
    # Armo el frame
    frame = {'TYPE':'DLG', 'ID':equipo_id, 'D_LINE':d_params}

    return frame

def insert_frame( frame ):

    print(frame)
    
    unit_id = frame.get('ID','DEFAULT')
    device_type = frame.get('TYPE','SPX')
    payload = { 'dataline': frame.get('D_LINE',{}) }

    try:
        r = requests.put( URL_REDIS + 'dataline', params={'unit':unit_id,'type':device_type}, json=payload, timeout=10 )
        if r.status_code != 200:
            print(f"INSERT ERROR {r.status_code}")
    except Exception as e:
        print(f"Exception {e}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser("Generador de frames de dataloggers")
    parser.add_argument("--framesxmin", "-f", type=int, default=10, help="Frames x minuto")

    args = parser.parse_args()

    frames_x_minuto = args.framesxmin
    frames_x_segundo = frames_x_minuto / 60
    intervalo = 1 / frames_x_segundo

    print(f"Generando {frames_x_minuto} frames x minuto.")
    print(f"Intervalo interframes: {intervalo:.2f} secs.")
    while True:

        start = time.perf_counter()

        frame = gen_new_frame()
        insert_frame( frame )
        
        elapsed = time.perf_counter() - start
        time.sleep(max(0, intervalo - elapsed))




