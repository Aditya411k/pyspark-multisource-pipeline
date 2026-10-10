"""
Loads the PySpark pipeline's output (multisource_pipeline.csv,
downloaded from Colab) into your local MySQL Workbench database.

Run this AFTER you've downloaded the CSV from the Colab notebook.

pip install pandas sqlalchemy pymysql
"""

import pandas as pd
from sqlalchemy import create_engine

MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "Your_Password"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "m_db"


CSV_PATH = "multisource_pipeline.csv"


df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows from {CSV_PATH}")

engine = create_engine("mysql+pymysql://root:Your_Password@localhost:3306/m_db")
df.to_sql("fact_weather_city", engine, if_exists="replace", index=False)
print("Loaded into MySQL table: fact_weather_city")

check = pd.read_sql(
    "SELECT city, temp_c, comfort_level, heat_exposure_score "
    "FROM fact_weather_city ORDER BY heat_exposure_score DESC;",engine,
    )
print("\nValidation query result:")
print(check)
