"""Основной код работы бота"""

import telebot
from random import *
from Image import svg_grid
from typing import List


class WordlyBot(telebot.TeleBot):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.Slovar = {}
        self.list_of_words: List[str] = []

    def start_command(self, message: telebot.types.Message) -> None:
        """Функция - команда приветствие пользователя и найстройка интерфейса"""
        id = message.chat.id
        self.Slovar[id] = {
            "word": "",
            "b": 0,
            "letters_in_word": [],
            "letters_not_in_word": [],
            "letters_is_not_used": [
                "а",
                "б",
                "в",
                "г",
                "д",
                "е",
                "ё",
                "ж",
                "з",
                "и",
                "й",
                "к",
                "л",
                "м",
                "н",
                "о",
                "п",
                "р",
                "с",
                "т",
                "у",
                "ф",
                "х",
                "ц",
                "ч",
                "ш",
                "щ",
                "ъ",
                "ы",
                "ь",
                "э",
                "ю",
                "я",
            ],
            "data": [
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
            ],
            "d": 0,
            "c": 0,
            "list_of_used_words": [],
        }
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("/play")
        button2 = telebot.types.KeyboardButton("/rules")
        markup.add(button, button2)
        self.send_message(
            message.chat.id,
            f"Здравствуй {message.chat.first_name}, добро пожаловать в WordHunter! Здесь вы можете веселиться, играя в Wordle.\n\nВсе возможности доступны из меню комманд. Например, чтобы узнать правила, есть комманда /rules. А чтобы начать игру комманда /play",
            reply_markup=markup,
        )

    def rules_command(self, message: telebot.types.Message) -> None:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("/play")
        markup.add(button)
        self.send_message(
            message.chat.id,
            "Правила простые! Вам нужно угадать слово из 5 букв. На это дается 6 попыток. Буквы в неправильных словах будут подсвечиваться, чтобы было проще отгадать нужное.\n\n⬛️ - Буква не входит в слово\n🟨 - Буква есть в слове, но не в этой позиции\n🟩 - Буква есть в слове и в этой позиции\n\nСыграем? /play",
            reply_markup=markup,
        )

    def play_command(self, message: telebot.types.Message) -> None:
        """Функция - команда запуск игры и настройка игры"""
        markup = telebot.types.ReplyKeyboardRemove()
        with open("data.txt", "r") as f:
            data = f.read()
            items: List[str] = data[1:-1].split(",")
            word: str = choice(items)
        id = message.chat.id
        self.Slovar[id] = {
            "word": f"{word[1:-1]}",
            "b": 0,
            "letters_in_word": [],
            "letters_not_in_word": [],
            "letters_is_not_used": [
                "а",
                "б",
                "в",
                "г",
                "д",
                "е",
                "ё",
                "ж",
                "з",
                "и",
                "й",
                "к",
                "л",
                "м",
                "н",
                "о",
                "п",
                "р",
                "с",
                "т",
                "у",
                "ф",
                "х",
                "ц",
                "ч",
                "ш",
                "щ",
                "ъ",
                "ы",
                "ь",
                "э",
                "ю",
                "я",
            ],
            "data": [
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
                [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
            ],
            "d": 0,
            "c": 0,
            "list_of_used_words": [],
        }
        self.list_of_words = items

        self.send_message(
            message.chat.id,
            "Cлово загадано! у вас есть 6 попыток, удачи!",
            reply_markup=markup,
        )

    def process_text_message(self, message: telebot.types.Message) -> None:
        """Функция логики самой игры"""
        id = message.chat.id
        message_text: str = message.text.lower()
        word_for_check = "'" + message_text + "'"
        if self.Slovar[id]["word"] == "":
            self.send_message(
                message.chat.id, "Игра еще не началась! Напишите /play"
            )
        elif self.Slovar[id]["b"] == 6:
            self.send_message(
                message.chat.id,
                "Игра окончена! Чтобы начать заново, нажмите на кнопку /play",
            )
        elif word_for_check not in self.list_of_words:
            self.send_message(
                message.chat.id, "Введите существующее слово из 5 букв!"
            )
        elif message_text in self.Slovar[id]["list_of_used_words"]:
            self.send_message(
                message.chat.id, "Вы уже писали это слово, выберите другое"
            )
        elif message_text == self.Slovar[id]["word"]:
            for i in message_text:
                self.Slovar[id]["data"][self.Slovar[id]["d"]][
                    self.Slovar[id]["c"]
                ][0] = i
                self.Slovar[id]["data"][self.Slovar[id]["d"]][
                    self.Slovar[id]["c"]
                ][1] = 2
                self.Slovar[id]["c"] += 1
            svg_grid(self.Slovar[id]["data"])
            img: Image = open("output.png", "rb")
            self.send_photo(message.chat.id, img)
            self.send_message(
                message.chat.id,
                "Поздравляем! Вы угадали слово! Чтобы начать заново, нажмите на кнопку /play",
            )
            self.b = 6
        else:
            self.Slovar[id]["list_of_used_words"].append(message_text)
            s: List[str] = list(self.Slovar[id]["word"])
            s2: List[str] = list(self.Slovar[id]["word"])
            green1: int = 0
            yellow1: int = 0
            green2: int = 0
            yellow2: int = 0
            Checked_Word1: List[str, int] = []
            Checked_Word2: List[str, int] = []
            for i in message_text:
                if i in s and self.Slovar[id]["word"].index(
                    i
                ) == message_text.index(i):
                    Checked_Word1.append([i, 2])
                    if i not in self.Slovar[id]["letters_in_word"]:
                        self.Slovar[id]["letters_in_word"].append(i)
                    if i in self.Slovar[id]["letters_is_not_used"]:
                        self.Slovar[id]["letters_is_not_used"].remove(i)
                    s.remove(i)
                    green1 += 1
                elif i in s:
                    Checked_Word1.append([i, 1])
                    if i not in self.Slovar[id]["letters_in_word"]:
                        self.Slovar[id]["letters_in_word"].append(i)
                    if i in self.Slovar[id]["letters_is_not_used"]:
                        self.Slovar[id]["letters_is_not_used"].remove(i)
                    s.remove(i)
                    yellow1 += 1
                else:
                    Checked_Word1.append([i, 0])
                    if (
                        i not in self.Slovar[id]["letters_not_in_word"]
                        and i not in self.Slovar[id]["letters_in_word"]
                    ):
                        self.Slovar[id]["letters_not_in_word"].append(i)
                    if i in self.Slovar[id]["letters_is_not_used"]:
                        self.Slovar[id]["letters_is_not_used"].remove(i)
            message_text2: str = message_text[::-1]
            word2: str = self.Slovar[id]["word"][::-1]
            for i in message_text2:
                if i in s2 and word2.index(i) == message_text2.index(i):
                    Checked_Word2.append([i, 2])
                    if i not in self.Slovar[id]["letters_in_word"]:
                        self.Slovar[id]["letters_in_word"].append(i)
                    if i in self.Slovar[id]["letters_is_not_used"]:
                        self.Slovar[id]["letters_is_not_used"].remove(i)
                    s2.remove(i)
                    green2 += 1
                elif i in s:
                    Checked_Word2.append([i, 1])
                    if i not in self.Slovar[id]["letters_in_word"]:
                        self.Slovar[id]["letters_in_word"].append(i)
                    if i in self.Slovar[id]["letters_is_not_used"]:
                        self.Slovar[id]["letters_is_not_used"].remove(i)
                    s2.remove(i)
                    yellow2 += 1
                else:
                    Checked_Word2.append([i, 0])
                    if (
                        i not in self.Slovar[id]["letters_not_in_word"]
                        and i not in self.Slovar[id]["letters_in_word"]
                    ):
                        self.Slovar[id]["letters_not_in_word"].append(i)
                    if i in self.Slovar[id]["letters_is_not_used"]:
                        self.Slovar[id]["letters_is_not_used"].remove(i)
            if green1 > green2:
                self.Slovar[id]["data"][self.Slovar[id]["d"]] = Checked_Word1
            elif green1 < green2:
                self.Slovar[id]["data"][self.Slovar[id]["d"]] = Checked_Word2[
                    ::-1
                ]
            elif yellow1 >= yellow2:
                self.Slovar[id]["data"][self.Slovar[id]["d"]] = Checked_Word1
            else:
                self.Slovar[id]["data"][self.Slovar[id]["d"]] = Checked_Word2[
                    ::-1
                ]
            self.Slovar[id]["d"] += 1
            svg_grid(self.Slovar[id]["data"])
            img: Image = open("output.png", "rb")
            self.send_photo(message.chat.id, img)
            if self.Slovar[id]["b"] < 5:
                self.send_message(
                    message.chat.id,
                    "Буквы в слове: "
                    + str(sorted(self.Slovar[id]["letters_in_word"]))[
                        1:-1
                    ].replace("'", ""),
                )
                self.send_message(
                    message.chat.id,
                    "Буквы не в слове: "
                    + str(sorted(self.Slovar[id]["letters_not_in_word"]))[
                        1:-1
                    ].replace("'", ""),
                )
                self.send_message(
                    message.chat.id,
                    "Неиспользованные буквы: "
                    + str(self.Slovar[id]["letters_is_not_used"])[
                        1:-1
                    ].replace("'", ""),
                )
            self.Slovar[id]["b"] += 1
            if self.Slovar[id]["b"] == 6:
                self.send_message(
                    message.chat.id,
                    "Вы проиграли! Загаданное слово было: "
                    + self.Slovar[id]["word"],
                )
                self.send_message(
                    message.chat.id,
                    "Чтобы начать заново, нажмите на кнопку /play",
                )

    def run(self) -> None:
        """Функция логики работы бота"""
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.play_command, commands=["play"])
        self.register_message_handler(self.rules_command, commands=["rules"])
        self.register_message_handler(
            self.process_text_message, content_types=["text"]
        )
        self.polling(none_stop=True, interval=0)
