import os
import pandas as pd

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

station_name = input("Enter the name of the station: ").strip().lower()

station_list = pd.read_csv(
    os.path.join(DATA_DIRECTORY, "station_list.csv"), encoding="latin-1"
)
temperature_data = pd.read_csv(
    os.path.join(DATA_DIRECTORY, "temperature_data.csv"), encoding="latin-1"
)
precipitation_data = pd.read_csv(
    os.path.join(DATA_DIRECTORY, "precipitation_data.csv"), encoding="latin-1"
)


def get_matching_stations(station_list, station_name):
    matching_stations = []
    for index, row in station_list.iterrows():
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


matching_stations = get_matching_stations(station_list, station_name)

matching_temperatures = get_temperature(matching_stations)
matching_precipitaitons = get_precipitation(matching_stations)

results = {}

for row in matching_stations:
    data = {
        "station_name": row["Stationsname"].strip(),
        "bundesland": row["Bundesland"].strip(),
    }
    results[row["Stations_id"]] = data

for row in matching_temperatures:
    for column, value in row.items():
        if column == "Jahr":
            results[row["Stations_id"]]["average_temperature"] = row["Jahr"]
        else:
            # TODO: Do manually
            pass


for row in matching_temperatures:
    for column, value in row.items():
        if column == "Jahr":
            # The temperature is already averaged in "Jahr" column
            results[row["Stations_id"]]["average_temperature"] = value
            print(value)
        else:
            # Calculate manually
            pass

for row in matching_precipitaitons:
    for column, value in row.items():
        if column == "Jahr":
            # We add a new column, take the total precipitaiton and divide it by 12
            results[row["Stations_id"]]["average_precipitation"] = round(
                row["Jahr"] / 12, 2
            )
        else:
            # Calculate manually
            pass

for index, (key, value) in enumerate(results.items(), start=1):
    print(
        f"{index}. Station: {value.get('station_name', 'N/A')}, "
        f"State: {value.get('bundesland', 'N/A')}, "
        f"Average Temperature: {value.get('average_temperature', 'N/A')}, "
        f"Average Precipitation: {value.get('average_precipitation', 'N/A')}"
    )
