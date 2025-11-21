from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_mysql_to_kafka',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Run PySpark ETL job to read from MySQL and write to Kafka'
) as dag:
    run_etl = SparkSubmitOperator(
        task_id='run_pyspark_etl',
        application='/opt/pipeline/pyspark_etl.py',
        name='etl_mysql_to_kafka',
        conf={
            'spark.jars.packages': 'mysql:mysql-connector-java:8.0.27,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0'
        }
    )
