from __future__ import annotations
import pendulum
from docker.types import Mount
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id="etl_cafeteros_docker_dag",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 9 * * 1",
    catchup=False,
    tags=["etl", "gcs"],
) as dag:
    run_etl_script = DockerOperator(
        task_id="run_etl_script",
        # La imagen que construiste con tu Dockerfile
        image="cultiveconnect-etl",
        container_name="task_etl_container",
        api_version="auto",
        docker_url="unix:///var/run/docker.sock",
        network_mode="bridge",
        auto_remove="force",
        mount_tmp_dir=False,
        # Ya no se necesita el mount del archivo de credenciales
        # porque está empaquetado dentro de la imagen.
        mounts=[
            Mount(source="/var/run/docker.sock", target="/var/run/docker.sock", type="bind"),
        ]
    )