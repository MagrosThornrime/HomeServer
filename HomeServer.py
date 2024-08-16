from flask import Flask, render_template, url_for, request

app = Flask(__name__)

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