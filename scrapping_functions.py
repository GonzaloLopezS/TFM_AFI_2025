import numpy as np
import pandas as pd
from marinetrafficapi import MarineTrafficApi

# Opcion A: funcion de extraccion de datos mediante API
try:
    api = MarineTrafficApi(api_key="565b636b073b55b4de19a39b55c2a3cde88c4f3f")
    vessel_positions = api.vessel_historical_track()
except:
    print("No funciona")

# Opcion B: funcion de extraccion de datos mediante web scrapping
print("Opción de entrar en MarineTraffic")

# Variables globales:
url_principal = 'https://www.marinetraffic.com/en/data/'

# Datos de puertos:
sub_ports = '?asset_type=ports'
# columns_ports = '&columns=flag,portname,unlocode,photo,vessels_in_port,vessels_departures,vessels_arrivals,vessels_expected_arrivals,local_time,anchorage,geographical_area_one,geographical_area_two,coverage'
columns_ports = '&columns=flag%2Cportname%2Cunlocode%2Cvessels_in_port%2Cvessels_departures%2Cvessels_arrivals%2Cvessels_expected_arrivals%2Clocal_time%2Cgeographical_area_one%2Cgeographical_area_two'
filters_ports = '&geographical_area_one_in=NPAC|North+Pacific%2CUSWC|US+West+Coast%2CJAPAN|Japan+Coast%2CSCHINA|South+China%2CCCHINA|Central+China'

url_puertos = url_principal + sub_ports + columns_ports + filters_ports
print(url_puertos)

# Datos de embarcaciones:
sub_vessels = '?asset_type=vessels'
# columns_vessels = '&imo,mmsi,reported_destination, reported_eta,time_of_latest_position'
columns_vessels = '&columns=imo%2Cmmsi%2Creported_destination%2Creported_eta%2Ctime_of_latest_position'
filters_vessels = '&ship_type_in=7|Cargo+Vessels'

url_vessels = url_principal + sub_vessels + columns_vessels + filters_vessels
print(url_vessels)

try:
    print("Hola")

    #http request a alguna de las páginas:
    

except:
    print("Not working")

# Desarrollo en dev_december2024

# Fuente: https://www.marinetraffic.com/en/data/