from backend.services.sheets_service import get_feedback_data
from backend.services.data_processor import DataProcessor


def main():

    feedback = get_feedback_data()

    processor = DataProcessor(feedback)

    summary = processor.build_summary()

    print("=" * 60)
    print("Student Tribe Weekly Feedback Summary")
    print("=" * 60)

    print(summary)


if __name__ == "__main__":
    main()