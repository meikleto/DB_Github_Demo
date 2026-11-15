from pyspark.sql import DataFrame, functions as F


def summarize_orders(orders: DataFrame) -> DataFrame:
    """Total amount and order count per customer, ignoring cancelled orders."""
    return (
        orders.filter(F.col("status") != "CANCELLED")
        .groupBy("customer")
        .agg(
            F.round(F.sum("amount"), 2).alias("total_amount"),
            F.count("*").alias("order_count"),
        )
        .orderBy("customer")
    )


def invalid_rows(orders: DataFrame) -> DataFrame:
    """Rows that break the data rules: no customer, or a negative amount."""
    return orders.filter(F.col("customer").isNull() | (F.col("amount") < 0))