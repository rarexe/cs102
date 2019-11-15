import telebot
from telebot import apihelper

bot = telebot.TeleBot('840490390:AAHefA6LEtLLFIl_fjDN-O8KMluVi5HcaGk')

apihelper.proxy = {'https': 'https://51.15.120.43:3128'}

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling()
