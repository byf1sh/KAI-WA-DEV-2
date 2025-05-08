import requests
import json
from services.data_utils import extract_field
from datetime import datetime
from services.bot import send
import time

def form_service(timestamp, caseID, content):
    url = "https://forms.office.com/formapi/api/fdd345f9-103a-4dcf-8685-4bde04046f0c/users/b31f33e5-90e3-412a-a263-5ff4f3484a45/forms('-UXT_ToQz02GhUveBARvDOUzH7PjkCpBomNf9PNISkVUNUg0TEUwUDFDN1ZMNThDMlNHTjNMMVVZMC4u')/responses"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        # Tambahkan User-Agent jika diperlukan
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "startDate": datetime.utcnow().isoformat() + "Z",
        "submitDate": datetime.utcnow().isoformat() + "Z",
        "answers": json.dumps([
            {
                "questionId": "r961e72df4b1d46fea5b3ed3df14bea58",
                "answer1": timestamp
            },
            {
                "questionId": "r1158fc0ee1134322b85fe6cf7a59a1a8",
                "answer1": caseID
            },
            {
                "questionId": "r2589d21575a94098be581967ed0ce5d9",
                "answer1": content
            }
        ])
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 201:
        send("Automation Error - Form not created successfully, URL Form maybe expired, or request data maybe broken")

    # print(f"Response Body:\n{response.text}")

def make_data(data):
    for row in data:
        if "[Automation]" in row["message"]:
            print("Automation Detected not sending to xlsx")
        elif "NOC KAI" in row["message"]:
            print("Message from noc not sending to xlsx")
        else:
            case_id = extract_field("Case ID", row["message"])
            form_service(row["timestamp"], case_id ,row["message"])
        time.sleep(3)

# form_service("231","213","wadawd")