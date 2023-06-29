from src.db import TherapistDB
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from typing import *
from constants import DAYS_OF_WEEK
from utils import weekday_to_num
import numpy as np
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta, strptime


class CallbackProcessor:
    def __init__(self, db: TherapistDB):
        self.db = db

    def process(self, callback, patient_full_name) -> InlineKeyboardMarkup | dict:
        print(f"Incoming callback: {callback}")
        path = callback.split('/')
        useful_data = path[1:]
        match path[0]:
            case "list_of_therapists":
                return self.get_list_of_therapists()
            case "booking":
                return self.booking_path(useful_data, patient_full_name)
            case "therapist_page":
                return self.get_therapist_page(useful_data)
            case _:
                # using callback because it is important to save info about therapist name
                return self.process_calendar(callback)

    def get_list_of_therapists(self) -> InlineKeyboardMarkup:
        therapists_full_names = self.db.get_therapist_list()
        therapist_keyboard = [
            [InlineKeyboardButton(name, callback_data=f"therapist_page/{self._text_to_http(name)}")]
            for name in therapists_full_names
        ]
        reply_markup = InlineKeyboardMarkup(therapist_keyboard)
        response = {'text': "List of therapists", 'reply_markup': reply_markup}
        return response

    def get_therapist_page(self, full_therapist_name: list) -> dict:
        full_therapist_name = full_therapist_name[0]
        description = self.db.get_therapist_info(full_therapist_name)
        # picture = self.db.get_therapist_picture(full_name)
        therapist_text = f"{full_therapist_name} \n\n{description}"
        reply = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Записаться", callback_data=f"booking/{full_therapist_name}")]])
        response = {'text': therapist_text, 'reply_markup': reply}
        return response

    def get_booking_available_time(self, therapist_full_name: str, booking_date: date) -> dict:
        available_times= self.db.get_booking_available_time_single_day(therapist_full_name, booking_date)
        buttons = []
        for time in available_times:
            callback_data = f"booking/{therapist_full_name}/{booking_date}/{time}"
            buttons.append(InlineKeyboardButton(text=time, callback_data=callback_data))
        buttons = list(np.array_split(buttons, indices_or_sections=4))
        buttons = [list(arr) for arr in buttons]
        reply_markup = InlineKeyboardMarkup(buttons)
        response = {'text': f"Available dates on {booking_date}", 'reply_markup': reply_markup}
        return response

    def booking_path(self, callback: List[str], full_patient_name) -> dict:
        # callback = full_name + "/" + day_of_week + "/" + time
        # or
        # callback = full_name + "/" + day_of_week
        # or
        # callback = full_name
        full_therapist_name = callback[0]
        if len(callback) == 1:
            reply_markup = self._send_current_month_options(full_therapist_name)
            response = {'text': "Выберите дату", 'reply_markup': reply_markup}
            return response
        elif len(callback) == 2:
            day_of_week = callback[1]
            response = self.get_booking_available_time(full_therapist_name, int(day_of_week))
            return response
        elif len(callback) == 3:
            booking_date = strptime(callback[1], "%Y-%m-%d").date()
            time_of_day = callback[2]
            response = self.make_an_appointment(booking_date, time_of_day, full_therapist_name, full_patient_name)
            return response

    def _send_current_week_options(self, full_therapist_name) -> InlineKeyboardMarkup:
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(day, callback_data=f"booking/{full_therapist_name}/{weekday_to_num(day)}")]
             for day in DAYS_OF_WEEK])
        return reply_markup

    def _send_current_month_options(self, full_therapist_name):
        calendar, step = DetailedTelegramCalendar(therapist=full_therapist_name).build()
        return calendar

    def _text_to_http(self, full_name) -> str:
        return full_name.replace(' ', '_').lower()

    def make_an_appointment(self, day_of_week: date, time_of_day: str, full_therapist_name: str, full_patient_name: str):
        result = self.db.make_appointment(day_of_week, time_of_day, full_therapist_name, full_patient_name)
        response = {'text': result, 'reply_markup': None}
        return response

    def process_calendar(self, callback):
        min_date = date.today()
        max_date = date.today() + timedelta(days=30)
        therapist_name = callback.split('/')[0]

        result, key, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date, therapist=therapist_name
                                                     ).process(callback)
        text = ''
        reply_markup = None
        if not result and key:
            # user continues down the calendar
            text = f"Select {LSTEP[step]}"
            response = {'text': text, 'reply_markup': key}
        elif result:
            booking_date = result
            # user selected a specific day
            response = self.get_booking_available_time(therapist_name, booking_date)
        return response
