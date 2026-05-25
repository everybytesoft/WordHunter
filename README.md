# WordHunter — Wordle-бот для Telegram

Телеграм-бот, реализующий игру **Wordle** на русском языке. Игрок угадывает случайное слово из 5 букв за 6 попыток. После каждой попытки бот присылает картинку с цветовыми подсказками.

**Цветовые обозначения:**

- ⬛ — буква не входит в слово
- 🟨 — буква есть в слове, но стоит не на своём месте
- 🟩 — буква стоит на правильном месте

---

## Требования

- Python 3.10+
- [Homebrew](https://brew.sh) (только для macOS/Linux — нужен для системной библиотеки cairo)
- Токен Telegram-бота (получить у [@BotFather](https://t.me/BotFather))

---

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-username/WordHunter.git
cd WordHunter
```

### 2. Установить системную библиотеку cairo

**macOS:**

```bash
brew install cairo
```

**Ubuntu/Debian:**

```bash
sudo apt-get install libcairo2
```

**Windows:**

Скачать и установить GTK runtime: [GTK for Windows Runtime Environment Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)

### 3. Установить Python-зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить переменную окружения (macOS/Linux)

Чтобы Python находил библиотеку cairo, добавьте в `~/.zshrc` или `~/.bashrc`:

```bash
# macOS (Homebrew на Apple Silicon)
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# macOS (Homebrew на Intel)
export DYLD_LIBRARY_PATH="/usr/local/lib:$DYLD_LIBRARY_PATH"
```

Затем примените изменения:

```bash
source ~/.zshrc  # или source ~/.bashrc
```

### 5. Вставить токен бота

Откройте нужный файл запуска и замените токен на свой:

```python
# main.py
bot = WordlyBot('ВАШ_ТОКЕН_ЗДЕСЬ')

# или Bot in aiogram.py
bot = Bot(token='ВАШ_ТОКЕН_ЗДЕСЬ')
```

---

## Запуск

Проект поддерживает три варианта запуска:

### Вариант 1 — основной (pyTelegramBotAPI, однопользовательский)

```bash
python main.py
```

Файлы: `main.py`, `WordlyBot.py`, `Image.py`, `data.txt`

### Вариант 2 — на aiogram (однопользовательский)

```bash
python "Bot in aiogram.py"
```

Файлы: `Bot in aiogram.py`, `Image.py`, `data.txt`

### Вариант 3 — с базой данных SQLite (многопользовательский)

```bash
python main.py  # при подключённом WordlyBot_With_DB.py
```

Файлы: `main.py`, `WordlyBot_With_DB.py`, `Image.py`, `data.txt`

> **Примечание:** вариант 3 находится в разработке — основная функция (разделение состояния по пользователям) работает, но могут встречаться ошибки.

---

## Структура проекта

```text
WordHunter/
├── main.py                  # Точка входа (варианты 1 и 3)
├── WordlyBot.py             # Логика бота на pyTelegramBotAPI
├── WordlyBot_With_DB.py     # Логика бота с SQLite (вариант 3)
├── Bot in aiogram.py        # Логика бота на aiogram (вариант 2)
├── Image.py                 # Генерация PNG-картинки с результатом хода
├── data.txt                 # Словарь русских слов из 5 букв
└── requirements.txt         # Python-зависимости
```

---

## Команды бота

| Команда  | Описание                        |
|----------|---------------------------------|
| `/start` | Приветствие и настройка меню    |
| `/play`  | Начать новую игру               |
| `/rules` | Показать правила игры           |

---

## WordHunter — Wordle Bot for Telegram

A Telegram bot implementing the **Wordle** game in Russian. The player guesses a random 5-letter word within 6 attempts. After each attempt, the bot sends an image with color-coded hints.

**Color legend:**

- ⬛ — letter is not in the word
- 🟨 — letter is in the word but in the wrong position
- 🟩 — letter is in the correct position

---

## Requirements

- Python 3.10+
- [Homebrew](https://brew.sh) (macOS/Linux only — required for the cairo system library)
- A Telegram bot token (get one from [@BotFather](https://t.me/BotFather))

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/WordHunter.git
cd WordHunter
```

### 2. Install the cairo system library

**macOS:**

```bash
brew install cairo
```

**Ubuntu/Debian:**

```bash
sudo apt-get install libcairo2
```

**Windows:**

Download and install the GTK runtime: [GTK for Windows Runtime Environment Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set the library path environment variable (macOS/Linux)

So Python can find the cairo library, add this to your `~/.zshrc` or `~/.bashrc`:

```bash
# macOS (Homebrew on Apple Silicon)
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# macOS (Homebrew on Intel)
export DYLD_LIBRARY_PATH="/usr/local/lib:$DYLD_LIBRARY_PATH"
```

Then apply the changes:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

### 5. Insert your bot token

Open the launch file you want to use and replace the token with yours:

```python
# main.py
bot = WordlyBot('YOUR_TOKEN_HERE')

# or Bot in aiogram.py
bot = Bot(token='YOUR_TOKEN_HERE')
```

---

## Running the Bot

The project supports three launch options:

### Option 1 — main (pyTelegramBotAPI, single-user)

```bash
python main.py
```

Files used: `main.py`, `WordlyBot.py`, `Image.py`, `data.txt`

### Option 2 — aiogram (single-user)

```bash
python "Bot in aiogram.py"
```

Files used: `Bot in aiogram.py`, `Image.py`, `data.txt`

### Option 3 — with SQLite database (multi-user)

```bash
python main.py  # with WordlyBot_With_DB.py connected
```

Files used: `main.py`, `WordlyBot_With_DB.py`, `Image.py`, `data.txt`

> **Note:** Option 3 is a work in progress — the core feature (per-user game state) works, but some bugs may occur.

---

## Project Structure

```text
WordHunter/
├── main.py                  # Entry point (options 1 and 3)
├── WordlyBot.py             # Bot logic using pyTelegramBotAPI
├── WordlyBot_With_DB.py     # Bot logic with SQLite (option 3)
├── Bot in aiogram.py        # Bot logic using aiogram (option 2)
├── Image.py                 # PNG image generation for guess results
├── data.txt                 # Russian 5-letter word dictionary
└── requirements.txt         # Python dependencies
```

---

## Bot Commands

| Command  | Description                      |
|----------|----------------------------------|
| `/start` | Welcome message and menu setup   |
| `/play`  | Start a new game                 |
| `/rules` | Show the game rules              |
