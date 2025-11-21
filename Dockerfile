# Use Bitnami's Spark base image
FROM bitnami/spark:3.5.0

USER root

# Install required Python packages
RUN pip install kafka-python mysql-connector-python

# Copy pipeline code into image
WORKDIR /opt/pipeline
COPY pyspark_etl.py .

# Default command: run the PySpark job with Kafka package
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "/opt/pipeline/pyspark_etl.py"]
