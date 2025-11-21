from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp


def main():
    # Initialize Spark session with required packages for MySQL and Kafka
    spark = (
        SparkSession.builder.appName("etl_mysql_to_kafka")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,mysql:mysql-connector-java:8.0.29",
        )
        .getOrCreate()
    )

    # JDBC connection details
    jdbc_url = "jdbc:mysql://<MYSQL_HOST>:<MYSQL_PORT>/<DATABASE>"
    connection_properties = {
        "user": "<MYSQL_USER>",
        "password": "<MYSQL_PASSWORD>",
        "driver": "com.mysql.cj.jdbc.Driver",
    }

    # Read data from MySQL table
    df = spark.read.jdbc(url=jdbc_url, table="<TABLE_NAME>", properties=connection_properties)

    # Small transformation: add processing timestamp
    transformed_df = df.withColumn("processed_at", current_timestamp())

    # Write records to Kafka; convert rows to JSON strings
    transformed_df.selectExpr("to_json(struct(*)) AS value").write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "<KAFKA_BOOTSTRAP_SERVERS>") \
        .option("topic", "<KAFKA_TOPIC>") \
        .save()

    spark.stop()


if __name__ == "__main__":
    main()
