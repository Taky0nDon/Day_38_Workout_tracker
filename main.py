import os
import requests
import datetime as dt

import dotenv


def add_values_to_sheet(date: str, time: str, exercise_name: str, duration: int | float, calories: int | float) -> None:
    sheet_addition = {"workout": {
            "date": date,
            "time": time,
            "exercise": exercise_name,
            "duration": duration,
            "calories": calories
        }
    }
    sheet_post = requests.post(url=SHEETY_POST_ENDPOINT, json=sheet_addition, headers=SHEETY_HEADER)
    sheet_post.raise_for_status()


dotenv.load_dotenv("ENVIRONMENT.env")
NUTRI_ID = os.environ.get("NUTRITIONIX_APPID")
NUTRI_KEY = os.environ.get("NUTRITIONIX_KEY")
NUTRI_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRI_AUTH = {"x-app-id": NUTRI_ID, "x-app-key": NUTRI_KEY}

SHEETY_POST_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
SHEETY_KEY = os.environ.get("SHEETY_KEY")
SHEETY_HEADER = {"Authorization": f"Bearer {os.environ.get('SHEETY_TOKEN')}"}

user_input: str = input("What exercise have you done today?\n")
user_gender: str = input("What is your gender?\n")
user_weight_in_kg: int = int(input("What is your weight (in kg)?\n"))
user_height_in_cm: int = int(input("What is your hieght (in cm)?\n"))
user_age_in_years: int = int(input("What is your age (in years)?\n"))

exercise_params = {
    "query": user_input,
    "gender": user_gender,
    "weight_kg": user_weight_in_kg,
    "height_cm": user_height_in_cm,
    "age": user_age_in_years
}

today: str = dt.datetime.now().strftime("%m/%d/%Y")
current_time: str = dt.datetime.now().strftime("%H:%M:%S")

call = requests.post(url=NUTRI_ENDPOINT, headers=NUTRI_AUTH, json=exercise_params)
call.raise_for_status()
response: dict = call.json()
exercise_list: list[str] = []
duration_list: list[int] = []
calories_list: list[int] = []

for exercise in response["exercises"]:
    current_exercise = exercise["user_input"]
    current_duration = exercise["duration_min"]
    current_calories = exercise["nf_calories"]
    add_values_to_sheet(date=today, time=current_time, exercise_name=current_exercise, duration=current_duration,
                        calories=current_calories)




