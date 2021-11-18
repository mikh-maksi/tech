import schedule
import time


from telegram.ext import Updater, MessageHandler, Filters

def job():
    print("I'm working...")

def job_m():
    print("Minute...")
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=str(total_dict))

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("23:00").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job_m)

while True:
    schedule.run_pending()
    time.sleep(1)


def echo(update, context):
    string_in = update.message.text
    string_out = string_in
    update.message.reply_text(string_out)

updater = Updater("2013484013:AAGNF0KtAimfPfyLR2yPZs-JYsJNv7sFRwA")

dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.all, echo))

updater.start_polling()
updater.idle()
