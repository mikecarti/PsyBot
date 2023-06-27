from src.db import TherapistDB
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from typing import *
from constants import DAYS_OF_WEEK
from utils import weekday_to_num


class CallbackProcessor:
    def __init__(self, db: TherapistDB):
        self.db = db

    def process(self, callback) -> InlineKeyboardMarkup | dict:
        path = callback.split('/')
        match path[0]:
            case "list_of_therapists":
                return self.get_list_of_therapists()
            case "booking":
                return self.booking_path(path[1:])
            case _:
                return self.get_therapist_page(callback)

    def get_list_of_therapists(self) -> InlineKeyboardMarkup:
        therapists_full_names = self.db.get_therapist_list()
        therapist_keyboard = [
            [InlineKeyboardButton(name, callback_data=self._text_to_http(name))]
            for name in therapists_full_names
        ]
        reply_markup = InlineKeyboardMarkup(therapist_keyboard)
        answer = {'text': "List of therapists", 'reply_markup': reply_markup}
        return answer

    def get_therapist_page(self, full_therapist_name) -> dict:
        description = self.db.get_therapist_info(full_therapist_name)
        # picture = self.db.get_therapist_picture(full_name)
        therapist_text = f"{full_therapist_name} \n\n{description}"
        reply = InlineKeyboardMarkup([[InlineKeyboardButton("Записаться", callback_data=f"booking/{full_therapist_name}")]])
        answer = {'text': therapist_text, 'reply_markup': reply}
        return answer

    def get_booking_available_dates(self, full_name, day_of_week) -> dict:
        available_times = self.db.get_booking_available_time_single_day(full_name, day_of_week)
        buttons = []
        for time in available_times:
            callback_data = f"booking/{full_name}/{day_of_week}/{time}"
            buttons.append(InlineKeyboardButton(time, callback_data=callback_data))
        reply_markup = InlineKeyboardMarkup([buttons])
        answer = {'text': "Available dates", 'reply_markup': reply_markup}
        return answer

    def booking_path(self, callback: List[str]) -> dict:
        # callback = full_name + "/" + day_of_week + "/" + time
        # or
        # callback = full_name + "/" + day_of_week
        # or
        # callback = full_name
        full_therapist_name = callback[0]
        if len(callback) == 1:
            reply_markup = self._send_current_week_options(full_therapist_name)
            answer = {'text': "Выберите дату", 'reply_markup': reply_markup}
            return answer
        elif len(callback) == 2:
            day_of_week = callback[1]
            answer = self.get_booking_available_dates(full_therapist_name, day_of_week)
            return answer
        elif len(callback) == 3:
            time = callback[2]


    def _send_current_week_options(self, full_therapist_name) -> InlineKeyboardMarkup:
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(day, f"booking/{full_therapist_name}/{weekday_to_num(day)}")]
             for day in DAYS_OF_WEEK])
        return reply_markup

    def _text_to_http(self, full_name) -> str:
        return full_name.replace(' ', '_').lower()

