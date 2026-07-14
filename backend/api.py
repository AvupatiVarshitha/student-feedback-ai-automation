from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
from backend.scheduler import start_scheduler, load_schedule

BASE_DIR = os.path.dirname(__file__)
BATCH_FILE = os.path.join(BASE_DIR, "data", "batches.json")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
SETTINGS_FILE = os.path.join(
    BASE_DIR,
    "config",
    "settings.json"
)

class Batch(BaseModel):
    name: str
    telegram_chat_id: str
    google_form: str
    google_sheet: str
    email: str
    active: bool

app = FastAPI(
    title="Student Tribe Feedback AI",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():

    start_scheduler()

# Allow React frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Later we'll restrict this after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Student Tribe Feedback AI Backend Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }

@app.get("/batches")
def get_batches():

    with open(BATCH_FILE, "r") as file:
        batches = json.load(file)

    return batches
@app.post("/batches")
def add_batch(batch: Batch):

    with open(BATCH_FILE, "r") as file:
        batches = json.load(file)

    new_batch = batch.model_dump()

    new_batch["id"] = len(batches) + 1

    batches.append(new_batch)

    with open(BATCH_FILE, "w") as file:
        json.dump(batches, file, indent=4)

    return {
        "message": "Batch Added Successfully",
        "batch": new_batch
    }
@app.put("/batches/{batch_id}")
def update_batch(batch_id: int, batch: Batch):

    with open(BATCH_FILE, "r") as file:
        batches = json.load(file)

    updated = False

    for i in range(len(batches)):

        if batches[i]["id"] == batch_id:

            batches[i] = {
                "id": batch_id,
                **batch.model_dump()
            }

            updated = True
            break

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Batch not found"
        )

    with open(BATCH_FILE, "w") as file:
        json.dump(batches, file, indent=4)

    return {
        "message": "Batch updated successfully"
    }
@app.delete("/batches/{batch_id}")
def delete_batch(batch_id: int):

    with open(BATCH_FILE, "r") as file:
        batches = json.load(file)

    new_batches = []

    deleted = False

    for batch in batches:

        if batch["id"] == batch_id:

            deleted = True

        else:

            new_batches.append(batch)

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Batch not found"
        )

    with open(BATCH_FILE, "w") as file:

        json.dump(new_batches, file, indent=4)

    return {
        "message": "Batch deleted successfully"
    }
@app.get("/dashboard")
def dashboard():

    with open(BATCH_FILE, "r") as file:
        batches = json.load(file)

    total_batches = len(batches)

    active_batches = sum(
        1 for batch in batches
        if batch["active"]
    )

    return {

        "total_batches": total_batches,

        "active_batches": active_batches,

        "reports_generated": 0,

        "forms_sent": 0,

        "last_report": "Not Generated"

    }
@app.post("/generate-report")
def generate_report():

    try:

        print("Step 1 - Reading Google Sheets")

        from backend.services.sheets_service import get_feedback_data
        from backend.services.report_builder import ReportBuilder
        from backend.services.charts_service import ChartService
        from backend.services.pdf_service import PDFService

        feedback = get_feedback_data()

        print("Step 2 - Building Report")

        builder = ReportBuilder(feedback)

        report = builder.build_report()

        print("Step 3 - Creating Charts")

        charts = ChartService()

        for batch in report["batches"]:
            charts.generate_all_charts(
                batch["statistics"],
                batch["name"]
            )

        print("Step 4 - Generating PDF")

        pdf = PDFService()

        pdf.build_pdf(
            report,
            "backend/reports/test_report.pdf"
        )

        print("Finished Successfully")

        return {
            "success": True,
            "message": "PDF Generated Successfully!"
        }

    except Exception as e:

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@app.get("/reports")
def get_reports():

    reports = []

    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    for file in os.listdir(REPORT_FOLDER):

        if file.endswith(".pdf"):

            reports.append({

                "name": file,

                "status": "Ready",

                "generatedAt": datetime.now().strftime("%d-%b-%Y"),

                "batches": 3

            })

    return reports
@app.get("/download/{filename}")
def download_report(filename: str):

    file_path = os.path.join(REPORT_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )
@app.delete("/reports/{filename}")
def delete_report(filename: str):

    print("Requested:", filename)
    print("Folder:", REPORT_FOLDER)
    print("Files:", os.listdir(REPORT_FOLDER))

    file_path = os.path.join(REPORT_FOLDER, filename)

    print("Looking for:", file_path)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Report not found: {file_path}"
        )

    os.remove(file_path)

    return {
        "success": True,
        "message": "Report deleted successfully"
    }
@app.get("/analytics")
def analytics():

    from backend.services.sheets_service import get_feedback_data

    feedback = get_feedback_data()
    for batch in feedback.values():
        if batch:
            print(batch[0])
            break

    trainer_total = 0
    interaction_total = 0
    program_total = 0

    trainer_count = 0
    interaction_count = 0
    program_count = 0

    total_responses = 0
    top_topics = []
    challenges = []
    suggestions = []

    for batch in feedback.values():

        for row in batch:
            row = {k.strip(): v for k, v in row.items()}
 

            total_responses += 1

            topic = row.get(
                "What topics did you learn or practice last week?",
                ""
            )

            if topic:
                top_topics.append(topic)

# Challenges
            challenge = row.get(
                "Are you facing any challenges in the course? If yes, please mention.",
                ""
            )

            if challenge:
                challenges.append(challenge)

# Suggestions
            suggestion = row.get(
                "What improvements would you suggest for the course?",
            ""
            )

            if suggestion:
                suggestions.append(suggestion)

            try:
                trainer_total += float(
                    row["How would you rate the overall training and guidance provided by Rizwan sir?"]
                )
                trainer_count += 1
            except:
                pass

            try:
                interaction_total += float(
                    row["How would you rate the trainer’s interaction with students?"]
                )
                interaction_count += 1
            except:
                pass

            try:
                program_total += float(
                    row["How satisfied are you with the program team?"]
                )
                program_count += 1
            except:
                pass

    trainer_avg = round(
        trainer_total / trainer_count, 2
    ) if trainer_count else 0

    interaction_avg = round(
        interaction_total / interaction_count, 2
    ) if interaction_count else 0

    program_avg = round(
        program_total / program_count, 2
    ) if program_count else 0

    overall = round(
        (trainer_avg + interaction_avg + program_avg) / 3,
        2
    )

    return {

    "ratings": [

        {
            "metric": "Overall Rating",
            "score": overall
        },

        {
            "metric": "Trainer",
            "score": trainer_avg
        },

        {
            "metric": "Interaction",
            "score": interaction_avg
        },

        {
            "metric": "Program Team",
            "score": program_avg
        }

    ],

    "trend": [

        {
            "week": "Responses",
            "score": overall
        }

    ],

    "responses": total_responses,

    "top_topics": top_topics,

    "common_challenges": challenges,

    "suggestions": suggestions

}

SETTINGS_FILE = os.path.join(
    BASE_DIR,
    "config",
    "settings.json"
)



@app.get("/settings")
def get_settings():

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


@app.put("/settings")
def update_settings(settings: dict):

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)
    load_schedule()

    return {
        "message": "Settings Updated Successfully"
    }