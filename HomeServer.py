from flask import Flask, render_template, request

from SensorsDatabase import add_sensors_entry, get_sensor_entries

app = Flask(__name__)
sensor_entries = get_sensor_entries()

@app.route("/sensor_entry", methods=["POST"])
def add_sensor_data():
    try:
        sensor = request.form["Czujnik"]
    except KeyError:
        print("Sensor's name not found")
        return ""
    data = request.form.to_dict()
    add_sensors_entry(sensor_entries, sensor, data)
    return ""
    
@app.route("/sensors")
def sensors():
    return render_template("sensors.html")

@app.route("/guide")
def guide():
    return render_template("guide.html")

@app.route("/")
def homepage():
    return render_template("main.html")

if __name__ == "__main__":
    app.run()