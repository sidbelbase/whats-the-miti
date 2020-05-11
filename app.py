from flask import Flask, render_template, jsonify
from main.nepali import nepali_date
from main.english import date_today, live_time
from time import sleep

app = Flask(__name__)


@app.route("/")
def show_date():
    nepalimiti = nepali_date()
    datetoday = date_today()
    livetime = live_time()
    title = nepalimiti
    return render_template(
        "base.html",
        live_time=livetime,
        date_today=datetoday,
        nepali_miti=nepalimiti,
        title=title,
    )


@app.route("/api")
def nepali_miti():
    nepalimiti = nepali_date()
    datetoday = date_today()
    livetime = live_time()
    return jsonify(
        {"nepali_miti": nepalimiti, "date_today": datetoday, "clock_time": livetime}
    )


if __name__ == "__main__":
    app.run(debug=True)
