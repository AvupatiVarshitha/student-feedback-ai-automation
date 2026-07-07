import json
from datetime import datetime

from backend.services.data_processor import DataProcessor
from backend.services.ollama_service import analyze_feedback


class ReportBuilder:

    def __init__(self, feedback):

        self.feedback = feedback
        self.processor = DataProcessor(feedback)

    def build_report(self):

        summary = self.processor.build_summary()

        prompt = f"""
You are an Education Quality Analyst.

Analyze the following weekly feedback summary.

Weekly Feedback Summary

{json.dumps(summary, indent=4)}

Generate a JSON report with the following sections:

1. Overall Sentiment
2. Key Strengths
3. Major Concerns
4. Top Learning Topics
5. Common Challenges
6. Improvement Suggestions
7. Action Items
8. Overall Quality Score (Out of 100)

Return ONLY valid JSON.
"""

        ai_report = analyze_feedback(prompt)

        try:
            ai_report = ai_report.replace("```json", "").replace("```", "").strip()
            ai_report = json.loads(ai_report)
        except:
            pass

        report = {

            "generated_at":
                datetime.now().strftime("%d-%m-%Y %H:%M"),

            "statistics":
                summary,

            "ai_analysis":
                ai_report

        }

        return report