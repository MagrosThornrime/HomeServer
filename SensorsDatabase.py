import csv


SENSORS_FILE = "data/sensors.csv"
MAX_ENTRIES = 100

SensorEntry = tuple[int, float, float]

def get_sensors_data() -> list[SensorEntry]:
    sensors_data = []
    try:
        with open(SENSORS_FILE, "r") as csv_file:
            sensors_reader = csv.reader(csv_file, delimiter=";")
            for sensor, temperature, humidity in sensors_reader:
                sensors_data.append((sensor, temperature, humidity))
    except FileNotFoundError:
        open(SENSORS_FILE, "w").close()
    finally:
        return sensors_data
    
def add_sensors_entry(sensors_data: list[SensorEntry], sensor: int,
                      temperature: float, humidity: float):
    sensors_data.append((sensor, temperature, humidity))
    if len(sensors_data) > MAX_ENTRIES:
        del sensors_data[0]
    print(sensors_data)
    with open(SENSORS_FILE, "w", newline="") as csv_file:
        sensors_writer = csv.writer(csv_file, delimiter=";")
        sensors_writer.writerows(sensors_data)
