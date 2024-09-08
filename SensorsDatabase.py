import json
from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

SENSORS_FILE = "data/sensors.json"
MAX_ENTRIES = 100

class SensorError(Exception):
    pass

def trim_entries(sensor_entries: list[dict]):
    if len(sensor_entries) > MAX_ENTRIES:
        excess_entries = len(sensor_entries) - MAX_ENTRIES
        del sensor_entries[:excess_entries]
        
def get_keys(entry: dict):
    return [key for key in entry.keys() if key not in {"Czas", "Czujnik"}]

def validate(sensor_entries: list[dict]):
    used_keys = {}

    for entry in sensor_entries:        
        # check if sensor name is valid
        if "Czujnik" not in entry:
            raise SensorError("Wpis z bazy nie zawiera nazwy czujnika")
        sensor = entry["Czujnik"]
        if not isinstance(sensor, str):
            raise SensorError("Wpis z bazy posiada niepoprawną nazwę czujnika")

        # check if saved time is valid
        if "Czas" not in entry:
            raise SensorError("Wpis z bazy nie posiada daty i godziny")
        time = entry["Czas"]
        try:
            datetime.fromisoformat(time)
        except ValueError:
            raise SensorError("Wpis z bazy posiada niepoprawną datę")
        
        # check if entry is similiar to all others from the sensor
        keys = get_keys(entry)
        if sensor in used_keys and set(keys) != used_keys[sensor]:
            raise SensorError(f"Wpisy z bazy dotyczące czujników '{sensor}' mają różne parametry")
        else:
            used_keys[sensor] = set(keys)

def get_entries() -> list[dict]:
    sensor_entries = []
    try:
        with open(SENSORS_FILE, "r") as json_file:
            sensor_entries = json.load(json_file)
            validate(sensor_entries)
            trim_entries(sensor_entries)
    except FileNotFoundError:
        open(SENSORS_FILE, "w").close()
    return sensor_entries
    
def add_entry(sensor_entries: list[dict], sensor: str, data: dict):
    current_time = datetime.now().isoformat(sep=" ", timespec="minutes")
    entry = {key: float(value) for key, value in data.items() if key != "Czujnik"}
    entry["Czujnik"] = sensor
    entry["Czas"] = current_time
    sensor_entries.append(entry)
    try:
        validate(sensor_entries)
    except SensorError:
        del sensor_entries[-1]
        return
    trim_entries(sensor_entries)
    with open(SENSORS_FILE, "w") as json_file:
        json.dump(sensor_entries, json_file, indent=2)

def get_latest(sensor_entries: list[dict]) -> list[dict]:
    validate(sensor_entries)
    entries_found = {}
    for entry in sensor_entries[::-1]:
        sensor = entry["Czujnik"]
        if sensor not in entries_found:
            entries_found[sensor] = entry
    entries_found = [value for value in entries_found.values()]
    entries_found.sort(key=lambda entry: entry["Czujnik"])
    return entries_found

def get_sensor(sensor_entries: list[dict], sensor: str) -> list[dict]:
    validate(sensor_entries)
    return [entry for entry in sensor_entries if entry["Czujnik"] == sensor]

def create_plots(sensor_entries: list[dict], sensor: str):
    validate(sensor_entries)
    measurements = {}
    for entry in sensor_entries:
        for key, value in entry.items():
            if key == "Czujnik":
                continue
            if key not in measurements:
                measurements[key] = []
            if key == "Czas":
                value = datetime.now() - datetime.fromisoformat(value)
                value = pd.Timedelta(value, unit="h") / pd.Timedelta("1 hour")
            measurements[key].append(value)
    df = pd.DataFrame(measurements)
    df.set_index("Czas", inplace=True)
    for series_name, _ in df.items():
        if series_name == "Czas":
            continue
        plot = sns.scatterplot(df[series_name])
        plot.set(xlabel="Liczba godzin od pomiaru", ylabel=series_name)
        plt.savefig(f"static/temp/{sensor}_{series_name}.png")
        plt.clf()
