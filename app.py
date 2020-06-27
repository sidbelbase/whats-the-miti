from flask import Flask, render_template, jsonify
from collections import defaultdict
from main.nepali import nepali_date
from main.english import date_today, live_time
from time import sleep
import requests

app = Flask(__name__)


def rotate_dict(old_dict, the_key):
    new_dict = defaultdict(list)
    for item in old_dict:
        for data in old_dict[item]:
            listby = data[the_key]
            count = data["count"]
            new_dict[listby].append({item: count})
    return new_dict


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
    return {"nepali_miti": nepalimiti, "date_today": datetoday, "clock_time": livetime}


@app.route("/api/provinces")
def provinces():
    provinces = requests.\
        get("https://data.nepalcorona.info/api/v1/covid/summary").\
        json()["province"]
    return rotate_dict(provinces, "province")


@app.route("/api/districts")
def districts():
    districts = requests.\
        get("https://data.nepalcorona.info/api/v1/covid/summary").\
        json()["district"]
    return rotate_dict(districts, "district")


if __name__ == "__main__":
    app.run(debug=True)
