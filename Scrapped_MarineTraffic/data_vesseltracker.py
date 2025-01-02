import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random

def extract_container_content(url, output_csv):
    try:
        # Realiza la solicitud GET a la URL
        response = requests.get(url)
        response.raise_for_status()  # Verifica que la solicitud sea exitosa

        # Analiza el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra el contenedor con la clase especificada
        container = soup.find('div', class_='results-table')

        if container:
            # Encuentra las filas de datos dentro de las clases 'row odd' y 'row even'
            rows = container.find_all('div', class_=['row odd', 'row even'])
            table_data = []

            for row in rows:
                # Obtiene todas las columnas dentro de la fila
                cols = row.find_all('div')
                table_data.append([col.get_text(strip=True) for col in cols])

            # Escribe los datos en un archivo CSV
            with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(table_data)

            return f"Datos guardados en el archivo {output_csv}"
        else:
            return "No se encontró un contenedor con la clase 'results-table'."
    except requests.exceptions.RequestException as e:
        return f"Error al realizar la solicitud: {e}"

def generar_urls(base_url, paginacion, num_paginas):
    """
    Genera una lista de URLs con valores de página del 1 al num_paginas,
    introduciendo pausas aleatorias entre cada iteración.

    Args:
        base_url: La parte fija de la URL.
        num_paginas: El número máximo de páginas a generar.
        media_pausa: La media de la pausa en segundos.
        desviacion_tipica: La desviación estándar de la pausa en segundos.
    """
    url_prototype = base_url + paginacion
    urls = []
    for i in range(1, num_paginas + 1):
        url = url_prototype.replace("X", str(i))
        urls.append(url)

    return urls
    
# URL de la página que deseas analizar
url = "https://www.vesseltracker.com/en/ports.html"
num_paginas = 30
media_pausa = 2.5
desviacion_tipica = 0.55

paginacion = "?page=X&sortOrder=desc&sortField=noOfShips"
mis_urls = generar_urls(url, paginacion, num_paginas)

# Nombre del archivo CSV de salida
current_date = datetime.now().strftime("_%Y%m%d")
output_csv = f"port_data_vesseltracker_{current_date}.csv"

# Llama a la función y muestra el resultado
for pagina in mis_urls:
    result = extract_container_content(pagina, output_csv)
    print(result)

    #Pausa aleatoria:
    pausa = random.normalvariate(media_pausa, desviacion_tipica)
    time.sleep(max(0, pausa))

