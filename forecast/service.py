from datetime import date

import requests


def service_forecast(start: date, end: date) -> float:
    """Returns predicted mean for the next day."""
    assert start <= end
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude=47.4984&longitude=19.0404&daily=temperature_2m_max,temperature_2m_min&start_date={start}&end_date={end}"
    )
    response.raise_for_status()
    data = response.json()
    max_temps = data["daily"]["temperature_2m_max"]
    min_temps = data["daily"]["temperature_2m_min"]
    forecast = [
        round(0.5 * (max_temp + min_temp), 2)
        for max_temp, min_temp in zip(max_temps, min_temps)
    ]
    return forecast
