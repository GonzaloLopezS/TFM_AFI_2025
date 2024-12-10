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
print("Hola Mundo")

# Desarrollo en dev_december2024

# Fuente: https://www.marinetraffic.com/en/data/