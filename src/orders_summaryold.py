# Databricks notebook source
# MAGIC %md
# MAGIC # Orders summary
# MAGIC Builds total order amounts per customer into `<catalog>.sales.orders_summary`.

# COMMAND ----------

dbutils.widgets.text("catalog", "orders_dev")
catalog = dbutils.widgets.get("catalog")

# COMMAND ----------

from orders.transforms import summarize_orders, invalid_rows

# Sample data; later you'd use spark.table(...) to read a real table
orders = spark.createDataFrame(
    [(1, "Acme", 120.00, "SHIPPED"), (2, "Acme", 80.50, "SHIPPED"),
     (3, "Globex", 45.25, "CANCELLED"), (4, "Globex", 300.00, "SHIPPED")],
    "order_id INT, customer STRING, amount DOUBLE, status STRING",
)

# COMMAND ----------

# Data-quality gate: stop the job rather than publish bad numbers
bad = invalid_rows(orders)
if bad.count() > 0:
    display(bad)
    raise ValueError(f"{bad.count()} invalid order rows; fix the source data")

# COMMAND ----------

summary = summarize_orders(orders)
summary.write.mode("overwrite").saveAsTable(f"{catalog}.sales.orders_summary")
display(summary)