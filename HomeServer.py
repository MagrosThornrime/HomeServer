from flask import Flask, render_template, request

from SensorsDatabase import add_sensors_entry, get_sensors_data

app = Flask(__name__)
sensors_data = get_sensors_data()

@app.route("/sensor_entry", methods=["GET"])
def add_sensor_data():
    sensor = int(request.args.get("sensor"))
    temperature = float(request.args.get("temperature"))
    humidity = float(request.args.get("humidity"))
    add_sensors_entry(sensors_data, sensor, temperature, humidity)
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