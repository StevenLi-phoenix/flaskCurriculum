from flask import Flask, render_template, request
import pickle
from os.path import exists, join
from datetime import datetime, time, timedelta, date


# todo: Add a recording system for bugs report


def loadTimeSchedule():
    if not exists(join("cache", "timeschedule.tmp")):
        import reloadtimetable
        return reloadtimetable.single_load()
    return pickle.load(open(join("cache", "timeschedule.tmp"), "rb"))


file = loadTimeSchedule()
schedule, times = file["schedule"], file["time"]
order = ["P1", "P2", "Break", "P3", "P4", "P5", "Launch", "launch period", "P6", "P7", "P8", "P9", "P10"]
app = Flask(__name__)


@app.route('/')
def index_html():
    return render_template("index.html")


@app.route('/api/school/current/classperiod')
def getCurrentPeriod():
    now = datetime.now().time()
    # now = time(10, 20)
    try:
        for period, timesitem in times.items():
            start_time, end_time = timesitem
            if start_time <= now < end_time:
                return period
        else:
            return -1
    except TypeError:
        return -1


def getNextClassPeriod(sch):
    now = datetime.now().time()
    try:
        period = "P0"
        for period, timesitem in times.items():
            start_time, end_time = timesitem
            if now < start_time and not sch.get(period):
                continue
            else:
                break
        return period
    except TypeError as e:
        raise e


def getTodaySchduel(sch):
    start, end = None, None
    for period in order:
        p = sch.get(period)
        if p:
            start = period
            break
    for period in order[::-1]:
        p = sch.get(period)
        if p:
            end = period
            break
    return start, end


def duration(start, end):
    return datetime.combine(date.today(), end) - datetime.combine(date.today(), start)


@app.route('/api/school/current/timeprogress')
def getCurrentTimeProgress():
    """
    Get current time progress
    if we have class now it will return:
        {"period": period,"schedule": today_schedule.get(period),"timePeriodPassed": timePeriodPassed,"timePeriodTotal": timePeriodTotal}
    else it will return:
        {"period":None}

    :return: {"period": period,
                ["schedule": today_schedule.get(period),]
                ["timePeriodPassed": timePeriodPassed,]
                ["timePeriodTotal": timePeriodTotal]}
                The key "period" could be None,
    """
    today_schedule = schedule.get(datetime.now().weekday())
    period = getCurrentPeriod()
    timeperiodpercentage = times.get(period)
    if timeperiodpercentage:
        now = datetime.now().time()
        timePeriodPassed = duration(timeperiodpercentage[0], now).seconds
        # print(timeperiodpercentage, now, timePeriodPassed)
        timePeriodTotal = duration(timeperiodpercentage[0], timeperiodpercentage[1]).seconds
        return {"period": period,
                "schedule": today_schedule.get(period),
                "timePeriodPassed": timePeriodPassed,
                "timePeriodTotal": timePeriodTotal}
    else:
        return {"period": timeperiodpercentage}


@app.route('/api/school/current/day')
def getCurrentDayProgress():
    today_schedule = schedule.get(datetime.now().weekday())
    period = getNextClassPeriod(today_schedule)
    start, end = getTodaySchduel(today_schedule)
    timeperiodpercentage = times.get(period)
    if start:
        now = datetime.now().time()
        seconds_of_today = duration(times.get(start)[0], times.get(end)[1]).seconds
        seconds_passed_of_today = duration(times.get(start)[0], now).seconds if times.get(start)[0] < now else -1
        seconds_to_next_class = duration(datetime.now().time(), timeperiodpercentage[0]).seconds
        return {"seconds_to_next_class": seconds_to_next_class,
                "seconds_of_today": seconds_of_today,
                "seconds_passed_of_today": seconds_passed_of_today,
                "next_class": today_schedule.get(period),}
    else:
        return {}


@app.route('/bugs', methods=["GET"])
def renderPageForReportBugs():
    return render_template("report.html")


@app.route('/bugs', methods=["POST"])
def reportBugs():
    data = request.get_json()
    print(data)
    return {}


@app.errorhandler(404)
def render_404error_page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(port=2000)
