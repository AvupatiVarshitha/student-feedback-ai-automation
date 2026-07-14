import json
from pathlib import Path


class SchedulerService:

    def __init__(self):
        config_path = Path("backend/config/settings.json")

        with open(config_path, "r", encoding="utf-8") as file:
            self.settings = json.load(file)

    def get_form_schedule(self):
        return (
            self.settings["schedule"]["form_date"],
            self.settings["schedule"]["form_time"]
        )


    def get_report_schedule(self):
        return (
            self.settings["schedule"]["report_date"],
            self.settings["schedule"]["report_time"]
        )