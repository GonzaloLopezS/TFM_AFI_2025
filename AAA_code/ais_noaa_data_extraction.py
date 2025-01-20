import pandas as pd
from AAA_code.zip_processing import *

url = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2024/index.html"
directory = 'ais_noaa_gov'

# crear expresion regular para obtener todos los .zip:
base_name = 'AIS_2024_09' # variable con los nombres de los ficheros
zip_filenames = [f"{base_name}_{str(i).zfill(2)}.zip" for i in range(1, 31)]
cargo_vessels = [70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0]

# 7. repetir 1-6
for i in zip_filenames:
    path_to_zip_file = directory + '/' + i
    href_in = i
    print(path_to_zip_file)
    print(i)

    # Captura de datos:
    file_link = web_scraping(url, href_in)
    csv_filename = download_zip(file_link, path_to_zip_file)
    uncompress_zip(csv_filename, path_to_zip_file, directory)

    # Extraccion y Transformación:
    dataframe_csv = data_extraction(csv_filename)
    data_transformation(dataframe_csv, cargo_vessels, csv_filename)

    # Eliminacion del fichero .zip una vez extraidos los datos:
    file_elimination(csv_filename, path_to_zip_file)

# Carga del nuevo dataframe:
# dataframe_loaded = pd.read_csv(directory + "/" + dataframe_procesado)

# Revisar variables que manejan directory y filenames.
# Igual es posible extender su uso a spark. Problema: limite de librerias.
# Si pudiera, se podría extender la captura de datos para análisis.