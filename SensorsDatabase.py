import json
from datetime import datetime


SENSORS_FILE = "data/sensors.json"
MAX_ENTRIES = 100

def get_sensor_entries() -> list[dict]:
    sensor_entries = []
    try:
        with open(SENSORS_FILE, "r") as json_file:
            sensor_entries = json.load(json_file)
    except FileNotFoundError:
        open(SENSORS_FILE, "w").close()
    finally:
        return sensor_entries
    
def add_sensors_entry(sensor_entries: list[dict], sensor: str, data: dict):
    current_time = datetime.now().isoformat()
    entry = {key: value for key, value in data.items() if key != "Czujnik"}
    entry["Czujnik"] = sensor
    entry["Czas"] = current_time
    sensor_entries.append(entry)
    if len(sensor_entries) > MAX_ENTRIES:
        del sensor_entries[0]
    with open(SENSORS_FILE, "w") as json_file:
        json.dump(sensor_entries, json_file, indent=2)
