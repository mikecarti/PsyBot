import logging
from client import Client
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from constants import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
def main():
    application = ApplicationBuilder().token(TG_TOKEN).build()
    client = Client()
    client.run(application)

if __name__ == "__main__":
    main()
