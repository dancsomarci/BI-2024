import pyodbc
import os
import datetime


# Database connection setup
def get_connection():
    """Establishes a connection to the Azure SQL database."""
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={os.getenv('SERVER')};"
        f"DATABASE={os.getenv('DATABASE')};"
        f"UID={os.getenv('UID')};"
        f"PWD={os.getenv('PWD')};"
    )
    return connection


# Function to insert into Temperature table
def insert_temperature(min_temp, max_temp, mean_temp):
    """Inserts a record into the Temperature table."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO Temperature ( min, max, mean)
        VALUES (?, ?, ?);
    """,
        min_temp,
        max_temp,
        mean_temp,
    )
    connection.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    temperature_id = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return temperature_id


# Function to insert into Forecast table
def insert_forecast(lstm, service):
    """Inserts a record into the Forecast table."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO Forecast (lstm, service)
        VALUES (?, ?);
    """,
        lstm,
        service,
    )
    connection.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    forecast_id = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return forecast_id


# Function to insert into Days
def insert_days(date, temperature_id, forecast_id):
    """Inserts a record into the Days."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO Days (date, temperature_id, forecast_id)
        VALUES (?, ?, ?);
    """,
        date,
        temperature_id,
        forecast_id,
    )
    connection.commit()
    cursor.close()
    connection.close()


# Combined function to populate all tables
def populate_tables(date, min_temp, max_temp, mean_temp, lstm, service):
    """Populates the Temperature, Forecast, and FactTable tables."""
    temperature_id = insert_temperature(min_temp, max_temp, mean_temp)
    forecast_id = insert_forecast(lstm, service)
    insert_days(date, temperature_id, forecast_id)
    print("Data successfully inserted into all tables.")


def get_last_date():
    """Fetches the last date from the Days table."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT MAX(date) 
        FROM Days;
        """
    )
    last_date = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return last_date


def get_past_7_days_mean_temp(given_date):
    connection = get_connection()
    cursor = connection.cursor()

    # Convert given_date to datetime for calculation
    given_date_dt = datetime.datetime.strptime(given_date, "%Y-%m-%d")
    past_7_days_dt = given_date_dt - datetime.timedelta(days=6)
    past_7_days = past_7_days_dt.strftime("%Y-%m-%d")

    cursor.execute(
        """
        SELECT d.date, t.mean
        FROM Days d
        JOIN Temperature t ON d.temperature_id = t.id
        WHERE d.date BETWEEN ? AND ?
        ORDER BY d.date ASC;
        """,
        past_7_days,
        given_date,
    )

    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return [round(x[1], 2) for x in results]
