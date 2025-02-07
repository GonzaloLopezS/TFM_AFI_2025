import pandas as pd
from AAA_code.zip_processing import *

csv_filename = "quarterly-port-freight-statistics-july-to-september-2024-tables.zip"
zip_filenames = ["quarterly-port-freight-statistics-july-to-september-2024-tables.zip"]
directory = 'home_uk'

for i in zip_filenames:
    path_to_zip_file = directory + '/' + i
    href_in = i
    print(path_to_zip_file)
    print(i)

    # Captura de datos:
    uncompress_zip(csv_filename, path_to_zip_file, directory)

    # Extraccion y Transformación:
    dataframe_csv = data_extraction(csv_filename)
    data_transformation(dataframe_csv, cargo_vessels, csv_filename)

    # Eliminacion del fichero .zip una vez extraidos los datos:
    file_elimination(csv_filename, path_to_zip_file)
