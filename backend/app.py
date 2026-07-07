from backend.services.sheets_service import get_feedback_data
from backend.services.ollama_service import analyze_feedback


def load_prompt(feedback_text):
    with open(
        "backend/prompts/feedback_prompt.txt",
        "r",
        encoding="utf-8"
    ) as file:
        prompt = file.read()

    return prompt.replace("{{feedback}}", feedback_text)


def main():

    print("=" * 60)
    print("Student Tribe Feedback Intelligence System")
    print("=" * 60)

    try:

        feedback = get_feedback_data()

        print(f"\nTotal Responses: {len(feedback)}")

        feedback_text = ""

        for row in feedback:

            feedback_text += "\n"

            for key, value in row.items():
                feedback_text += f"{key}: {value}\n"

        prompt = load_prompt(feedback_text)

        print("\nSending feedback to Gemma 3...\n")

        result = analyze_feedback(prompt)

        print("=" * 60)
        print("AI FEEDBACK REPORT")
        print("=" * 60)
        print(result)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()