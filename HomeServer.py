from flask import Flask, render_template, request

import SensorsDatabase as sensors_db

app = Flask(__name__)
sensor_entries = sensors_db.get_entries()

@app.route("/sensor_entry", methods=["POST"])
def add_sensor_data():
    try:
        sensor = request.form["Czujnik"]
    except KeyError:
        print("Sensor's name not found")
        return ""
    data = request.form.to_dict()
    sensors_db.add_entry(sensor_entries, sensor, data)
    return ""
    
@app.route("/sensors")
def sensors():
    latest_entries = sensors_db.get_latest(sensor_entries)
    return render_template("sensors.html", sensor_entries=latest_entries)

@app.route("/sensors/<sensor>")
def sensor_detailed(sensor: str):
    # TODO: what if somebody uses the url but there are no entries for the sensor?
    entries = sensors_db.get_sensor(sensor_entries, sensor)
    sensors_db.create_plots(entries, sensor)
    keys = sensors_db.get_keys(sensor_entries)
    return render_template("sensors_detailed.html", sensor=sensor, keys=keys)

@app.route("/guide")
def guide():
    return render_template("guide.html")

@app.route("/")
def homepage():
    return render_template("main.html")

if __name__ == "__main__":
    app.run()