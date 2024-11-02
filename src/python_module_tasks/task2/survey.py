import json
import os

import requests


class Survey:
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    HEADERS = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    BASE_URL = "https://api.surveymonkey.com/v3"
    parsed_survey_data: dict = {}
    id: str | None = None

    def __init__(self, questions_file: str):
        if not os.path.isfile(questions_file):
            print(f"File {questions_file} not found")
            raise FileNotFoundError
        questions_file_f = open(
            questions_file,
            "r",
        )
        questions_dict = json.load(questions_file_f)
        questions_file_f.close()
        self.parsed_survey_data = self.__parse_questions(questions_dict)

    def __parse_questions(self, questions_dict):
        survey_name = list(questions_dict.keys())[0]
        pages = []
        for page_name, questions in questions_dict[survey_name].items():
            page = {"title": page_name, "questions": []}
            for question_name, question in questions.items():
                question_payload = {
                    "headings": [{"heading": question["Description"]}],
                    "family": "single_choice",
                    "subtype": "vertical",
                    "answers": {
                        "choices": [{"text": answer} for answer in question["Answers"]]
                    },
                }
                page["questions"].append(question_payload)
            pages.append(page)

        return {"survey_name": survey_name, "pages": pages}

    def create(self):
        create_page_url = f"{self.BASE_URL}/surveys"
        page_payload = {
            "title": self.parsed_survey_data["survey_name"],
            "pages": self.parsed_survey_data["pages"],
        }
        response = requests.post(
            create_page_url, headers=self.HEADERS, json=page_payload
        )
        if response.status_code >= 400:
            print(response.status_code)
            raise Exception(f"Error creating survey: {response.json()}")

        self.id = response.json()["id"]
        return response.json()

    def __create_email_collector(self):
        if self.id is None:
            raise Exception("Survey not created yet")

        create_collector_url = f"{self.BASE_URL}/surveys/{self.id}/collectors"
        payload = {
            "type": "email",
            "name": "Email collector",
        }
        response = requests.post(
            create_collector_url, headers=self.HEADERS, json=payload
        )
        if response.status_code >= 400:
            raise Exception(f"Error creating collector: {response.json()}")

        return response.json()

    def __create_collector_message(self, collector_id: str):
        if self.id is None:
            print("Survey not created yet")
            raise Exception("Survey not created yet")

        create_collector_url = f"{self.BASE_URL}/collectors/{collector_id}/messages"
        payload = {
            "type": "invite",
            "subject": "Survey invitation",
            "body_text (for email invitations)": "Please take this survey",
        }
        response = requests.post(
            create_collector_url, headers=self.HEADERS, json=payload
        )
        if response.status_code >= 400:
            raise Exception(f"Error creating collector message: {response.json()}")

        return response.json()

    def __add_message_recipents(
        self, collector_id: str, message_id: str, recipents_emails: list[str]
    ):
        if self.id is None:
            raise Exception("Survey not created yet")

        add_recipents_url = f"{self.BASE_URL}/collectors/{collector_id}/messages/{message_id}/recipients/bulk"
        payload = {"contants": [{"email": email} for email in recipents_emails]}
        response = requests.post(add_recipents_url, headers=self.HEADERS, json=payload)

        if response.status_code >= 400:
            raise Exception(f"Error adding recipents: {response.json()}")

        return response.json()

    def __send_message(self, collector_id: str, message_id: str):
        if self.id is None:
            raise Exception("Survey not created yet")

        send_message_url = (
            f"{self.BASE_URL}/collectors/{collector_id}/messages/{message_id}/send"
        )
        response = requests.post(send_message_url, headers=self.HEADERS)

        if response.status_code >= 400:
            raise Exception(f"Error sending message: {response.json()}")

        return response.json()

    def add_email_recipents(self, emails: list[str]):
        collector = self.__create_email_collector()
        message = self.__create_collector_message(collector["id"])
        recipents = self.__add_message_recipents(collector["id"], message["id"], emails)
        send_res = self.__send_message(collector["id"], message["id"])

        return send_res
