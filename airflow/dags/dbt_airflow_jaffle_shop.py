from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

from datetime import datetime, timedelta
import os

# Define define arguments for DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 5, 8),
    "email": ['airflow@airflow.com'],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

# Define dbt commands
dbt_debug_cmd = "bash -c 'dbt debug'"

dbt_run_cmd = "bash -c 'dbt run'"

dbt_test_cmd = "bash -c 'dbt test'"

# Each container needs access to the dbt job and profiles.yml from ~/.dbt
mounts = [
    Mount(
        source=os.environ.get('DBT_JOB_PATH'),
        target="/usr/app",
        type="bind"
    ),
    Mount(
        source=os.environ.get('DOT_DBT_PATH'),
        target="/root/.dbt",
        type="bind"
    )
]

with DAG(
    dag_id="dbt_airflow_jaffle_shop",
    default_args=default_args,
    schedule_interval="@daily"
) as dag:
    
    dbt_debug = DockerOperator(
        task_id="dbt-debug",
        container_name="dbt-debug",
        image="dbt-job-jaffle-shop:latest",
        command=dbt_debug_cmd,
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        auto_remove=True,
        mounts=mounts,
        mount_tmp_dir=False
    )   
    
    dbt_run = DockerOperator(
        task_id="dbt-run",
        container_name="dbt-run",
        image="dbt-job-jaffle-shop:latest",
        command=dbt_run_cmd,
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        auto_remove=True,
        mounts=mounts,
        mount_tmp_dir=False
    )   

    dbt_test = DockerOperator(
        task_id="dbt-test",
        container_name="dbt-test",
        image="dbt-job-jaffle-shop:latest",
        command=dbt_test_cmd,
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        auto_remove=True,
        mounts=mounts,
        mount_tmp_dir=False
    )   

    dbt_debug >> dbt_run >> dbt_test