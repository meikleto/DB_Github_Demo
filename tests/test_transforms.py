from orders.transforms import invalid_rows, summarize_orders


def by_customer(df):
    return {r["customer"]: r.asDict() for r in df.collect()}


def test_cancelled_orders_are_ignored(orders):
    result = by_customer(summarize_orders(orders))
    assert result["Globex"]["total_amount"] == 300.00
    assert result["Globex"]["order_count"] == 1


def test_totals_per_customer(orders):
    result = by_customer(summarize_orders(orders))
    assert result["Acme"]["total_amount"] == 200.50
    assert result["Acme"]["order_count"] == 2


def test_amounts_are_rounded_to_cents(spark):
    df = spark.createDataFrame(
        [("Initech", 0.1, "SHIPPED"), ("Initech", 0.2, "SHIPPED")],
        "customer STRING, amount DOUBLE, status STRING",
    )
    assert summarize_orders(df).first()["total_amount"] == 0.3


def test_output_columns_are_stable(orders):
    assert summarize_orders(orders).columns == ["customer", "total_amount", "order_count"]


def test_empty_input_gives_empty_output(spark, orders):
    empty = spark.createDataFrame([], orders.schema)
    assert summarize_orders(empty).count() == 0


def test_invalid_rows_are_flagged(spark):
    df = spark.createDataFrame(
        [(1, "Acme", 10.0, "SHIPPED"), (2, None, 5.0, "SHIPPED"), (3, "Globex", -1.0, "SHIPPED")],
        "order_id INT, customer STRING, amount DOUBLE, status STRING",
    )
    assert sorted(r["order_id"] for r in invalid_rows(df).collect()) == [2, 3]
