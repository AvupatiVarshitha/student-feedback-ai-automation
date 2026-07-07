
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, Image, PageBreak
)
import os

class PDFService:
    def __init__(self):
        self.styles = getSampleStyleSheet()

    def _heading(self, text):
        style = self.styles["Heading1"]
        style.alignment = TA_CENTER
        style.textColor = colors.HexColor("#0B3C5D")
        return Paragraph(text, style)

    def _section(self, title):
        return Paragraph(f"<b>{title}</b>", self.styles["Heading2"])

    def _add_chart(self, story, path, title):
        if os.path.exists(path):
            story.append(self._section(title))
            story.append(Image(path, width=6.3*inch, height=3.6*inch))
            story.append(Spacer(1,0.2*inch))

    def build_pdf(self, report, output_path):

        doc = SimpleDocTemplate(output_path)

        story=[]

        stats=report["statistics"]
        ai=report["ai_analysis"]

        quality=ai.get("Overall Quality Score",
                    ai.get("Overall Quality Score (Out of 100)","N/A"))

        sentiment=ai.get("Overall Sentiment","N/A")

        story.append(self._heading("Student Tribe Weekly Feedback Report"))
        story.append(Paragraph("<b>AI Powered Analytics Dashboard</b>",
                               self.styles["Heading2"]))
        story.append(Spacer(1,0.2*inch))

        story.append(
            Paragraph(
                f"<b>Generated:</b> {report['generated_at']}",
                self.styles["Normal"]
            )
        )

        story.append(Spacer(1,0.2*inch))

        table=Table([
            ["Metric","Value"],
            ["Responses",stats["total_responses"]],
            ["Course Satisfaction",stats["course_satisfaction"]],
            ["Trainer Rating",stats["trainer_rating"]],
            ["Program Team Rating",stats["program_team_rating"]],
            ["Quality Score",quality],
            ["Overall Sentiment",sentiment]
        ],colWidths=[3.5*inch,2.5*inch])

        table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0B3C5D")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),0.5,colors.grey),
            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("BOTTOMPADDING",(0,0),(-1,0),8),
        ]))

        story.append(table)
        story.append(Spacer(1,0.25*inch))

        story.append(self._section("Executive Summary"))
        story.append(Paragraph(str(sentiment),self.styles["BodyText"]))

        story.append(PageBreak())

        chart_dir="backend/reports/charts"

        self._add_chart(story, os.path.join(chart_dir,"ratings.png"),"Ratings Overview")
        self._add_chart(story, os.path.join(chart_dir,"concept_clarity.png"),"Concept Clarity")
        self._add_chart(story, os.path.join(chart_dir,"course_pace.png"),"Course Pace")

        story.append(PageBreak())

        story.append(self._section("Top Learning Topics"))
        for topic,count in stats.get("topics_learned",[]):
            story.append(Paragraph(f"• {topic} ({count})",self.styles["BodyText"]))

        story.append(Spacer(1,0.2*inch))

        story.append(self._section("Common Challenges"))
        for item,count in stats.get("common_challenges",[])[:10]:
            story.append(Paragraph(f"• {item} ({count})",self.styles["BodyText"]))

        story.append(Spacer(1,0.2*inch))

        story.append(self._section("Improvement Suggestions"))
        for item,count in stats.get("improvement_suggestions",[])[:10]:
            story.append(Paragraph(f"• {item} ({count})",self.styles["BodyText"]))

        story.append(PageBreak())

        story.append(self._section("Key Strengths"))
        for s in ai.get("Key Strengths",[]):
            story.append(Paragraph(f"✔ {s}",self.styles["BodyText"]))

        story.append(Spacer(1,0.2*inch))

        story.append(self._section("Major Concerns"))
        for s in ai.get("Major Concerns",[]):
            story.append(Paragraph(f"⚠ {s}",self.styles["BodyText"]))

        story.append(Spacer(1,0.2*inch))

        story.append(self._section("Action Items"))
        for s in ai.get("Action Items",[]):
            story.append(Paragraph(f"• {s}",self.styles["BodyText"]))

        story.append(Spacer(1,0.3*inch))

        story.append(Paragraph(
            f"<b>Overall Quality Score:</b> {quality}/100",
            self.styles["Heading2"]
        ))

        doc.build(story)
        print("PDF generated successfully.")
