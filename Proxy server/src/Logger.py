
import csv
import os
import datetime
from Config import LOG_FILE

class Logger:
    HEADERS = ["Timestamp", "Client_IP", "Method", "URL", "Status"]

    @staticmethod
    def init():
        if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
            with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(Logger.HEADERS)

    @staticmethod
    def log(ip, method, url, status):
        try:
            Logger.init()
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([time, ip, method, url, status])
        except Exception:
            pass
