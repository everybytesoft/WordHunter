""" Основной код работы бота на aiogram """
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from random import *
from aiogram import F
from aiogram.types import FSInputFile
from Image import svg_grid

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token='6772995205:AAG2HfLj4Q2H77sCLAEaO4uJ1nTDbqTny1c')
# Диспетчер
dp = Dispatcher()


class WordlyBot:
    """ Храним данные для игры в классе """
    word: str = ""
    word_for_check: str= ""
    b: int = 0
    letters_in_word: list[str] = []
    letters_not_in_word: list[str] = []
    letters_is_not_used: list[str] = [
        "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м",
        "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ",
        "ы", "ь", "э", "ю", "я"
    ]
    list_of_words: list[str] = []
    data: list[str, int] = [
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
    ]
    d: int = 0
    c: int = 0
    list_of_used_words: list[str] = []



@dp.message(Command("start"))
async def start_command(message: types.Message) -> str:
    """ Функция - команда приветствие пользователя и найстройка интерфейса """
    button = [[types.KeyboardButton(text="/play")]]
    markup = types.ReplyKeyboardMarkup(keyboard=button)
    await message.answer(
        "Добро пожаловать в наш телеграмм бот! Здесь вы можете играть в игру Worlde. Вам нужно угадать слово из 5 букв. Чтобы начать игру, нажмите на кнопку /play",
        reply_markup=markup)

    await message.answer("""Обозначения: 
⬛️ - буква не входит в слово, 
🟨 - буква есть в слове, но не в этой позиции, 
🟩 - буква есть в слове и в этой позиции""")


@dp.message(Command("play"))
async def play_command(message: types.Message) -> str:
    """ Функция - команда запуск игры и настройка игры """
    with open("data.txt", "r") as f:
        data = f.read()
        items: list[str] = data[1:-1].split(',')
        word: str = choice(items)
    WordlyBot.word = word[1:-1]
    WordlyBot.b = 0
    WordlyBot.letters_in_word = []
    WordlyBot.letters_not_in_word = []
    WordlyBot.letters_is_not_used = [
        "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м",
        "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ",
        "ы", "ь", "э", "ю", "я"
    ]
    WordlyBot.list_of_words = items
    WordlyBot.data = [
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
        [[" ", 0], [" ", 0], [" ", 0], [" ", 0], [" ", 0]],
    ]
    WordlyBot.d = 0
    WordlyBot.c = 0
    WordlyBot.list_of_used_words = []
    await message.answer(
        "Слово загадано! У вас есть 6 попыток, чтобы угадать его. Напишите слово:"
    )


@dp.message(F.text)
async def process_text_message(message: types.Message):
    """ Функция логики самой игры """
    message_text: str = message.text.lower()
    WordlyBot.word_for_check = "'" + message_text + "'"
    if WordlyBot.word == "":
        await message.answer("Игра еще не началась! Напишите /play")
    elif WordlyBot.b == 6:
        await message.answer(
            "Игра окончена! Чтобы начать заново, нажмите на кнопку /play")
    elif WordlyBot.word_for_check not in WordlyBot.list_of_words:
        await message.answer("Введите существующее слово из 5 букв!")
    elif message_text in WordlyBot.list_of_used_words:
        await message.answer("Вы уже писали это слово, выберите другое")
    elif message_text == WordlyBot.word:
        for i in message_text:
            WordlyBot.data[WordlyBot.d][WordlyBot.c][0] = i
            WordlyBot.data[WordlyBot.d][WordlyBot.c][1] = 2
            WordlyBot.c += 1
        svg_grid(WordlyBot.data)
        img: image = FSInputFile("output.png")
        await message.answer_photo(img)
        await message.answer(
            "Поздравляем! Вы угадали слово! Чтобы начать заново, нажмите на кнопку /play"
        )
        WordlyBot.b = 6
    else:
        WordlyBot.list_of_used_words.append(message_text)
        s: list[str] = list(self.word)
        s2: list[str] = list(self.word)
        green1: int = 0
        yellow1: int = 0
        green2: int = 0
        yellow2: int = 0
        Checked_Word1: list[str, int] = []
        Checked_Word2: list[str, int] = []
        for i in message_text:
            if i in s and WordlyBot.word.index(i) == message_text.index(i):
                Checked_Word1.append([i, 2])
                if i not in WordlyBot.letters_in_word:
                    WordlyBot.letters_in_word.append(i)
                if i in WordlyBot.letters_is_not_used:
                    WordlyBot.letters_is_not_used.remove(i)
                s.remove(i)
                green1 += 1
            elif i in s:
                Checked_Word1.append([i, 1])
                if i not in WordlyBot.letters_in_word:
                    WordlyBot.letters_in_word.append(i)
                if i in WordlyBot.letters_is_not_used:
                    WordlyBot.letters_is_not_used.remove(i)
                s.remove(i)
                yellow1 += 1
            else:
                Checked_Word1.append([i, 0])
                if i not in WordlyBot.letters_not_in_word and i not in WordlyBot.letters_in_word:
                    WordlyBot.letters_not_in_word.append(i)
                if i in WordlyBot.letters_is_not_used:
                    WordlyBot.letters_is_not_used.remove(i)
        message_text2: str = message_text[::-1]
        word2: str = WordlyBot.word[::-1]
        for i in message_text2:
            if i in s2 and word2.index(i) == message_text2.index(i):
                Checked_Word2.append([i, 2])
                if i not in WordlyBot.letters_in_word:
                    WordlyBot.letters_in_word.append(i)
                if i in WordlyBot.letters_is_not_used:
                    WordlyBot.letters_is_not_used.remove(i)
                s2.remove(i)
                green2 += 1
            elif i in s:
                Checked_Word2.append([i, 1])
                if i not in WordlyBot.letters_in_word:
                    WordlyBot.letters_in_word.append(i)
                if i in WordlyBot.letters_is_not_used:
                    WordlyBot.letters_is_not_used.remove(i)
                s2.remove(i)
                yellow2 += 1
            else:
                Checked_Word2.append([i, 0])
                if i not in WordlyBot.letters_not_in_word and i not in WordlyBot.letters_in_word:
                    WordlyBot.letters_not_in_word.append(i)
                if i in WordlyBot.letters_is_not_used:
                    WordlyBot.letters_is_not_used.remove(i)
        if green1 > green2:
            WordlyBot.data[WordlyBot.d] = Checked_Word1
        elif green1 < green2:
            WordlyBot.data[WordlyBot.d] = Checked_Word2[::-1]
        elif yellow1 >= yellow2:
            WordlyBot.data[WordlyBot.d] = Checked_Word1
        else:
            WordlyBot.data[WordlyBot.d] = Checked_Word2[::-1]
        WordlyBot.d += 1
        svg_grid(WordlyBot.data)
        img: image = FSInputFile("output.png")
        await message.answer_photo(img)
        if WordlyBot.b < 5:
            await message.answer(
                "Буквы в слове: " +
                str(sorted(WordlyBot.letters_in_word))[1:-1].replace("'", ""))
            await message.answer("Буквы не в слове: " + str(
                sorted(WordlyBot.letters_not_in_word))[1:-1].replace("'", ""))
            await message.answer(
                "Неиспользованные буквы: " +
                str(WordlyBot.letters_is_not_used)[1:-1].replace("'", ""))
        WordlyBot.b += 1
        if WordlyBot.b == 6:
            await message.answer("Вы проиграли! Загаданное слово было: " +
                                 WordlyBot.word)
            await message.answer("Чтобы начать заново, нажмите на кнопку /play"
                                 )


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
