# Data Pipeline de la Federación Nacional de Cafeteros

Este proyecto es una pipeline de datos automatizada construida con **Apache Airflow** y **Docker**. Su objetivo es extraer datos sobre el precio interno del café de un archivo Excel de la Federación Nacional de Cafeteros, realizar transformaciones básicas y cargar la información en un bucket de **Google Cloud Storage (GCS)**.

-----

## 1\. Características del Proyecto

  * **Orquestación**: Se utiliza **Airflow** para programar y monitorear la ejecución de la pipeline.
  * **Contenedorización**: El proceso ETL se ejecuta de forma aislada dentro de un contenedor de Docker, lo que garantiza la portabilidad y un entorno de ejecución consistente.
  * [cite\_start]**Extracción de Datos**: El script `etl-cafeteros.py` descarga un archivo `.xlsx` directamente de la página web de la Federación Nacional de Cafeteros de Colombia[cite: 1, 4].
  * [cite\_start]**Transformación**: Se utiliza la librería **Pandas** para limpiar, filtrar y formatear los datos extraídos[cite: 1, 4].
  * [cite\_start]**Carga de Datos**: La información procesada se guarda como un archivo `.csv` en un bucket de GCS[cite: 1, 4].

-----

## 2\. Requisitos y Dependencias

Para ejecutar este proyecto localmente, necesitas tener instalados los siguientes programas:

  * **Docker Desktop**: La herramienta para construir y gestionar los contenedores Docker.
  * **Git**: Para clonar este repositorio.

-----

## 3\. Estructura del Proyecto

  * `dags/`: Contiene el DAG de Airflow (`etl_dag.py`) que define la pipeline.
  * `etl-cafeteros.py`: El script Python que realiza la extracción, transformación y carga (ETL).
  * [cite\_start]`Dockerfile`: El archivo que define cómo se construye la imagen de Docker para el script ETL[cite: 2].
  * `docker-compose.yaml`: Configuración para levantar el clúster de Airflow (Webserver, Scheduler, etc.).
  * [cite\_start]`requirements.txt`: Lista las librerías de Python necesarias para el script ETL[cite: 1].
  * [cite\_start]`.env`: Archivo de configuración para variables de entorno de Docker[cite: 7].
  * [cite\_start]`cultiveconnect-fc0aa870574b.json`: (Archivo confidencial) Credenciales de servicio de Google Cloud para la autenticación[cite: 5].

-----

## 4\. Configuración y Autenticación

[cite\_start]El proyecto utiliza una cuenta de servicio de Google Cloud para autenticarse y subir archivos a GCS[cite: 5]. [cite\_start]El archivo `cultiveconnect-fc0aa870574b.json` contiene las credenciales necesarias[cite: 5].

**Pasos de Configuración:**

1.  Crea tu propia cuenta de servicio en Google Cloud y descarga el archivo JSON de credenciales.
2.  [cite\_start]Renombra tu archivo JSON a `cultiveconnect-fc0aa870574b.json` y colócalo en la misma carpeta raíz del proyecto[cite: 5].
3.  [cite\_start]El `Dockerfile` copia este archivo en la imagen de Docker y establece la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` para que el script pueda encontrarlo[cite: 2].

> **ADVERTENCIA**: Por motivos de seguridad, el archivo de credenciales de Google Cloud **NO DEBE** ser subido a repositorios públicos como GitHub. [cite\_start]El `Dockerfile` está diseñado para funcionar con el nombre específico de tu archivo[cite: 2].

-----

## 5\. Instrucciones de Uso (Paso a Paso)

Sigue estos pasos para poner en marcha la pipeline.

### Paso 1: Clonar el Repositorio

Abre tu terminal y clona el proyecto:

```bash
git clone https://github.com/tu-usuario/nombre-de-tu-repo.git
cd nombre-de-tu-repo
```

### Paso 2: Configurar el Entorno

Configura el ID de usuario de Airflow y construye la imagen de Docker para tu script ETL.

1.  Crea un archivo `.env` para definir el ID de usuario. Esto evita problemas de permisos de archivos.
    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
2.  Construye la imagen de Docker que contiene tu script ETL y sus dependencias.
    ```bash
    docker build -t cultiveconnect-etl .
    ```

### Paso 3: Inicializar la Base de Datos y Crear el Usuario

[cite\_start]Antes de iniciar todos los servicios, es necesario inicializar la base de datos de Airflow y crear el usuario administrador por defecto[cite: 1, 2, 7].

```bash
docker compose up airflow-init
```

Este comando levanta un contenedor temporal que realiza las migraciones de la base de datos y crea un usuario `airflow` con la contraseña `airflow`. La tarea debería terminar con un mensaje similar a `"User "airflow" created with role "Admin""`.

### Paso 4: Levantar los Servicios de Airflow

Una vez que la base de datos está inicializada, puedes levantar todos los demás servicios de Airflow en segundo plano.

```bash
docker compose up -d
```

### Paso 5: Acceder a la Interfaz de Usuario (UI) de Airflow

Abre tu navegador web y navega a `http://localhost:8080`.

  * **Usuario**: `airflow`
  * **Contraseña**: `airflow`

En la UI, verás el DAG `etl_cafeteros_docker_dag` y podrás activarlo o monitorear su ejecución.

### Paso 6: Detener el Entorno de Airflow

Para detener todos los servicios y liberar recursos, ejecuta:

```bash
docker compose down
```

-----

## Contribuciones

Si deseas contribuir, por favor, abre un "issue" o envía un "pull request".

## Licencia

Este proyecto está bajo la licencia [Tu Licencia (por ejemplo: MIT)].
