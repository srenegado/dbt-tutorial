#!/bin/bash

docker build --tag dbt-job-jaffle-shop:latest \
  --target dbt-third-party \
  --build-arg dbt_third_party=dbt-bigquery \
  .