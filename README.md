# etl-spark-mysql-pipeline  

This repository provides a starter ETL pipeline built with PySpark. It reads data from a MySQL database using JDBC, applies a simple transformation, and then writes the results to an Apache Kafka topic. The repository includes a Dockerfile for containerized execution and a minimal Airflow DAG outline for scheduling the job.  

## Prerequisites  

- A running MySQL database with connectivity from your environment.  
- An Apache Kafka cluster available for data output.  
- Docker installed if you plan to build and run the containerized pipeline.  
- (Optional) Apache Airflow for workflow scheduling.  

## Getting Started  

1. **Clone the repository**:  

   ```bash  
   git clone https://github.com/icella/etl-spark-mysql-pipeline.git  
   cd etl-spark-mysql-pipeline  
   ```  

2. **Configure environment variables**: Create an `.env` file or export the following variables to define your MySQL and Kafka details:  

   ```bash  
   MYSQL_HOST=<your_mysql_host>  
   MYSQL_PORT=3306  
   MYSQL_DATABASE=<your_database_name>  
   MYSQL_TABLE=<your_source_table>  
   MYSQL_USER=<your_mysql_user>  
   MYSQL_PASSWORD=<your_mysql_password>  

   KAFKA_BOOTSTRAP_SERVERS=<your_kafka_bootstrap_servers>  
   KAFKA_TOPIC=<your_kafka_topic>  
   ```  

3. **Build the Docker image**:  

   ```bash  
   docker build -t etl-spark-mysql-pipeline .  
   ```  

4. **Run the pipeline**:  

   ```bash  
   docker run --env-file .env etl-spark-mysql-pipeline  
   ```  

   The container will start a Spark job that reads data from MySQL, adds a `processed_at` timestamp column, serializes each row as JSON and publishes it to the specified Kafka topic.  

## Airflow Integration  

A minimal DAG skeleton is provided in `dags/etl_mysql_to_kafka.py`. To use it:  

- Copy or symlink the `dags/` directory into your Airflow `dags/` folder.  
- Ensure that Airflow has access to a Spark installation and the repository code. The DAG uses the `SparkSubmitOperator` to submit the `pyspark_etl.py` script.  
- Configure the DAG schedule and default arguments according to your environment.  

This DAG outlines the task but does not set up connections; you must ensure that the environment variables or configuration used by Spark specify the JDBC and Kafka connection details described above.  

## Structure  

- `pyspark_etl.py` – PySpark job that reads from MySQL, performs a transformation and writes to Kafka.  
- `Dockerfile` – Container recipe for packaging the PySpark job.  
- `dags/etl_mysql_to_kafka.py` – Airflow DAG skeleton.  
- `README.md` – This document with setup instructions.  

## Notes  

- The JDBC connector JAR for MySQL must be available to Spark. In the Dockerfile provided, the necessary MySQL connector is added automatically.  
- Modify the transformation logic in `pyspark_etl.py` to suit your needs; currently it only adds a `processed_at` timestamp. 
