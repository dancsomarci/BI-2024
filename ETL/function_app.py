import azure.functions as func
import logging
import pandas as pd
from io import StringIO
from db import populate_tables, get_last_date, get_past_7_days_mean_temp
from forecast.service import service_forecast
from lstm import lstm
from datetime import date as datetype

app = func.FunctionApp()


def load_csv(myblob: func.InputStream) -> pd.DataFrame:
    blob_content = myblob.read().decode("utf-8")
    data = pd.read_csv(StringIO(blob_content))
    logging.info(f"Data successfully loaded into DataFrame with shape {data.shape}")
    return data


def seed(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob"
        f"Name: {myblob.name}, Blob Size: {myblob.length} bytes"
    )

    data = load_csv(myblob)
    for row in data[["date", "max", "min", "mean", "lstm", "service"]].values:
        d, ma, mi, me, lstm, service = row
        populate_tables(d, mi, ma, me, lstm, service)
        logging.info("Inserted row")


def process(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob"
        f"Name: {myblob.name}, Blob Size: {myblob.length} bytes"
    )

    data = load_csv(myblob)
    logging.info(f"First few rows:\n{data.head()}")

    if len(data) != 1:
        logging.error("Multiple input rows!")
        return

    last_date = get_last_date()
    date = datetype.fromisoformat(data["date"][0])
    if last_date is None or (
        date > last_date
        and (date - last_date).days == 1
    ):
        service_value = service_forecast(date, date)[0]
        x = get_past_7_days_mean_temp(str(date))
        lstm_value = lstm(x)
        logging.info(f"LSTM pred: {lstm_value}")
        logging.info(f"service pred: {service_value}")
        populate_tables(str(date), float(data["min"][0]), float(data["max"][0]), float(data["mean"][0]), float(lstm_value), float(service_value))
        logging.info("Data successfully processed and stored.")

@app.blob_trigger(
    arg_name="myblob",
    path="weather-data/raw/{name}.csv",
    connection="autoprocessorstore_STORAGE",
)
def data_processor(myblob: func.InputStream):
    try:
        process(myblob)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
