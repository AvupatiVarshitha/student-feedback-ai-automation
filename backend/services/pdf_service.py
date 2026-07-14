import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)


class PDFService:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # -------------------------------------------------
    # Heading
    # -------------------------------------------------

    def _heading(self, text):

        style = self.styles["Heading1"]

        style.alignment = TA_CENTER

        style.textColor = colors.HexColor("#0B3C5D")

        return Paragraph(text, style)

    # -------------------------------------------------
    # Section
    # -------------------------------------------------

    def _section(self, text):

        return Paragraph(
            f"<b>{text}</b>",
            self.styles["Heading2"]
        )

    # -------------------------------------------------
    # Chart
    # -------------------------------------------------

    def _add_chart(self, story, path, title):

        if os.path.exists(path):

            story.append(
                self._section(title)
            )

            story.append(
                Image(
                    path,
                    width=6.3 * inch,
                    height=3.6 * inch
                )
            )

            story.append(
                Spacer(1, 0.2 * inch)
            )

    # -------------------------------------------------
    # PDF
    # -------------------------------------------------

    def build_pdf(self, report, output_path):

        doc = SimpleDocTemplate(output_path)

        story = []

        # ------------------------------
        # Cover
        # ------------------------------

        story.append(
            self._heading(
                "Student Tribe Weekly Feedback Report"
            )
        )

        story.append(
            Paragraph(
                "<b>AI Powered Analytics Dashboard</b>",
                self.styles["Heading2"]
            )
        )

        story.append(
            Spacer(1, 0.3 * inch)
        )

        story.append(
            Paragraph(
                f"<b>Generated:</b> {report['generated_at']}",
                self.styles["Normal"]
            )
        )

        story.append(
            Spacer(1, 0.4 * inch)
        )

        # -------------------------------------------------
        # Every Batch
        # -------------------------------------------------

        for batch in report["batches"]:

            stats = batch["statistics"]

            ai = batch["ai_analysis"]

            batch_name = batch["name"]

            quality = ai.get(
                "Overall Quality Score",
                ai.get(
                    "Overall Quality Score (Out of 100)",
                    "N/A"
                )
            )

            sentiment = ai.get(
                "Overall Sentiment",
                "N/A"
            )

            story.append(
                self._heading(batch_name)
            )

            story.append(
                Spacer(1, 0.2 * inch)
            )

            table = Table(

                [

                    ["Metric", "Value"],

                    ["Responses",
                     stats["total_responses"]],

                    ["Course Satisfaction",
                     stats["course_satisfaction"]],

                    ["Trainer Rating",
                     stats["trainer_rating"]],

                    ["Program Team Rating",
                     stats["program_team_rating"]],

                    ["Quality Score",
                     quality],

                    ["Overall Sentiment",
                     sentiment]

                ],

                colWidths=[
                    3.5 * inch,
                    2.5 * inch
                ]

            )

            table.setStyle(

                TableStyle([

                    ("BACKGROUND",
                     (0, 0),
                     (-1, 0),
                     colors.HexColor("#0B3C5D")),

                    ("TEXTCOLOR",
                     (0, 0),
                     (-1, 0),
                     colors.white),

                    ("GRID",
                     (0, 0),
                     (-1, -1),
                     0.5,
                     colors.grey),

                    ("BACKGROUND",
                     (0, 1),
                     (-1, -1),
                     colors.whitesmoke),

                    ("ALIGN",
                     (0, 0),
                     (-1, -1),
                     "CENTER"),

                    ("FONTNAME",
                     (0, 0),
                     (-1, 0),
                     "Helvetica-Bold")

                ])

            )

            story.append(table)

            story.append(
                Spacer(1, 0.3 * inch)
            )

            chart_folder = os.path.join(
                "backend",
                "reports",
                "charts",
                batch_name
            )

            self._add_chart(
                story,
                os.path.join(chart_folder, "ratings.png"),
                "Average Ratings"
            )

            self._add_chart(
                story,
                os.path.join(chart_folder, "course_pace.png"),
                "Course Pace"
            )

            self._add_chart(
                story,
                os.path.join(chart_folder, "concept_clarity.png"),
                "Concept Clarity"
            )

            self._add_chart(
                story,
                os.path.join(chart_folder, "topics.png"),
                "Top Learning Topics"
            )

            self._add_chart(
                story,
                os.path.join(chart_folder, "suggestions.png"),
                "Improvement Suggestions"
            )

            # -----------------------------------------
            # AI Analysis
            # -----------------------------------------

            story.append(
                self._section("Executive Summary")
            )

            story.append(
                Paragraph(
                    str(sentiment),
                    self.styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 0.2 * inch)
            )

            story.append(
                self._section("Top Learning Topics")
            )

            for topic, count in stats.get("topics_learned", []):

                story.append(
                    Paragraph(
                        f"• {topic} ({count})",
                        self.styles["BodyText"]
                    )
                )

            story.append(
                Spacer(1, 0.2 * inch)
            )

            story.append(
                self._section("Common Challenges")
            )

            for challenge, count in stats.get("common_challenges", [])[:10]:

                story.append(
                    Paragraph(
                        f"• {challenge} ({count})",
                        self.styles["BodyText"]
                    )
                )

            story.append(
                Spacer(1, 0.2 * inch)
            )

            story.append(
                self._section("Improvement Suggestions")
            )

            for suggestion, count in stats.get("improvement_suggestions", [])[:10]:

                story.append(
                    Paragraph(
                        f"• {suggestion} ({count})",
                        self.styles["BodyText"]
                    )
                )

            story.append(
                Spacer(1, 0.3 * inch)
            )

            story.append(
                self._section("Key Strengths")
            )

            for item in ai.get("Key Strengths", []):

                story.append(
                    Paragraph(
                        f"✔ {item}",
                        self.styles["BodyText"]
                    )
                )

            story.append(
                Spacer(1, 0.2 * inch)
            )

            story.append(
                self._section("Major Concerns")
            )

            for item in ai.get("Major Concerns", []):

                story.append(
                    Paragraph(
                        f"⚠ {item}",
                        self.styles["BodyText"]
                    )
                )

            story.append(
                Spacer(1, 0.2 * inch)
            )

            story.append(
                self._section("Action Items")
            )

            for item in ai.get("Action Items", []):

                story.append(
                    Paragraph(
                        f"• {item}",
                        self.styles["BodyText"]
                    )
                )

            story.append(
                Spacer(1, 0.3 * inch)
            )

            story.append(

                Paragraph(

                    f"<b>Overall Quality Score:</b> {quality}/100",

                    self.styles["Heading2"]

                )

            )

            # -----------------------------------------
            # Next Batch
            # -----------------------------------------

            if batch != report["batches"][-1]:

                story.append(PageBreak())

        # -----------------------------------------
        # Build PDF
        # -----------------------------------------

        doc.build(story)

        print("\n✅ Multi Batch PDF Generated Successfully!")