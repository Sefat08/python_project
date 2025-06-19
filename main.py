import os
import pandas as pd

# Get the current working directory of the python file that is running
CURRENT_DIRECTORY = os.getcwd()

# We know that the data is actually in a 'data' folder. So, we create a path with the current directory and add the data string
DATA_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'data')

station_name = input('Enter the name of the station: ').strip().lower()

station_list = pd.read_csv(os.path.join(DATA_DIRECTORY, 'station_list.csv'), encoding='latin-1')
temperature_data = pd.read_csv(os.path.join(DATA_DIRECTORY, 'temperature_data.csv'), encoding='latin-1')
precipitation_data = pd.read_csv(os.path.join(DATA_DIRECTORY, 'precipitation_data.csv'), encoding='latin-1')


def get_matching_stations(station_list, station_name):
    matching_stations = []
    for index, row in station_list.iterrows():
        station = row['Stationsname'].strip().lower()
        if station_name in station:
            matching_stations.append(row)

    return matching_stations


def get_temperature(matching_stations):
    matching_rows = []
    for row in matching_stations:
        station_id = row['Stations_id']
        
        for _, t_row in temperature_data.iterrows():
            if t_row['Stations_id'] == station_id:
                matching_rows.append(t_row)
    return matching_rows

def get_precipitation(matching_stations):
    matching_rows = []
    for row in matching_stations:
        station_id = row['Stations_id']
        
        for _, p_row in precipitation_data.iterrows():
            if p_row['Stations_id'] == station_id:
                matching_rows.append(p_row)
    return matching_rows
        
matching_stations = get_matching_stations(station_list, station_name)

matching_temperatures = get_temperature(matching_stations)
matching_precipitaitons = get_precipitation(matching_stations)

print(matching_stations)
print(matching_temperatures)