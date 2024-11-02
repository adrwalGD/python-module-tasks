from dotenv import load_dotenv

load_dotenv()

import sys

from python_module_tasks.task2.survey import Survey


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <questions_file> <emails_file>")
        return
    questions_file = sys.argv[1]
    emails_file = sys.argv[2]

    survey = Survey(questions_file)
    res_data = survey.create()
    print("RES DATA", res_data)

    emails_file = open(
        emails_file,
        "r",
    )
    emails = emails_file.readlines()
    emails_file.close()

    survey.add_email_recipents(emails)


if __name__ == "__main__":
    main()
