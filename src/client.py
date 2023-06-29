from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    Application,
    ContextTypes
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from therapist import Therapist
from db import TherapistDB
from processor import CallbackProcessor
from constants import *



class Client:
    """
    class responsible for running all assyncronous tasks
    """

    def __init__(self):
        self.db = TherapistDB()
        self.processor = CallbackProcessor(self.db)
        example1 = Therapist('Timchenko Daniil Gennadyevich', '1234567890', 'TEST')
        example2 = Therapist('Not Daniil Gennadyevich', '125125125', 'TEST')
        self.db.add_therapist(example1)
        self.db.add_therapist(example2)

    def run(self, tg_app: Application) -> None:
        self.init_handlers(tg_app)
        print("Polling...")
        tg_app.run_polling()

    def init_handlers(self, app: Application) -> None:
        app.add_handler(CallbackQueryHandler(self.button))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.incoming_message))
        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('list', self.get_therapist_list))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton("Register on a session", callback_data="list_of_therapists"),
                InlineKeyboardButton("View my registrations", callback_data="2"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please choose:", reply_markup=reply_markup)

    async def incoming_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please use buttons, not text")

    async def get_therapist_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(self.db.get_therapist_list_as_text()))

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message"""
        query = update.callback_query
        await query.answer()

        reply = self.processor.process(query.data, update.effective_user.full_name)
        await query.edit_message_text(text=reply['text'], reply_markup=reply['reply_markup'])

