from flask import Flask, render_template
from main.nepali import nepali_date
from main.english import date_today, live_time
from time import sleep

app = Flask(__name__)


@app.route("/")
def show_date():
    nepali_mahina = nepali_date()[0]
    nepali_din = nepali_date()[1]
    datetoday = date_today()
    livetime = live_time()
    title = nepali_mahina + " " + nepali_din + " : " + datetoday
    return render_template(
        "base.html",
        live_time=livetime,
        date_today=datetoday,
        nepali_mahina=nepali_mahina,
        nepali_din=nepali_din,
        title=title,
    )


if __name__ == "__main__":
    app.run(debug=True)
