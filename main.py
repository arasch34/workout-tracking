import requests
from datetime import datetime
import os

GENDER = "Male"
WEIGHT = 78
HEIGHT = 180
AGE = 24

APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]

NUTRITIONX_ENDPOINT = " https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.environ["SHEET_ENDPOINT"]

exercise_text = input("Tell me what exercise you did!")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

response = requests.post(NUTRITIONX_ENDPOINT, json=params, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    # Authentication
    sheet_response = requests.post(
        SHEETY_ENDPOINT,
        json=sheet_inputs,
        auth=(
            os.environ["USERNAME"],
            os.environ["PASSWORD"]
        )
    )
