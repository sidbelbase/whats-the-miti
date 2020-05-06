from datetime import datetime
from dateutil import tz


def date_today():
    current_date = datetime.now()
    now = current_date.astimezone(tz.gettz("Asia/Kathmandu"))
    return now.strftime("%B %e, %A")


def live_time():
    current_time = datetime.now()
    now = current_time.astimezone(tz.gettz("Asia/Kathmandu"))
    return now.strftime("%H.%M.%S")
