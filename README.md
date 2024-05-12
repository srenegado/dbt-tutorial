# dbt-tutorial
This project shows how dbt can be run with Airflow and Docker containers. It does so by:
- building a Docker image from the dbt project, and
- running said image with the DockerOperator in an Airflow DAG.

## Setup
Some prerequisites:
- Install [Docker Desktop and Docker Compose](https://docs.docker.com/compose/install/).
- Install [dbt core](https://docs.getdbt.com/docs/core/installation-overview).
- This project uses BigQuery:
  - Setup an account through [GCP](https://cloud.google.com/free?hl=en).
  - Create a [new GCP project](https://docs.getdbt.com/guides/bigquery?step=2) and [generate BigQuery credentials](https://docs.getdbt.com/guides/bigquery?step=4).
  - [Connect to BigQuery](https://docs.getdbt.com/guides/manual-install?step=4), but ignore creating a new 'profiles.yml' file: use the `SAMPLE-profiles.yml` file here after renaming it.

In the `profiles.yml` file, change `GCP_PROJECT_ID` and `NAME_OF_YOUR_JSON_KEYFILE` appropriately.

In `airflow/.env`, set `DBT_JOB_PATH=/abs/path/of/this/project/dbt` and `DOT_DBT_PATH=/abs/path/to/.dbt`.

## Usage
### Build a Docker image
To run our dbt models in Docker containers, we need to build a Docker image.

`cd` to the `dbt` folder and run:
```
chmod u+x build-dbt-image.sh
./build-dbt-image.sh
```

Then run
```
docker image ls
```
to check if an image called `dbt-job-jaffle-shop` was made.

### Run Airflow with docker compose
First `cd` to the `airflow` folder and run
```
docker compose up airflow-init
```
That may take a while.

Then start up Airflow by running
```
docker compose up
```
That may also take a while.

### Checking out our dbt model
Open up the Airflow UI by going to `0.0.0.0:8080` in your browser. Login using `airflow` as username and password.

Congratulations! Your DAG should be up and running and your dbt models should be materialized. Check out BigQuery Console for your created tables.

## Acknowledgements
This work generally followed [this medium article](https://medium.com/@tdonizeti/how-to-run-dbt-core-from-an-airflow-pipeline-using-the-dockeroperator-e48cf215e9f6) by Thales Donizeti for integrating dbt core with Airflow.

The dbt project is based off dbt Lab's [Jaffle Shop project](https://github.com/dbt-labs/jaffle-shop).

The Dockerfile and compose.yml file are based off the official files supplied by dbt Lab and Airflow, respectively.

