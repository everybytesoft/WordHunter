""" Основной код работы бота с базами данных """
import telebot
from random import *
from Image import svg_grid
from sqlite3 import connect


class WordlyBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.list_of_words = []

    def start_command(self, message: telebot.types.Message):
        """ Функция - команда приветствие пользователя и найстройка интерфейса """
        user_id = message.from_user.id
        with connect('sqlite (2).db') as connection:
            my_cursor = connection.cursor()
            query = f'SELECT id FROM WordleDataBase WHERE id = {user_id}'
            my_cursor.execute(query)
            rows = my_cursor.fetchall()
            if len(rows) == 0:
                query = f'''INSERT INTO WordleDataBase (id) 
VALUES ({user_id})'''
                my_cursor.execute(query)
                connection.commit()
                query = f'''INSERT INTO data (id) 
VALUES ({user_id})'''
                my_cursor.execute(query)
                connection.commit()
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

    def play_command(self, message: telebot.types.Message):
        """ Функция - команда запуск игры и настройка игры """
        user_id = message.from_user.id
        with open("data.txt", "r") as f:
            data = f.read()
            items = data[1:-1].split(',')
            new_word = choice(items)
        self.list_of_words = items
        with connect('sqlite (2).db') as connection:
            my_cursor = connection.cursor()
            query = f"""UPDATE WordleDataBase
SET word={new_word},
    b=0,
    letters_in_word='',
    letters_not_in_word='',
    letters_is_not_used='а, б, в, г, д, е, ё, ж, з, и, й, к, л, м, н, о, п, р, с, т, у, ф, х, ц, ч, ш, щ, ъ, ы, ь, э, ю, я',
    d=0,
    c=0,
    list_of_used_words=''
where id={user_id};"""
            my_cursor.execute(query)
            connection.commit()
            query = f"""UPDATE data
SET word1=' ,0;  ,0;  ,0;  ,0;  ,0',
    word2=' ,0;  ,0;  ,0;  ,0;  ,0',
    word3=' ,0;  ,0;  ,0;  ,0;  ,0',
    word4=' ,0;  ,0;  ,0;  ,0;  ,0',
    word5=' ,0;  ,0;  ,0;  ,0;  ,0',
    word6=' ,0;  ,0;  ,0;  ,0;  ,0'
WHERE id={user_id};"""
            my_cursor.execute(query)
            connection.commit()
        self.send_message(
            message.from_user.id,
            "Слово загадано! У вас есть 6 попыток, чтобы угадать его. Напишите слово:"
        )


    def process_text_message(self, message: telebot.types.Message):
        """ Функция логики самой игры """
        user_id = message.from_user.id
        with connect('sqlite (2).db') as connection:
            my_cursor = connection.cursor()
            query = f"SELECT * FROM WordleDataBase WHERE id={user_id};"
            my_cursor.execute(query)
            row = my_cursor.fetchall()
        word = row[0][1]
        b = row[0][2]
        if b == 0:
            letters_in_word = list(row[0][3])
            letters_not_in_word = list(row[0][4])
        else:
            letters_in_word = row[0][3].split(',')
            letters_not_in_word = row[0][4].split(',')
        letters_is_not_used = row[0][5].split(',')
        d = row[0][6]
        c = row[0][7]
        list_of_used_words = list(row[0][8])
        with connect('sqlite (2).db') as connection:
            my_cursor = connection.cursor()
            query = f"""SELECT word1, word2, word3, word4, word5, word6 FROM data WHERE id={user_id};"""
            my_cursor.execute(query)
            row = my_cursor.fetchall()
        data = list(row[0])
        data2 = []
        for i in data:
            data2.append(i.split(";"))
        data3 = []
        for i in data2:
            s = []
            for j in i:
                s.append(j.split(","))
            data3.append(s)
        message_text = message.text.lower()
        word_for_check = "'" + message_text + "'"
        if word == "":
            self.send_message(message.from_user.id, "Игра еще не началась! Напишите /play")
        elif b == 6:
            self.send_message(message.from_user.id, "Игра окончена! Чтобы начать заново, нажмите на кнопку /play")
        elif word_for_check not in self.list_of_words:
            self.send_message(message.from_user.id, "Введите существующее слово из 5 букв!")
        elif message_text in list_of_used_words:
            self.send_message(message.from_user.id, "Вы уже писали это слово, выберите другое")
        elif message_text == word:
            for i in message_text:
                data3[d][c][0] = i
                data3[d][c][1] = 2
                c += 1
            svg_grid(data3)
            img = open('output.png', 'rb')
            self.send_photo(message.from_user.id, img)
            self.send_message(message.from_user.id, "Поздравляем! Вы угадали слово! Чтобы начать заново, нажмите на кнопку /play")
            b = 6
            with connect('sqlite (2).db') as connection:
                my_cursor = connection.cursor()
                query = f"UPDATE WordleDataBase SET b=6 WHERE id={user_id}"
                my_cursor.execute(query)
                connection.commit()
        else:
            list_of_used_words.append(message_text)
            s = list(word)
            s2 = list(word)
            green1 = 0
            yellow1 = 0
            green2 = 0
            yellow2 = 0
            Checked_Word1 = []
            Checked_Word2 = []
            for i in message_text:
                if i in s and word.index(i) == message_text.index(i):
                    Checked_Word1.append([i, 2])
                    if i not in letters_in_word:
                        letters_in_word.append(i)
                    if i in letters_is_not_used:
                        letters_is_not_used.remove(i)
                    s.remove(i)
                    green1 += 1
                elif i in s:
                    Checked_Word1.append([i, 1])
                    if i not in letters_in_word:
                        letters_in_word.append(i)
                    if i in letters_is_not_used:
                        letters_is_not_used.remove(i)
                    s.remove(i)
                    yellow1 += 1
                else:
                    Checked_Word1.append([i, 0])
                    if i not in letters_not_in_word and i not in letters_in_word:
                        letters_not_in_word.append(i)
                    if i in letters_is_not_used:
                        letters_is_not_used.remove(i)
            message_text2 = message_text[::-1]
            word2 = word[::-1]
            for i in message_text2:
                if i in s2 and word2.index(i) == message_text2.index(i):
                    Checked_Word2.append([i, 2])
                    if i not in letters_in_word:
                        letters_in_word.append(i)
                    if i in letters_is_not_used:
                        letters_is_not_used.remove(i)
                    s2.remove(i)
                    green2 += 1
                elif i in s:
                    Checked_Word2.append([i, 1])
                    if i not in letters_in_word:
                        letters_in_word.append(i)
                    if i in letters_is_not_used:
                        letters_is_not_used.remove(i)
                    s2.remove(i)
                    yellow2 += 1
                else:
                    Checked_Word2.append([i, 0])
                    if i not in letters_not_in_word and i not in letters_in_word:
                        letters_not_in_word.append(i)
                    if i in letters_is_not_used:
                        letters_is_not_used.remove(i)
            if green1 > green2:
                data3[d] = Checked_Word1
            elif green1 < green2:
                data3[d] = Checked_Word2[::-1]
            elif yellow1 >= yellow2:
                data3[d] = Checked_Word1
            else:
                data3[d] = Checked_Word2[::-1]
            d += 1
            svg_grid(data3)
            img = open('output.png', 'rb')
            self.send_photo(message.from_user.id, img)
            if b < 5:
                self.send_message(message.from_user.id,
                                 "Буквы в слове: " + str(sorted(letters_in_word))[1:-1].replace("'", ""))
                self.send_message(message.from_user.id,
                                 "Буквы не в слове: " + str(sorted(letters_not_in_word))[1:-1].replace("'", ""))
                self.send_message(
                    message.from_user.id,
                    "Неиспользованные буквы: " + str(letters_is_not_used)[1:-1].replace("'", ""))
            b += 1
            if b == 6:
                self.send_message(message.from_user.id,
                                 "Вы проиграли! Загаданное слово было: " + word)
                self.send_message(message.from_user.id,
                                 "Чтобы начать заново, нажмите на кнопку /play")
            with connect('sqlite (2).db') as connection:
                my_cursor = connection.cursor()
                query = f"""UPDATE WordleDataBase
SET b={b},
    letters_in_word='{str(letters_in_word)[1:-1].replace("'", "")}',
    letters_not_in_word='{str(letters_not_in_word)[1:-1].replace("'", "")}',
    letters_is_not_used='{str(letters_is_not_used)[1:-1].replace("'", "")}',
    d={d},
    c={c},
    list_of_used_words='{str(list_of_used_words)[1:-1].replace("'", "")}'
WHERE id={user_id};"""
                my_cursor.execute(query)
                connection.commit()
                query = f"""UPDATE data
SET word1='{data3[0][0][0]},{data3[0][0][1]};{data3[0][1][0]},{data3[0][1][1]};{data3[0][2][0]},{data3[0][2][1]};{data3[0][3][0]},{data3[0][3][1]};{data3[0][4][0]},{data3[0][4][1]}',
    word2='{data3[1][0][0]},{data3[1][0][1]};{data3[1][1][0]},{data3[1][1][1]};{data3[1][2][0]},{data3[1][2][1]};{data3[1][3][0]},{data3[1][3][1]};{data3[1][4][0]},{data3[1][4][1]}',
    word3='{data3[2][0][0]},{data3[2][0][1]};{data3[2][1][0]},{data3[2][1][1]};{data3[2][2][0]},{data3[2][2][1]};{data3[2][3][0]},{data3[2][3][1]};{data3[2][4][0]},{data3[2][4][1]}',
    word4='{data3[3][0][0]},{data3[3][0][1]};{data3[3][1][0]},{data3[3][1][1]};{data3[3][2][0]},{data3[3][2][1]};{data3[3][3][0]},{data3[3][3][1]};{data3[3][4][0]},{data3[3][4][1]}',
    word5='{data3[4][0][0]},{data3[4][0][1]};{data3[4][1][0]},{data3[4][1][1]};{data3[4][2][0]},{data3[4][2][1]};{data3[4][3][0]},{data3[4][3][1]};{data3[4][4][0]},{data3[4][4][1]}',
    word6='{data3[5][0][0]},{data3[5][0][1]};{data3[5][1][0]},{data3[5][1][1]};{data3[5][2][0]},{data3[5][2][1]};{data3[5][3][0]},{data3[5][3][1]};{data3[5][4][0]},{data3[5][4][1]}'
WHERE id={user_id};"""
                my_cursor.execute(query)
                connection.commit()


    def run(self):
        """ Функция логики самой игры """
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.play_command, commands=["play"])
        self.register_message_handler(self.process_text_message, content_types=["text"])
        self.polling(none_stop=True, interval=0)
