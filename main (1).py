import telebot
from random import *
from Image import svg_grid


class WordlyBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
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
        data = [[[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],]
        d = 0
        c = 0
        list_of_used_words = []
  

    def start_command(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("/play")
        markup.add(button)
        self.send_message(
            message.from_user.id,
            "Добро пожаловать в наш телеграмм бот! Здесь вы можете играть в игру Worlde. Вам нужно угадать слово из 5 букв. Чтобы начать игру, нажмите на кнопку /play",
            reply_markup=markup)
        self.send_message(
            message.from_user.id, """Обозначения: 
    ⬛️ - буква не входит в слово, 
    🟨 - буква есть в слове, но не в этой позиции, 
    🟩 - буква есть в слове и в этой позиции""")


    def play_command(self, message: telebot.types.Message):
      with open("data.txt", "r") as f:
        data = f.read()
        items = data[1:-1].split(',')
        word = choice(items)
      self.word = word[1:-1]
      self.b = 0
      self.letters_in_word = []
      self.letters_not_in_word = []
      self.letters_is_not_used = [
          "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м",
          "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ",
          "ы", "ь", "э", "ю", "я"
      ]
      self.list_of_words = items
      self.data = [[[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                   [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                   [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                   [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                   [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                   [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],]
      self.d = 0
      self.c = 0
      self.list_of_used_words = []
      self.send_message(
          message.from_user.id,
          "Слово загадано! У вас есть 6 попыток, чтобы угадать его. Напишите слово:"
      )
  
  
    def process_text_message(self, message: telebot.types.Message):
        message_text = message.text.lower()
        self.word_for_check = "'" + message_text + "'"
        if self.word == "":
            self.send_message(message.from_user.id, "Игра еще не началась! Напишите /play")
        elif self.b == 6:
            self.send_message(message.from_user.id, "Игра окончена! Чтобы начать заново, нажмите на кнопку /play")
        elif self.word_for_check not in self.list_of_words:
            self.send_message(message.from_user.id, "Введите существующее слово из 5 букв!")
        elif message_text in self.list_of_used_words:
            self.send_message(message.from_user.id, "Вы уже писали это слово, выберите другое")
        elif message_text == self.word:
            for i in message_text:
                self.data[self.d][self.c][0] = i
                self.data[self.d][self.c][1] = 2
                self.c += 1
            svg_grid(self.data)
            img = open('output.png', 'rb')
            self.send_photo(message.from_user.id, img)
            self.send_message(message.from_user.id, "Поздравляем! Вы угадали слово! Чтобы начать заново, нажмите на кнопку /play")
            self.b = 6
        else:
            self.list_of_used_words.append(message_text)
            s = list(self.word)
            for i in message_text:
                if i in s and self.word.index(i) == message_text.index(i):
                    self.data[self.d][self.c] = [i, 2]
                    if i not in self.letters_in_word:
                        self.letters_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
                    s.remove(i)
                    self.c += 1       
                elif i in s:
                    self.data[self.d][self.c] = [i, 1]
                    if i not in self.letters_in_word:
                        self.letters_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
                    s.remove(i)
                    self.c += 1
                else:
                    self.data[self.d][self.c] = [i, 0]
                    if i not in self.letters_not_in_word:
                        self.letters_not_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
                    self.c += 1
            self.d += 1
            self.c = 0
            svg_grid(self.data)
            img = open('output.png', 'rb')
            self.send_photo(message.from_user.id, img)
            if self.b < 5:
                self.send_message(message.from_user.id,
                                 "Буквы в слове: " + str(sorted(self.letters_in_word))[1:-1].replace("'", ""))
                self.send_message(message.from_user.id,
                                 "Буквы не в слове: " + str(sorted(self.letters_not_in_word))[1:-1].replace("'", ""))
                self.send_message(
                    message.from_user.id,
                    "Неиспользованные буквы: " + str(self.letters_is_not_used)[1:-1].replace("'", ""))
            self.b += 1
            if self.b == 6:
                self.send_message(message.from_user.id,
                                 "Вы проиграли! Загаданное слово было: " + self.word)
                self.send_message(message.from_user.id,
                                 "Чтобы начать заново, нажмите на кнопку /play")
  
    def run(self):
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.play_command, commands=["play"])
        self.register_message_handler(self.process_text_message, content_types=["text"])
        self.polling(none_stop=True, interval=0)


def main() -> None:
    bot = WordlyBot('6772995205:AAG2HfLj4Q2H77sCLAEaO4uJ1nTDbqTny1c')
    bot.run()


if __name__ == "__main__":
    main()
