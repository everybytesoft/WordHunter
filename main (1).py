import telebot
from random import *

TOKEN = '6772995205:AAG2HfLj4Q2H77sCLAEaO4uJ1nTDbqTny1c'
bot = telebot.TeleBot(TOKEN)


class save:
  word = ""
  word_for_check = ""
  b = 0
  letters_in_word = []
  letters_not_in_word = []
  letters_is_not_used = [
      "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м",
      "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ",
      "ы", "ь", "э", "ю", "я"
  ]
  list_of_words = []


@bot.message_handler(commands=["start"])
def start_command(message: telebot.types.Message):
  markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
  button = telebot.types.KeyboardButton("/play")
  markup.add(button)
  bot.send_message(
      message.from_user.id,
      "Добро пожаловать в наш телеграмм бот! Здесь вы можете играть в игру Worlde. Вам нужно угадать слово из 5 букв. Чтобы начать игру, нажмите на кнопку /play",
      reply_markup=markup)
  bot.send_message(
      message.from_user.id, """Обозначения: 
⚫ - буква не входит в слово, 
🟡 - буква есть в слове, но не в этой позиции, 
🟢 - буква есть в слове и в этой позиции""")


@bot.message_handler(commands=["play"])
def play_command(message: telebot.types.Message):
  with open("data.txt", "r") as f:
    data = f.read()
    items = data[1:-1].split(',')
    word = choice(items)
  save.word = word[1:-1]
  save.b = 0
  save.letters_in_word = []
  save.letters_not_in_word = []
  save.letters_is_not_used = [
      "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м",
      "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ",
      "ы", "ь", "э", "ю", "я"
  ]
  save.list_of_words = items
  bot.send_message(
      message.from_user.id,
      "Слово загадано! У вас есть 6 попыток, чтобы угадать его. Напишите слово:"
  )


@bot.message_handler(content_types=["text"])
def process_text_message(message: telebot.types.Message):
  message_text = message.text.lower()
  save.word_for_check = "'" + message_text + "'"
  if save.word == "":
    bot.send_message(message.from_user.id,
                     "Игра еще не началась! Напишите /play")
  elif save.b == 6:
    bot.send_message(
        message.from_user.id,
        "Игра окончена! Чтобы начать заново, нажмите на кнопку /play")
  elif save.word_for_check not in save.list_of_words:
    bot.send_message(message.from_user.id,
                     "Введите существующее слово из 5 букв!")
  elif message_text == save.word:
    bot.send_message(
        message.from_user.id,
        "Поздравляем! Вы угадали слово! Чтобы начать заново, нажмите на кнопку /play"
    )
    save.b = 6
  else:
    bot.send_message(message.from_user.id, "Неправильно! Попробуйте еще раз.")
    answer = ""
    s = list(save.word)
    for i in message_text:
      if i in s and save.word.index(i) == message_text.index(i):
        answer += "🟢"
        if i not in save.letters_in_word:
          save.letters_in_word.append(i)
        if i in save.letters_is_not_used:
          save.letters_is_not_used.remove(i)
        s.remove(i)
      elif i in s:
        answer += "🟡"
        if i not in save.letters_in_word:
          save.letters_in_word.append(i)
        if i in save.letters_is_not_used:
          save.letters_is_not_used.remove(i)
        s.remove(i)
      else:
        answer += "⚫"
        if i not in save.letters_not_in_word:
          save.letters_not_in_word.append(i)
    bot.send_message(message.from_user.id, answer)
    bot.send_message(message.from_user.id,
                     "Буквы в слове: " + str(save.letters_in_word))
    bot.send_message(message.from_user.id,
                     "Буквы не в слове: " + str(save.letters_not_in_word))
    bot.send_message(
        message.from_user.id,
        "Неиспользованные буквы: " + str(save.letters_is_not_used))
    save.b += 1
    if save.b == 6:
      bot.send_message(message.from_user.id,
                       "Вы проиграли! Загаданное слово было: " + save.word)
      bot.send_message(message.from_user.id,
                       "Чтобы начать заново, нажмите на кнопку /play")


bot.polling()
