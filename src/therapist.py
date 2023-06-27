from appointment_calendar import Calendar
from typing import *

class Therapist:

    def __init__(self, full_name: str, tg_user_name: str, description: str):
        self.full_name = full_name
        self.full_name_url = full_name.replace(" ", "_").lower()
        self.tg_user_name = tg_user_name
        self.description = description
        self.calendar = Calendar(therapist_name=full_name)

    def get_booking_available_dates(self, day_of_week: int) -> List[str]:
        return self.calendar.get_available_dates(day_of_week)
