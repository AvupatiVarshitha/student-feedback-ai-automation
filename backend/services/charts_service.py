import os
import matplotlib.pyplot as plt


class ChartService:

    def __init__(self):

        self.chart_folder = "backend/reports/charts"

        os.makedirs(self.chart_folder, exist_ok=True)

    # ------------------------------------
    # Average Ratings
    # ------------------------------------

    def rating_chart(self, summary):

        labels = [
            "Course",
            "Trainer",
            "Program Team"
        ]

        values = [
            summary["course_satisfaction"],
            summary["trainer_rating"],
            summary["program_team_rating"]
        ]

        plt.figure(figsize=(6,4))
        plt.bar(labels, values)
        plt.ylim(0,5)
        plt.title("Average Ratings")
        plt.ylabel("Rating")
        plt.savefig(
            os.path.join(
                self.chart_folder,
                "ratings.png"
            ),
            bbox_inches="tight"
        )
        plt.close()

    # ------------------------------------
    # Course Pace
    # ------------------------------------

    def pace_chart(self, summary):

        pace = summary["course_pace"]

        plt.figure(figsize=(6,4))
        plt.bar(
            list(pace.keys()),
            list(pace.values())
        )

        plt.title("Course Pace")

        plt.savefig(
            os.path.join(
                self.chart_folder,
                "course_pace.png"
            ),
            bbox_inches="tight"
        )

        plt.close()

    # ------------------------------------
    # Concept Clarity
    # ------------------------------------

    def concept_chart(self, summary):

        clarity = summary["concept_clarity"]

        plt.figure(figsize=(6,4))

        plt.bar(
            list(clarity.keys()),
            list(clarity.values())
        )

        plt.title("Concept Clarity")

        plt.savefig(
            os.path.join(
                self.chart_folder,
                "concept_clarity.png"
            ),
            bbox_inches="tight"
        )

        plt.close()

    # ------------------------------------
    # Topics Learned
    # ------------------------------------

    def topics_chart(self, summary):

        topics = summary["topics_learned"][:5]

        labels = [x[0] for x in topics]

        values = [x[1] for x in topics]

        plt.figure(figsize=(8,4))

        plt.barh(labels, values)

        plt.title("Top Learned Topics")

        plt.savefig(
            os.path.join(
                self.chart_folder,
                "topics.png"
            ),
            bbox_inches="tight"
        )

        plt.close()

    # ------------------------------------
    # Improvement Suggestions
    # ------------------------------------

    def suggestions_chart(self, summary):

        suggestions = summary["improvement_suggestions"][:5]

        labels = [x[0] for x in suggestions]

        values = [x[1] for x in suggestions]

        plt.figure(figsize=(8,4))

        plt.barh(labels, values)

        plt.title("Top Improvement Suggestions")

        plt.savefig(
            os.path.join(
                self.chart_folder,
                "suggestions.png"
            ),
            bbox_inches="tight"
        )

        plt.close()

    # ------------------------------------
    # Generate Everything
    # ------------------------------------

    def generate_all_charts(self, summary):

        self.rating_chart(summary)

        self.pace_chart(summary)

        self.concept_chart(summary)

        self.topics_chart(summary)

        self.suggestions_chart(summary)