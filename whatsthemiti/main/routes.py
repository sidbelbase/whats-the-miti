from flask import Blueprint, render_template
from .nepali import nepali_date
from .english import date_today, live_time

main = Blueprint("main", __name__)


@main.route("/")
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
