import json
from pathlib import Path


class SchedulerService:

    def __init__(self):
        config_path = Path("backend/config/settings.json")

        with open(config_path, "r", encoding="utf-8") as file:
            self.settings = json.load(file)

    def get_send_schedule(self):
        return self.settings["schedule"]["send_day"], \
               self.settings["schedule"]["send_time"]

    def get_analysis_schedule(self):
        return self.settings["schedule"]["analysis_day"], \
               self.settings["schedule"]["analysis_time"]

    def get_report_schedule(self):
        return self.settings["schedule"]["report_day"], \
               self.settings["schedule"]["report_time"]