import numpy as np
import pandas as pd
import requests
import time
import random
import csv
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Datetime and csv file to export:
x = datetime.datetime.now()
date_part = x.strftime("%Y%m%d")
csv_export_filename = date_part + "_marinetraffic_ports.csv"

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

# Configuracion del driver de Firefox:
def driver_configuration():
    firefox_options = Options()
    # firefox_options.add_argument("--headless")
    firefox_options.add_argument("--incognito")
    service = Service(geckodriver_service)
    # firefox_options.binary_location = firefox_path
    print("Preparando el driver")
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def prueba_con_google():
    driver = driver_configuration()

    try:
        # Apertura de la página web:
        print("Antes de entrar en url")
        driver.get("https://www.google.com")

        print(driver.title)
        # driver.implicitly_wait(15)
        # print("Tras 15 segundos")

        # Rechazar cookies:
        try:
            boton_rechazar = WebDriverWait(driver, 10).until(
                # EC.element_to_be_clickable((By.XPATH,"//button[text()='Rechazar todo'] | //button[text()='Rechazar']"))
                # EC.element_to_be_clickable((By.NAME,"")) # id="W0wltc"
                EC.element_to_be_clickable((By.ID,"W0wltc")) # id="W0wltc"
            )
            boton_rechazar.click()
            print("Cookies rechazadas")
        except:
            print("No se encontró el botón de rechazo de cookies.")

        #Ignorar otras ventanas emergentes:
        try:
            ventanas_emergentes = driver.find_elements(By.XPATH, "//button[contains(text(),'No, gracias') or contains(text(),'Cerrar')]")
            for boton in ventanas_emergentes:
                boton.click()
            print("Ventanas emergentes cerradas.")
        except:
            print("No se encontraron ventanas emergentes")

        # Hacer click en otra pestaña:
        try:
            imagenes_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Imágenes']"))
            )
            imagenes_tab.click()
            print("Se hizo clic en la pestaña 'Imágenes'.")
        except Exception as e:
            print(f"No se pudo encontrar o hacer clic en la pestaña 'Imágenes': {e}")

        # Mantén el navegador abierto un momento para visualizar el resultado
        time.sleep(5)

    finally:
        driver.quit()


# if __name__ == "__main__":
#     main()

def extract_marinetraffic():
    driver = driver_configuration()

    try:
        driver.get(url_puertos)
        print(driver.title)
        driver.implicitly_wait(15)

        # Click on cross:
        close_button = driver.find_element(By.NAME, "4zd751")
        close_button.click()

        # Cookies:
        try:
            boton_rechazar = WebDriverWait(driver, 10).until(
                # EC.element_to_be_clickable((By.XPATH,"//button[text()='Rechazar todo'] | //button[text()='Rechazar']"))
                # EC.element_to_be_clickable((By.NAME,"")) # id="W0wltc"
                EC.element_to_be_clickable((By.ID,"W0wltc")) # id="W0wltc"
            )
            boton_rechazar.click()
            print("Cookies rechazadas")
        except:
            print("No se encontró el botón de rechazo de cookies")

        # Ventanas emergentes:
        try:
            ventanas_emergentes = driver.find_elements(By.XPATH, "//button[contains(text(),'No, gracias') or contains(text(),'Cerrar')]")
            for boton in ventanas_emergentes:
                boton.click()
            print("Ventanas emergentes cerradas.")
        except:
            print("No se encontraron ventanas emergentes")

        # Extraer datos de la tabla y cargarlos a un .csv:
        try:

            # Extraccion de la cabecera:
            

            # Extraccion de las filas de datos:
            data_block = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "1xdhyk6")) #class_name: MuiDataGrid-virtualScrollerContent
            )
            
            rows_data = data_block.find_elements(By.NAME, "MuiDataGrid-row")
            datos = []

            #Lectura fila a fila:
            for row in rows_data:
                cells = row.find_elements(By.NAME, "MuiDataGrid-cell")
                cells_texts = [cell.text for cell in cells]
                row_data =  cells_texts
                # {
                #     "data-id": row.get_attribute("data-id")
                #     "cells": cells_texts
                # }
                datos.append(row_data)

                # Espera entre iteracion e iteración:
                time.sleep(random.uniform(0.3,3))
                print(row_data)

            registros = datos


            # guardar los registros en un fichero .csv:
            try:
                nombre_archivo = csv_export_filename
                with open(nombre_archivo, mode="w", encoding = "utf-8", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    # csv_writer.writerow(header)
                    csv_writer.writerows(registros)
                print(f"Los datos se han guardado en el archivo: {nombre_archivo}")

            except:
                print("No se pudieron guardar los datos")

        except Exception as e:
            print(f"No se pudo tratar la tabla de MarineTraffic: {e}")

        # Mantén el navegador abierto un momento para visualizar el resultado
        time.sleep(5)

    finally:
        driver.quit()

extract_marinetraffic()