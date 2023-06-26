from src.db import TherapistDB
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class CallbackProcessor:
    def __init__(self, db: TherapistDB):
        self.db = db

    def process(self, callback) -> InlineKeyboardMarkup | dict:
        match callback:
            case "list_of_therapists":
                return self.markup_list_of_therapists()
            case "whatever":
                return
            case _:
                return self.get_therapist_page(callback)

    def markup_list_of_therapists(self) -> InlineKeyboardMarkup:
        therapists_full_names = self.db.get_therapist_list()
        therapist_keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in therapists_full_names]
        reply_markup = InlineKeyboardMarkup(therapist_keyboard)
        return reply_markup

    def get_therapist_page(self, full_name) -> dict:
        description = self.db.get_therapist_info(full_name)
        # picture = self.db.get_therapist_picture(full_name)
        page = {"full_name": full_name, "description": description}  # "picture": picture}
        return page
