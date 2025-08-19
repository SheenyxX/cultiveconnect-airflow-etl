# etl-cafeteros.py
# -*- coding: utf-8 -*-
"""
Script de Python para la extracción de datos y carga a Google Cloud Storage (GCS).
Diseñado para ser ejecutado dentro de un contenedor de Docker y orquestado por Airflow.
"""

import pandas as pd
import requests
from google.cloud import storage
from datetime import datetime
import io
import os

# =======================================================================================
# 1. Configuración del proyecto y la URL de descarga
# =======================================================================================
# La URL directa del archivo Excel de la Federación Colombiana de Cafeteros
url_archivo_excel = "https://federaciondecafeteros.org/app/uploads/2025/01/Precios-area-y-produccion-de-cafe-2025.xlsx"
bucket_name = "fncc-precio-mensual-cop--125kg-cafe-pergamino-seco"

# La clave de autenticación se gestionará a través de la variable de entorno
# GOOGLE_APPLICATION_CREDENTIALS, que Airflow inyectará en el contenedor.
# Se espera que el archivo de clave JSON se encuentre en la ruta especificada por esta variable.

# =======================================================================================
# 2. Autenticación y descarga de datos
# =======================================================================================
try:
    storage_client = storage.Client()
    print("Autenticación exitosa con Google Cloud. Usando GOOGLE_APPLICATION_CREDENTIALS.")
except Exception as e:
    print(f"Error de autenticación: {e}")
    # En un entorno de orquestación, es mejor no salir y dejar que la tarea falle.
    raise

try:
    response = requests.get(url_archivo_excel)
    response.raise_for_status()
    print("Archivo Excel descargado exitosamente.")
    excel_data = io.BytesIO(response.content)
except requests.exceptions.RequestException as e:
    print(f"Error al descargar el archivo: {e}")
    raise

# =======================================================================================
# 3. Extracción y transformación de datos con Pandas
# =======================================================================================
try:
    df_precio_mensual = pd.read_excel(
        excel_data,
        sheet_name="2. Precio Interno Mensual",
        skiprows=5,
        usecols=[3, 4]
    )
    df_precio_mensual.columns = ["fecha", "precio_interno"]
    df_precio_mensual = df_precio_mensual.dropna(subset=["fecha"])
    df_precio_mensual["fecha"] = pd.to_datetime(df_precio_mensual["fecha"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    df_precio_mensual["precio_interno"] = pd.to_numeric(df_precio_mensual["precio_interno"], errors="coerce")
    df_precio_mensual = df_precio_mensual.dropna(subset=["precio_interno"])
    print("Datos transformados con éxito.")
except Exception as e:
    print(f"Error en el procesamiento de datos con Pandas: {e}")
    raise

# =======================================================================================
# 4. Carga de datos a Google Cloud Storage
# =======================================================================================
try:
    csv_string_buffer = io.StringIO()
    df_precio_mensual.to_csv(csv_string_buffer, index=False)
    csv_string = csv_string_buffer.getvalue()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination_blob_name = f"precio_interno_mensual/limpio/precio_interno_mensual_{timestamp}.csv"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(csv_string, content_type='text/csv')

    print(f"Archivo {destination_blob_name} subido a {bucket_name} exitosamente.")
except Exception as e:
    print(f"Error al subir el archivo a GCS: {e}")
    raise

