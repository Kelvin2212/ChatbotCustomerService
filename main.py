import asyncio
from imaplib import Commands
from matplotlib.pyplot import text
from matplotlib.style import context
from telebot import types
from click import command
from regex import B
import telebot
from pyrogram import Client
from telegram.ext import *

import json
from string import punctuation
import random
import pickle
from tensorflow.keras.models import load_model

with open(r"D:\\UNTAR\\NLP\\project-chatbot-nekoya\\data\\intents.json") as data_file:
    data = json.load(data_file)

model = load_model(
    r"D:\\UNTAR\\NLP\\project-chatbot-nekoya\\bot_model.tf")
le_filename = open(
    r"D:\\UNTAR\\NLP\\project-chatbot-nekoya\\label_encoder.pickle", "rb")
le = pickle.load(le_filename)
le_filename.close()

bot_Token = "5603251334:AAESUOgxBEu7rvVaMtWx56aniN6xBcW8rS4"


def start_command(update, context):
    update.message.reply_text(
        "Terimakasih sudah menghubungi layanan Customer Service Nekoya, dengan senang hati kami akan memberikan informasi yang Bapak/Ibu butuhkan.")
    update.message.reply_text(
        "Silahkan bertanya seputar permsalahan yang bapak/ibu alami")


def help_command(update, context):
    update.message.reply_text('help')


def handle_massage(update, context):
    def preprocess_string(string):
        string = string.lower()
        exclude = set(punctuation)
        string = ''.join(ch for ch in string if ch not in exclude)
        return string

    exit = False
    while not exit:
        inp = text = str(update.message.text).lower()
        prob = model.predict([inp])
        results = le.classes_[prob.argmax()]
        if prob.max() < 0.2:
            print("Bot : Maaf kak, aku ga ngerti")
        else:
            for tg in data['intents']:
                if tg['tag'] == results:
                    responses = tg['responses']
            if results == 'bye':
                exit = True
                print("END CHAT")
            update.message.reply_text(random.choice(responses))
            print(f"Bot : {random.choice(responses)}")
        break


def main():

    updater = Updater(bot_Token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_massage))

    updater.start_polling(5)
    print("bot start running")
    updater.idle()


main()
