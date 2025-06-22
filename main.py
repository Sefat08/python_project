import os
import pprint
from numpy import average
import pandas as pd
import difflib

from pandas._libs.lib import count_level_2d

# Get the current working directory of the python file that is running
CURRENT_DIRECTORY = os.getcwd()

# We know that the data is actually in a 'data' folder. So, we create a path with the current directory and add the data string
DATA_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "data")

MONTHS_LIST = [
    "Jan",
    "Feb",
    "März",
    "Apr",
    "Mai",
    "Jun",
    "Jul",
    "Aug",
    "Sept",
    "Okt",
    "Nov",
    "Dez",
]


print("Loading dataset")

station_list = pd.read_csv(
    os.path.join(DATA_DIRECTORY, "station_list.csv"), encoding="utf-8"
)
temperature_data = pd.read_csv(
    os.path.join(DATA_DIRECTORY, "temperature_data.csv"), encoding="utf-8"
)
precipitation_data = pd.read_csv(
    os.path.join(DATA_DIRECTORY, "precipitation_data.csv"), encoding="utf-8"
)


def get_matching_stations(station_list, station_name):
    matching_stations = []
    for _, row in station_list.iterrows():
        station = row["Stationsname"].strip().lower()
        if station_name in station:
            matching_stations.append(row)

    return matching_stations


def get_temperature(matching_stations):
    matching_rows = []
    for row in matching_stations:
        station_id = row["Stations_id"]

        for _, t_row in temperature_data.iterrows():
            if t_row["Stations_id"] == station_id:
                matching_rows.append(t_row)
    return matching_rows


def get_precipitation(matching_stations):
    matching_rows = []
    for row in matching_stations:
        station_id = row["Stations_id"]

        for _, p_row in precipitation_data.iterrows():
            if p_row["Stations_id"] == station_id:
                matching_rows.append(p_row)
    return matching_rows


def determine_output():
    station_name = input("Enter the name of the station: ").strip().lower()

    matching_stations = get_matching_stations(station_list, station_name)
    matching_temperatures = get_temperature(matching_stations)
    matching_precipitaitons = get_precipitation(matching_stations)

    results = {}

    # Create a dictionary to populate and output relevant data
    for row in matching_stations:
        data = {
            "station_name": row["Stationsname"].strip(),
            "bundesland": row["Bundesland"].strip(),
        }

        results[row["Stations_id"]] = data

    for row in matching_temperatures:
        accumulated_temperature = 0
        if row["Stations_id"] in results:
            for column, value in row.items():
                match = difflib.get_close_matches(column, MONTHS_LIST, n=1, cutoff=0.6)

                if match:
                    accumulated_temperature += float(value)

        average_temperature = round(accumulated_temperature / 12, 2)
        results[row["Stations_id"]]["average_temperature"] = average_temperature

    for row in matching_precipitaitons:
        accumulated_precipitation = 0
        if row["Stations_id"] in results:
            for column, value in row.items():
                match = difflib.get_close_matches(column, MONTHS_LIST, n=1, cutoff=0.6)

                if match:
                    accumulated_precipitation += float(value)

        average_precipitation = round(accumulated_precipitation / 12, 2)
        results[row["Stations_id"]]["average_precipitation"] = average_precipitation

    for index, (key, value) in enumerate(results.items(), start=1):
        print(
            f"{index}. Station_ID: {key}\n"
            f"   Station: {value.get('station_name', 'N/A')}\n"
            f"   State: {value.get('bundesland', 'N/A')}\n"
            f"   Average Temperature: {value.get('average_temperature', 'N/A')}\n"
            f"   Average Precipitation: {value.get('average_precipitation', 'N/A')}\n"
        )


while True:
    determine_output()
