# PySpark Multi-Source Pipeline (OpenWeather API + City Reference Data)

## Overview
A batch data pipeline built with PySpark in Google Colab. It combines two
different sources, live weather data from the OpenWeather API and a static
city reference CSV, then cleans, joins and transforms them into one
analysis-ready table that is loaded into MySQL.

## Tech Stack
Python, PySpark (Spark SQL), Google Colab, OpenWeather API, pandas,
SQLAlchemy, MySQL

## Data Sources
| Source | Type | Content |
|---|---|---|
| OpenWeather API | Live API (JSON) | Current temperature, feels-like, humidity, wind speed and condition for 10 Indian cities |
| `city_reference.csv` | Static CSV | Region, approximate population (millions) and area (km²) per city |

Cities: Indore, Delhi, Mumbai, Bengaluru, Gurugram, Jalandhar, Hyderabad,
Chennai, Pune, Kolkata

## Pipeline Steps
1. **Extract:** called the OpenWeather API for each city with a retry
   function that handles rate limiting (HTTP 429), then checked for missing values.
2. **Load into Spark:** created a Spark DataFrame from the API data using an
   explicit schema, and read the city reference CSV.
3. **Clean:** converted the Unix timestamp to a proper timestamp, removed
   duplicate cities, filled missing wind speed with 0 and trimmed city names.
4. **Join:** inner join of weather and city data on `city` (10 rows in, 10 rows out).
5. **Transform:** created new columns:
   - `density_per_sq_km`: population density
   - `comfort_level`: Cold / Cool / Pleasant / Hot / Very Hot based on temperature
   - `heat_exposure_score`: temperature combined with population density
6. **Analyze:** Spark SQL queries to rank cities by heat exposure score, count
   cities per comfort level and compute average temperature per region.
7. **Load:** exported the result to CSV and loaded it into the MySQL table
   `fact_weather_city` using a small Python script.

## Project Files
- `multisource_pipeline.ipynb`: PySpark pipeline notebook (runs in Google Colab)
- `load_pyspark_output_to_mysql.py`: loads the output CSV into MySQL and runs a validation query
- `city_reference.csv`: static city reference data
- `multisource_pipeline.csv`: sample pipeline output

## How to Run
1. Get a free API key from [OpenWeather](https://openweathermap.org/api)
2. Open the notebook in Google Colab and set `API_KEY` in the config cell
3. Run all cells and upload `city_reference.csv` when asked
4. Run the last cell to download `multisource_pipeline.csv`
5. Update the MySQL username and password in `load_pyspark_output_to_mysql.py`
6. Install the requirements and run the script:
```
   pip install pandas sqlalchemy pymysql
   python load_pyspark_output_to_mysql.py
```

## Notes
- Weather data is a live snapshot, so values will differ each time the pipeline runs.
- The API key and database password are not stored in this repository.
