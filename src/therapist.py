from appointment_calendar import Calendar
from typing import *
from datetime import date


class Therapist:

    def __init__(self, full_name: str, tg_user_name: str, description: str):
        self.full_name = full_name
        self.full_name_url = full_name.replace(" ", "_").lower()
        self.tg_user_name = tg_user_name
        self.description = description
        self.calendar = Calendar(therapist_name=full_name)

    def get_available_time(self, booking_date: date) -> List[str]:
        return self.calendar.get_available_times(booking_date)

    def book_appointment(self, day_of_week, time_of_day, full_patient_name):
        self.calendar.book_appointment(day_of_week, time_of_day, full_patient_name)

