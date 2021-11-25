from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import logging

import pathlib


condition = ""

# ----------start option--------
dict31 = {"name":"Регистрационное поле 1","slug":"reg1","childs":"None"}
dict32 = {"name":"Регистрационное поле 2","slug":"reg2","childs":"None"}
dict33 = {"name":"Регистрационное поле 3","slug":"reg3","childs":"None"}
dict34 = {"name":"Регистрационное поле 4","slug":"reg4","childs":"None"}

list_child_dicts = []

list_child_dicts.append(dict31)
list_child_dicts.append(dict32)
list_child_dicts.append(dict33)
list_child_dicts.append(dict34)

dict1 = {"name":"Рег поле 1","slug":"rg1","childs":None}
dict2 = {"name":"Рег поле 2","slug":"rg2","childs":None}
dict3 = {"name":"Рег поле 3","slug":"rg3","childs":list_child_dicts}
start_options = []
start_options.append(dict1)
start_options.append(dict2)
start_options.append(dict3)
# -----------start option -----


# --------parameters-------
question_title = ["Вопрос 1","Вопрос 2","Вопрос 3"]
question_code = ["q1","q2","q3"]
main_options = []
for i in range(len(question_title)):
    dict_={"name":question_title[i],"slug":question_code[i],"childs":None}
    main_options.append(dict_)

print(main_options)

# --------parameters-------


def keyb(id,list_in):
    key_lst = []
    kb = [] 
    for i in range(len(list_in)):
        if start_check(id,list_in)[i]==0:
            key_lst = [(InlineKeyboardButton(list_in[i]["name"], callback_data=list_in[i]["slug"]))]
            kb.append(key_lst)
    return kb

def keyb_line(id,list_in):
    key_lst = []
    for i in range(len(list_in)):
        if start_check(id,list_in)[i]==0:
            key_lst.append(InlineKeyboardButton(list_in[i]["name"], callback_data=list_in[i]["slug"]))
    return [key_lst]


def dict2list_slug(dict_in):
    check_list = []
    for d in dict_in:
        check_list.append(d["slug"])
    return check_list


def start_check(id,check_dict):
    f = open('users_data.csv','r')
    reg_status = []
    check_list = dict2list_slug(check_dict)

    for i in range(len(check_list)):
        reg_status.append(0)
    for line in f:
        elements = line.split(";")
        if elements[0] == str(id):
            for i in range(len(check_list)):
                if elements[1]==check_list[i]:
                    reg_status[i] = 1
    f.close()
    return reg_status

def button(update: Update, context: CallbackContext) -> None:
    global condition
    query = update.callback_query
    query.answer()
    chat = update.effective_chat
    if query.data == "rg2":
        print("kb2")
        string = "kb2"
        keyboard = keyb(chat.id,list_child_dicts)
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat.id, text=string,reply_markup=reply_markup)
    elif (query.data in dict2list_slug(list_child_dicts)):
        f = open('users_data.csv','a')
        file_out = f"{chat.id};rg2;{query.data};"
        f.write(file_out+'\n')
        f.close()
        string = "kb2"
        keyboard = keyb(chat.id,start_options)
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=chat.id, text=string,reply_markup=reply_markup)

        # update.message.reply_text(string, reply_markup=reply_markup)

    elif (query.data in dict2list_slug(start_options)) or (query.data in dict2list_slug(main_options)):
        print(start_check(chat.id,start_options))
        query.edit_message_text(text=f"Введите {query.data}")
        condition = query.data

# def init(update: Update, context: CallbackContext) -> None:
#     path = pathlib.Path('users_data.csv')
#     if not(path):
#         f = open('users_data.csv','w')
#         f.close()

def check(update: Update, context: CallbackContext) -> None:
    global start_options
    chat = update.effective_chat
    keyboard = keyb(chat.id,main_options)
    reply_markup = InlineKeyboardMarkup(keyboard)
    if len(start_check(chat.id,main_options))!=sum(start_check(chat.id,main_options)):
        string = "Выберите один из вариантов:"
    else:
        string = "Доступные команды: /check"
    update.message.reply_text(string, reply_markup=reply_markup)


def start(update: Update, context: CallbackContext) -> None:
    global start_options
    path = pathlib.Path('users_data.csv')
    if not(path):
        f = open('users_data.csv','w')
        f.close()

    chat = update.effective_chat
    keyboard = keyb(chat.id,start_options)
    reply_markup = InlineKeyboardMarkup(keyboard)
    if len(start_check(chat.id,start_options))!=sum(start_check(chat.id,start_options)):
        string = "Выберите один из вариантов:"
    else:
        string = "Доступные команды: /check"
    update.message.reply_text(string, reply_markup=reply_markup)

def echo(update, context):
    global condition, account
    string_in = update.message.text
    chat = update.effective_chat
    if (condition in dict2list_slug(start_options)) or (condition in dict2list_slug(main_options)):
        f = open('users_data.csv','a')
        file_out = f"{chat.id};{condition};{string_in};"
        f.write(file_out+'\n')
        f.close()
        condition = ""
    print(start_check(chat.id,start_options))
    if len(start_check(chat.id,start_options))!=sum(start_check(chat.id,start_options)):
        string = "Выберите один из вариантов:"
        keyboard = keyb(chat.id,start_options)
    else:
        string = "Основное меню бота"
        keyboard = keyb(chat.id,main_options)


    reply_markup = InlineKeyboardMarkup(keyboard)
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=string,reply_markup=reply_markup)


def main() -> None:
    updater = Updater("")

    updater.dispatcher.add_handler(CommandHandler('check', check))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('init', init))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    # updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()