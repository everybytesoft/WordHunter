""" Основной код работы бота """
import telebot
from random import *
from Image import svg_grid
from typing import List, Union


class WordlyBot(telebot.TeleBot):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.word: str = ""
        self.word_for_check: str = ""
        self.b: int = 0
        self.letters_in_word: List[str] = []
        self.letters_not_in_word: List[str] = []
        self.letters_is_not_used: List[str] = [
            "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м",
            "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ",
            "ы", "ь", "э", "ю", "я"
        ]
        self.list_of_words: List[str] = []
        self.data: List[List[List[Union[str, int]]]] = [[[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                     [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                     [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                     [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                     [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                     [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],]
        self.d: int = 0
        self.c: int = 0
        self.list_of_used_words: List[str] = []

    def start_command(self, message: telebot.types.Message) -> None:
        """ Функция - команда приветствие пользователя и найстройка интерфейса """
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
🟩 - буква есть в слове и в этой позиции"""
        )

    def play_command(self, message: telebot.types.Message) -> None:
        """ Функция - команда запуск игры и настройка игры """
        with open("data.txt", "r") as f:
            data = f.read()
            items: List[str] = data[1:-1].split(',')
            word: str = choice(items)
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
            "слово загадано! у вас есть 6 попыток, чтобы угадать его. напишите слово:"
        )


    def process_text_message(self, message: telebot.types.Message) -> None:
        """ Функция логики самой игры """
        message_text: str = message.text.lower()
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
            img: Image = open('output.png', 'rb')
            self.send_photo(message.from_user.id, img)
            self.send_message(message.from_user.id, "Поздравляем! Вы угадали слово! Чтобы начать заново, нажмите на кнопку /play")
            self.b = 6
        else:
            self.list_of_used_words.append(message_text)
            s: List[str] = list(self.word)
            s2: List[str] = list(self.word)
            green1: int = 0
            yellow1: int = 0
            green2: int = 0
            yellow2: int = 0
            Checked_Word1: List[str, int] = []
            Checked_Word2: List[str, int] = []
            for i in message_text:
                if i in s and self.word.index(i) == message_text.index(i):
                    Checked_Word1.append([i, 2])
                    if i not in self.letters_in_word:
                        self.letters_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
                    s.remove(i)
                    green1 += 1
                elif i in s:
                    Checked_Word1.append([i, 1])
                    if i not in self.letters_in_word:
                        self.letters_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
                    s.remove(i)
                    yellow1 += 1
                else:
                    Checked_Word1.append([i, 0])
                    if i not in self.letters_not_in_word and i not in self.letters_in_word:
                        self.letters_not_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
            message_text2: str = message_text[::-1]
            word2: str = self.word[::-1]
            for i in message_text2:
                if i in s2 and word2.index(i) == message_text2.index(i):
                    Checked_Word2.append([i, 2])
                    if i not in self.letters_in_word:
                        self.letters_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
                    s2.remove(i)
                    green2 += 1
                elif i in s:
                    Checked_Word2.append([i, 1])
                    if i not in self.letters_in_word:
                        self.letters_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
                    s2.remove(i)
                    yellow2 += 1
                else:
                    Checked_Word2.append([i, 0])
                    if i not in self.letters_not_in_word and i not in self.letters_in_word:
                        self.letters_not_in_word.append(i)
                    if i in self.letters_is_not_used:
                        self.letters_is_not_used.remove(i)
            if green1 > green2:
                self.data[self.d] = Checked_Word1
            elif green1 < green2:
                self.data[self.d] = Checked_Word2[::-1]
            elif yellow1 >= yellow2:
                self.data[self.d] = Checked_Word1
            else:
                self.data[self.d] = Checked_Word2[::-1]
            self.d += 1
            svg_grid(self.data)
            img: Image = open('output.png', 'rb')
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


    def run(self) -> None:
        """ Функция логики работы бота """
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.play_command, commands=["play"])
        self.register_message_handler(self.process_text_message, content_types=["text"])
        self.polling(none_stop=True, interval=0)
