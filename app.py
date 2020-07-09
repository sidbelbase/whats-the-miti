from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
from collections import defaultdict
from main.nepali import nepali_date
from main.english import date_today, live_time
from time import sleep
import requests

app = Flask(__name__)
cors = CORS(app)

app.config["CORS_HEADERS"] = "Content-Type"


def rotate_dict(old_dict, the_key):
    new_dict = defaultdict(dict)
    for item in old_dict:
        for data in old_dict[item]:
            listby = data[the_key]
            count = data["count"]
            new_dict[listby].update({item: count})
    return new_dict


def first_filtered_districts(province_id):
    first_half_districts = defaultdict(dict)
    district_lists = requests.get(
        "https://data.nepalcorona.info/api/v1/districts"
    ).json()
    for district in district_lists:
        if province_id == "all":
            district_id = district["id"]
            first_half_districts[district_id].update(
                {
                    "id": district["id"],
                    "name": district["title_en"],
                    "coords": district["centroid"]["coordinates"],
                }
            )
        else:
            if district["province"] == int(province_id):
                district_id = district["id"]
                first_half_districts[district_id].update(
                    {"id": district["id"], "name": district["title_en"]}
                )
    return first_half_districts


def second_filtered_districts(province_id):
    district_ids = []
    district_lists = requests.get(
        "https://data.nepalcorona.info/api/v1/districts"
    ).json()

    for district in district_lists:
        if province_id == "all":
            district_id = district["id"]
            district_ids.append(district_id)
        else:
            if district["province"] == int(province_id):
                district_id = district["id"]
                district_ids.append(district_id)

    second_half_districts = defaultdict(dict)
    districts = requests.get(
        "https://data.nepalcorona.info/api/v1/covid/summary"
    ).json()["district"]
    improved_districts = rotate_dict(districts, "district")

    for _id, district in improved_districts.items():
        if _id in district_ids:
            second_half_districts.update({_id: district})
    return second_half_districts


def dict_merger(first_dict, second_dict):
    merger = defaultdict(dict)
    for data in (first_dict, second_dict):
        for key, val in data.items():
            merger[key].update(val)
    return merger


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


@app.route("/api/nepalimiti")
@cross_origin()
def nepali_miti():
    nepalimiti = nepali_date()
    datetoday = date_today()
    livetime = live_time()
    return {"nepali_miti": nepalimiti, "date_today": datetoday, "clock_time": livetime}


@app.route("/api/covid/provinces")
@cross_origin()
def provinces():
    improved = {}
    provinces = requests.get(
        "https://covidapi.mohp.gov.np/api/v1/stats/?province=all"
    ).json()
    for province in provinces:
        improved.update(
            {
                province["province_id"]: {
                    "name": province["province_name"],
                    "cases": province["total_positive"],
                    "deaths": province["total_death"],
                    "recovered": province["total_recovered"],
                }
            }
        )
    return improved


@app.route("/api/covid/province/<int:id>")
@cross_origin()
def province_details(id):
    improved = {}
    provinces = requests.get(
        f"https://covidapi.mohp.gov.np/api/v1/stats/?province={id}"
    ).json()
    for province in provinces:
        improved.update(
            {
                "id": province["province_id"],
                "name": province["province_name"],
                "samples": province["total_samples_collected"],
                "tested": province["total_tested"],
                "negative": province["total_negative"],
                "isolated": province["total_in_isolation"],
                "cases": province["total_positive"],
                "deaths": province["total_death"],
                "recovered": province["total_recovered"],
                "quarantined": province["in_quarantine"],
                "beds": province["num_of_bed"],
                "isolation_beds": province["num_of_isolation_bed"],
                "last_updated": province["update_date"],
                "occupied_isolation_beds": province["occupied_isolation_bed"],
                "occupied_ventilators": province["occupied_ventilators"],
            }
        )
    return improved


@app.route("/api/covid/districts/<string:any_params>")
@cross_origin()
def districts(any_params):
    return dict_merger(
        first_filtered_districts(any_params), second_filtered_districts(any_params)
    )


if __name__ == "__main__":
    app.run(debug=True)
