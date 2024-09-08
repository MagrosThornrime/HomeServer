from sqlite3 import DatabaseError
from flask import Flask, render_template, request

import SensorsDatabase as sensors_db

app = Flask(__name__)

@app.route("/sensor_entry", methods=["POST"])
def add_sensor_data():
    try:
        sensor = request.form["Czujnik"]
    except KeyError:
        return render_template("error.html", error_info="Żądanie nie zawiera nazwy czujnika")
    sensor_entries = sensors_db.get_entries()
    data = request.form.to_dict()
    sensors_db.add_entry(sensor_entries, sensor, data)
    return ""
    
@app.route("/sensors")
def sensors():
    try:
        sensor_entries = sensors_db.get_entries()
    except sensors_db.SensorError as error:
        return render_template("error.html", error_info=str(error))
    latest_entries = sensors_db.get_latest(sensor_entries)
    return render_template("sensors.html", sensor_entries=latest_entries)

@app.route("/sensors/<sensor>")
def sensor_detailed(sensor: str):
    try:
        sensor_entries = sensors_db.get_entries()
    except sensors_db.SensorError as error:
        return render_template("error.html", error_info=str(error))
    entries = sensors_db.get_sensor(sensor_entries, sensor)
    if not entries:
        return render_template("error.html", error_info="Baza danych nie zawiera wpisów z tego czujnika")
    sensors_db.create_plots(entries, sensor)
    keys = sensors_db.get_keys(entries[0])
    return render_template("sensors_detailed.html", sensor=sensor, keys=keys)

@app.route("/guide")
def guide():
    return render_template("guide.html")

@app.route("/")
def homepage():
    return render_template("main.html")

if __name__ == "__main__":
    app.run()