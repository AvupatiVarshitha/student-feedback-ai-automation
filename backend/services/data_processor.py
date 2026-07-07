from datetime import datetime, timedelta
from collections import Counter


class DataProcessor:

    def __init__(self, feedback_data):
        self.feedback_data = feedback_data

    # ------------------------------------
    # Clean Column Names
    # ------------------------------------

    def clean_row(self, row):
        cleaned = {}

        for key, value in row.items():
            cleaned[key.strip()] = value

        return cleaned

    # ------------------------------------
    # Filter Last N Days
    # ------------------------------------
    def normalize_text(self, text):
        if not text:
            return "No Response"

        text = str(text).strip().lower()

    # -------------------------
    # Yes responses
    # -------------------------

        if text in [
            "yes",
            "yes perfect",
            "yes, always",
            "yes always",
            "very clear",
            "clear"
        ]:
            return "Yes"

    # -------------------------
    # Sometimes
    # -------------------------

        if text in [
            "sometimes",
            "sometimes clear",
            "somewhat helpful"
        ]:
            return "Sometimes"

    # -------------------------
    # No
    # -------------------------

        if text in [
            "no",
            "noo",
            "nothing",
            "none",
            "nil",
            "na",
            "n/a",
            ".",
            "-"
        ]:
            return "No"

        return text.title()

    def filter_last_n_days(self, days=7):

        filtered = []
        cutoff = datetime.now() - timedelta(days=days)

        for row in self.feedback_data:

            row = self.clean_row(row)

            timestamp = row.get("Timestamp")

            if not timestamp:
                continue

            try:
                response_date = datetime.strptime(
                    timestamp,
                    "%d/%m/%Y %H:%M:%S"
                )

                if response_date >= cutoff:
                    filtered.append(row)

            except:
                continue

        return filtered

    # ------------------------------------
    # Course Satisfaction
    # ------------------------------------

    def course_satisfaction(self, responses):

        mapping = {
            "very satisfied": 5,
            "satisfied": 4,
            "neutral": 3,
            "dissatisfied": 2,
            "very dissatisfied": 1
        }

        ratings = []

        for row in responses:

            row = self.clean_row(row)

            value = str(
                row.get(
                    "How satisfied are you with the course so far?",
                    ""
                )
            ).strip().lower()

            if value in mapping:
                ratings.append(mapping[value])

        if not ratings:
            return 0

        return round(sum(ratings) / len(ratings), 2)

    # ------------------------------------
    # Trainer Rating
    # ------------------------------------

    def trainer_rating(self, responses):

        ratings = []

        for row in responses:

            row = self.clean_row(row)

            try:
                ratings.append(
                    float(
                        row["How would you rate the overall training and guidance provided by Rizwan sir?"]
                    )
                )
            except:
                pass

        if not ratings:
            return 0

        return round(sum(ratings) / len(ratings), 2)

    # ------------------------------------
    # Program Team Rating
    # ------------------------------------

    def program_team_rating(self, responses):

        ratings = []

        for row in responses:

            row = self.clean_row(row)

            try:
                ratings.append(
                    float(
                        row["How satisfied are you with the program team?"]
                    )
                )
            except:
                pass

        if not ratings:
            return 0

        return round(sum(ratings) / len(ratings), 2)

    # ------------------------------------
    # Concept Clarity
    # ------------------------------------

    def concept_clarity(self, responses):

        result = Counter()

        for row in responses:

            row = self.clean_row(row)

            answer = self.normalize_text(
                row.get(
                    "Are the concepts explained clearly in the sessions?",
                    ""
                )
            ).strip().lower()

            if answer:
                result[answer] += 1

        return dict(result)

    # ------------------------------------
    # Doubt Support
    # ------------------------------------

    def doubt_support(self, responses):

        result = Counter()

        for row in responses:

            row = self.clean_row(row)

            answer = self.normalize_text(
                row.get(
                    "Do you feel comfortable asking doubts during the sessions?",
                    ""
                )
            ).strip().lower()

            if answer:
                result[answer] += 1

        return dict(result)

    # ------------------------------------
    # Course Pace
    # ------------------------------------

    def course_pace(self, responses):

        result = Counter()

        for row in responses:

            row = self.clean_row(row)

            answer = self.normalize_text(
                row.get(
                    "How do you feel about the pace of the course?",
                    ""
                )
            ).strip().lower()

            if answer:
                result[answer] += 1

        return dict(result)

    # ------------------------------------
    # Assignment Helpfulness
    # ------------------------------------

    def assignment_helpfulness(self, responses):

        result = Counter()

        for row in responses:

            row = self.clean_row(row)

            answer = self.normalize_text(
                row.get(
                    "Are the assignments/practice tasks helping you understand the concepts better?",
                    ""
                )
            ).strip().lower()

            if answer:
                result[answer] += 1

        return dict(result)

    # ------------------------------------
    # Topics Learned
    # ------------------------------------

    def topics_summary(self, responses):

        topics = []

        for row in responses:

            row = self.clean_row(row)

            topic = row.get(
                "What topics did you learn or practice last week?",
                ""
            )

            if topic:
                topic = str(topic).replace(".", ",")
                for item in topic.split(","):
                    item = item.strip()
                    if item:
                        topics.append(item.title())

        return Counter(topics).most_common(10)

    # ------------------------------------
    # Common Challenges
    # ------------------------------------

    def common_challenges(self, responses):

        challenges = []

        for row in responses:

            row = self.clean_row(row)

            challenge = row.get(
                "Are you facing any challenges in the course? If yes, please mention.",
                ""
            )

            challenge = self.normalize_text(challenge)

            if challenge != "No": 
                challenges.append(challenge)

        return Counter(challenges).most_common(10)

    # ------------------------------------
    # Improvement Suggestions
    # ------------------------------------

    def improvement_suggestions(self, responses):

        suggestions = []

        for row in responses:

            row = self.clean_row(row)

            suggestion = row.get(
                "What improvements would you suggest for the course?",
                ""
            )
            suggestion = self.normalize_text(suggestion)

            if suggestion != "No":
                suggestions.append(suggestion)

        return Counter(suggestions).most_common(10)

    # ------------------------------------
    # Build Summary
    # ------------------------------------

    def build_summary(self, days=None):

        if days is None:
            responses = self.feedback_data
        else:
            responses = self.filter_last_n_days(days)

        summary = {

            "total_responses": len(responses),

            "course_satisfaction":
                self.course_satisfaction(responses),

            "trainer_rating":
                self.trainer_rating(responses),

            "program_team_rating":
                self.program_team_rating(responses),

            "concept_clarity":
                self.concept_clarity(responses),

            "doubt_support":
                self.doubt_support(responses),

            "course_pace":
                self.course_pace(responses),

            "assignment_helpfulness":
                self.assignment_helpfulness(responses),

            "topics_learned":
                self.topics_summary(responses),

            "common_challenges":
                self.common_challenges(responses),

            "improvement_suggestions":
                self.improvement_suggestions(responses)

        }

        return summary