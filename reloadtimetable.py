import csv
import pickle
from datetime import datetime, time


def create_cache():
    pickle.dump(files, open("./cache/timeschedule.tmp", "wb"))


def single_load():
    return files


def convert_timer():
    for key in timetable.keys():
        item = timetable[key]
        timetable[key] = (time_(item[0]), time_(item[1]))
    return timetable


def time_(s):
    return datetime.strptime(s, time_format).time()


# Define the time format as "%H:%M"
time_format = "%H:%M"

file = {}
with open('timetable.csv', 'r', newline='') as csvfile:
    timetable = csv.DictReader(csvfile)
    i = 0
    for row in timetable:
        file[i] = row
        i += 1

timetable = {
    "P1": ("8:00", "8:40"),
    "P2": ("8:45", "9:25"),
    "Break": ("9:25", "10:05"),
    "P3": ("10:05", "10:45"),
    "P4": ("10:50", "11:30"),
    "P5": ("11:35", "12:15"),
    "Launch": ("12:15", "12:55"),
    "Launch Period": ("12:55", "13:35"),
    "P6": ("13:40", "14:20"),
    "P7": ("14:25", "15:05"),
    "P8": ("15:10", "15:50"),
    "P9": ("15:55", "16:35"),
    "P10": ("16:40", "17:20"),
}

files = {
    "schedule": file,
    "time": convert_timer()
}

if __name__ == '__main__':
    create_cache()
    print(files)
