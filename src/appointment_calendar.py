import calendar
import datetime
from constants import DAYS_OF_WEEK
import pytz
class Calendar:
    TIME_SLOTS = [f"{n}:00" for n in range(7, 24)]

    def __init__(self, therapist_name):
        self.therapist_name = therapist_name
        self.calendar = self.init_calendar()
        # set up time zones
        self.moscow_tz = pytz.timezone('Europe/Moscow')
        self.utc_tz = pytz.timezone('UTC')

    def init_calendar(self):
        return {day_of_month: {time_slot: None for time_slot in self.TIME_SLOTS}
                for day_of_month in range(1, 31)}

    def book_appointment(self, day_of_month, time, patient_full_name):
        if self.calendar[day_of_month][time] is not None:
            raise ValueError(f'{self.therapist_name}Appointment already booked.')
        else:
            self.calendar[day_of_month][time] = patient_full_name
            self._log(f'Appointment booked for {day_of_month} at {time} with {patient_full_name}.')

    def cancel_appointment(self, day_of_month, time):
        if self.calendar[day_of_month][time] is None:
            self._log(f'There is no appointment booked at {day_of_month}, {time}.')
        else:
            patient = self.calendar[day_of_month][time]
            self.calendar[day_of_month][time] = None
            self._log(f'Appointment cancelled for {day_of_month} at {time} with {patient}.')

    def _log(self, msg):
        print(f'{self.therapist_name}: {msg}')

    def get_available_dates(self, day_of_week: int):
        nearest_day = self._get_nearest_possible_day_of_week(day_of_week)
        available_times = []
        for time_slot in self.calendar[nearest_day]:
            if self.calendar[nearest_day][time_slot] is None:
                available_times.append(time_slot)
        return available_times

    def _get_nearest_possible_day_of_week(self, desired_weekday):
        # get current UTC time
        now_utc = datetime.datetime.now(tz=self.utc_tz)
        # convert to Moscow time
        now_moscow = now_utc.astimezone(self.moscow_tz)
        # find nearest desired weekday
        days_ahead = (desired_weekday - now_moscow.weekday()) % 7
        nearest_desired_weekday = now_moscow + datetime.timedelta(days=days_ahead)
        day = nearest_desired_weekday.day
        return day
    