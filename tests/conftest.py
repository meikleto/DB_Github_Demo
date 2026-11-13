import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("unit-tests")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    yield session
    session.stop()


@pytest.fixture
def orders(spark):
    return spark.createDataFrame(
        [(1, "Acme", 120.00, "SHIPPED"), (2, "Acme", 80.50, "SHIPPED"),
         (3, "Globex", 45.25, "CANCELLED"), (4, "Globex", 300.00, "SHIPPED")],
        "order_id INT, customer STRING, amount DOUBLE, status STRING",
    )
