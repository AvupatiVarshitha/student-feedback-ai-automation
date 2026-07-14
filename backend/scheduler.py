from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from backend.automation_runner import AutomationRunner
from backend.services.scheduler_service import SchedulerService

scheduler = BackgroundScheduler()

runner = AutomationRunner()

def load_schedule():

    scheduler.remove_all_jobs()

    service = SchedulerService()

    form_date, form_time = service.get_form_schedule()
    report_date, report_time = service.get_report_schedule()

    form_datetime = datetime.strptime(
        f"{form_date} {form_time}",
        "%Y-%m-%d %H:%M"
    )

    report_datetime = datetime.strptime(
        f"{report_date} {report_time}",
        "%Y-%m-%d %H:%M"
    )

    # Send Google Forms
    scheduler.add_job(
        runner.send_forms,
        trigger="date",
        run_date=form_datetime,
        id="form_job"
    )

    # Run complete automation
    scheduler.add_job(
        runner.run_report_pipeline,
        trigger="date",
        run_date=report_datetime,
        id="report_job"
    )

    print("✅ Schedule Loaded")
def start_scheduler():

    load_schedule()

    if not scheduler.running:
        scheduler.start()

    print("🚀 Automation Scheduler Started")