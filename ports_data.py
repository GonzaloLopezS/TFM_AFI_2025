import numpy as np
import pandas as pd
import requests
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# URLs y Direcciones:
service_dir = "/usr/local/bin/"
geckodriver_path = "geckodriver-v0.35.0-linux64/geckodriver"
geckodriver_service = "/snap/bin/firefox.geckodriver"
firefox_path = "/usr/bin/firefox"

# Url de marine traffic y datos de puertos:
url_principal = 'https://www.marinetraffic.com/en/data/'
sub_ports = '?asset_type=ports'
# columns_ports = '&columns=flag,portname,unlocode,photo,vessels_in_port,vessels_departures,vessels_arrivals,vessels_expected_arrivals,local_time,anchorage,geographical_area_one,geographical_area_two,coverage'
columns_ports = '&columns=flag%2Cportname%2Cunlocode%2Cvessels_in_port%2Cvessels_departures%2Cvessels_arrivals%2Cvessels_expected_arrivals%2Clocal_time%2Cgeographical_area_one%2Cgeographical_area_two'
filters_ports_pacific = '&geographical_area_one_in=NPAC|North+Pacific%2CUSWC|US+West+Coast%2CJAPAN|Japan+Coast%2CSCHINA|South+China%2CCCHINA|Central+China%2CCISPAC|CIS+Pacific%2CSPAC|South+Pacific%2CINLCN|Inland%2C+China%2CEAUS|East+Australia%2CINDO|Indonesia%2CNCHINA|North+China%2CPHIL|Philippines%2CSEASIA|South-East+Asia%2CWCCAN|West+Coast+Canada'
filters_ports_atlantic_mediterranean = '&geographical_area_one_in=WMED|West+Mediterranean%2CBALTIC|Baltic+Sea%2CNOATL|North+Atlantic%2CECSA|East+Coast+South+America%2CUSG|Gulf+of+Mexico%2CADRIA|Adriatic+Sea%2CUSWC|US+West+Coast%2CNORDIC|Norwegian+Coast%2CCARIBS|Caribbean+Sea%2CINLSAM|Inland%2C+South+America%2CINLEU|Inland%2C+Europe%2CECCA|East+Coast+Central+America%2CECCAN|East+Coast+Canada%2CNCSA|North+Coast+South+America%2CUKC|UK+Coast+%26+Atlantic%2CUSEC|US+East+Coast%2CWAFR|West+Africa'

# Construccion de la url compuesta para peticiones de puertos:
url_puertos = url_principal + sub_ports + columns_ports + filters_ports_pacific
print(url_puertos)

# Configuracion del navegador Firefox:
firefox_options = Options()
firefox_options.add_argument("--headless")
# firefox_options.add_argument("-profile")
# firefox_options.binary_location = firefox_path

service = Service(geckodriver_service) #service_dir + geckodriver_path
print("Preparando el driver")
driver = webdriver.Firefox(service=service, options=firefox_options) # Fallo aqui: 

# Apertura de la página web:
print("Antes de entrar en url")
driver.get("https://www.google.com")

print("Hasta aqui")
# Tiempo de espera de carga del contenido dinámico:
print(driver.title)
driver.implicitly_wait(15)
print("Tras 15 segundos")

# # Extraccion de la información:
container = driver.find_element(By.CLASS_NAME, "MuiDataGrid-topContainer")
headers = container.find_elements(By.CLASS_NAME, "MuiDataGrid-columnHeaderTitle")

for header in headers:
    time.sleep(random.uniform(0,3))
    print(header.text)

driver.quit()

####### DESCATALOGADO ###################
# print(url_puertos)

# # realizacion de la peticion http al servidor web:
# response = requests.get(url_puertos)

# # Respuesta del servidor:
# if response.status_code == 200:
#     print("solicitud realizada")
# else:
#     print(f"Error: {response.status_code}")

# Presentacion del contenido html