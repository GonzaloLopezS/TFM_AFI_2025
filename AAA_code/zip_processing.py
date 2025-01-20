import pandas as pd
import zipfile
import os
import requests
from bs4 import BeautifulSoup
import re
import calendar

# 1. scraping a página de zips
def web_scraping(url_in, href_in):
    response = requests.get(url_in)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    file_link = soup.find('a', href=href_in)
    return file_link

# 2. descargar .zip
def download_zip(file_link_in, path_to_zip_file):
    if file_link_in:
        download_url = url.rsplit("/", 1)[0] + "/" + file_link_in['href'] # si no, = url
        print(f"Enlace encontrado: {download_url}")

        # Descargamos el archivo:
        zip_response = requests.get(download_url)
        zip_response.raise_for_status()

        # Guardar fichero en disco:
        target_file = path_to_zip_file #os.path.join(directory, csv_filename)
        with open(target_file, 'wb') as file:
            file.write(zip_response.content)
        print(f"Archivo {target_file} descargado con éxito.")
    else:
        print("No se encontró el enlace al archivo.")

    # convertir path_to_zip_file en puntero a fichero .csv:
    csv_filename = target_file.replace(".zip",".csv")
    return csv_filename

# 3. descomprimir zip
# csv_path = os.path.join(directory, csv_filename)
def uncompress_zip(csv_filename_in, path_to_zip_file_in, directory_in):
    if not os.path.exists(csv_filename_in):
        print(f"El archivo {csv_filename_in} no está extraído. Descomprimiendo...")
        with zipfile.ZipFile(path_to_zip_file_in, 'r') as zip_ref:
            zip_ref.extractall(directory_in)
    else:
        print(f"El archivo {csv_filename_in} ya está extraído. Saltando descompresión.")

# 4. extraer datos -> pd.DataFrame
def data_extraction(csv_filename_in):
    dataframe_csv = pd.read_csv(csv_filename_in)
    # df_sorted = df.sort_values(by = ['Cargo'], ascending= False)
    return dataframe_csv

# 5. obtener datos de interés -> guardarlos (revisar mmsi)
def data_transformation(df_in, vessel_type_list, csv_filename_in):
    df_unique = df_in.drop_duplicates(subset='MMSI', keep='first')

    # Eliminacion de NAs:
    nan_percentage = df_unique.isna().mean(axis=1)
    df_unique = df_unique[nan_percentage < 8/18]

    df_cargo = df_unique.loc[df_unique['VesselType'].isin(vessel_type_list)]
    df_cargo.sort_values(by = ['Length'], ascending= False)

    # Guardar dataframe procesado:
    dataframe_procesado = directory + "/" + "df_procesado_" + csv_filename_in.split("/")[1]
    df_cargo.to_csv(dataframe_procesado, index = False)

# 6. eliminar .zip y fichero original
def file_elimination(csv_original_in, zip_original_in):
    if os.path.exists(csv_original_in):
        os.remove(csv_original_in)
        print(f"Archivo CSV original '{csv_original_in}' eliminado.")

    if os.path.exists(zip_original_in):
        os.remove(zip_original_in)
        print(f"Archivo ZIP original '{zip_original_in}' eliminado.")
