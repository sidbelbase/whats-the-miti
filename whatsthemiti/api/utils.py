from collections import defaultdict
import requests


def rotate_dict(old_dict, the_key):
    new_dict = defaultdict(dict)
    for item in old_dict:
        for data in old_dict[item]:
            listby = data[the_key]
            count = data["count"]
            new_dict[listby].update({item: count})
    return new_dict


def dict_merger(first_dict, second_dict):
    merger = defaultdict(dict)
    for data in (first_dict, second_dict):
        for key, val in data.items():
            merger[key].update(val)
    return merger


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
