from .utils import (
    dict_merger,
    rotate_dict,
    first_filtered_districts,
    second_filtered_districts,
)
from whatsthemiti.main.english import date_today, live_time
from whatsthemiti.main.nepali import nepali_date
from flask_cors import cross_origin
from flask import Blueprint
import requests

api = Blueprint("api", __name__)


@api.route("/api/nepalimiti")
@cross_origin()
def nepali_miti():
    nepalimiti = nepali_date()
    datetoday = date_today()
    livetime = live_time()
    return {"nepali_miti": nepalimiti, "date_today": datetoday, "clock_time": livetime}


@api.route("/api/covid/provinces")
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


@api.route("/api/covid/province/<int:id>")
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


@api.route("/api/covid/districts/<string:any_params>")
@cross_origin()
def districts(any_params):
    return dict_merger(
        first_filtered_districts(any_params), second_filtered_districts(any_params)
    )
