import os
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import (ReplyKeyboardMarkup,  KeyboardButton,  InlineKeyboardMarkup,  InlineKeyboardButton)

TOKEN = os.getenv("BOT_TOKEN", "YOUR_DEFAULT_TOKEN")
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

KEYBOARD_BTN = KeyboardButton("Клавиатура")
INLINE_BTN = InlineKeyboardButton(text = "Случайное число", callback_data = "random_number")

@dp.message_handler(commands = ["start"])
async def start_command(msg: types.Message):
    markup = await getMainKeyboard()
    welcome_text = (
        "<b>Привет!</b>\n"
        "<u>Я бот с полезными командами!</u>\n"
        "Используй /help для списка команд"
    )
    await msg.answer(text = welcome_text, reply_markup = markup, parse_mode = "HTML")

@dp.message_handler(commands = ["help"])
async def help_command(msg: types.Message):
    markup = await getMainKeyboard()
    helpText = (
        "<b>Список команд:</b>\n"
        "/start - Начать работу\n"
        "/help - Показать помощь\n"
        "/inline - Показать inline-кнопку\n"
        "/openkeyboard - Открыть клавиатуру\n"
        "/online - Проверить статус бота"
    )
    await msg.answer(text = helpText, reply_markup = markup, parse_mode = "HTML")

@dp.message_handler(commands = ["inline"])
async def inline_command(msg: types.Message):
    markup = InlineKeyboardMarkup().add(INLINE_BTN)
    await msg.answer(text = "Нажми на кнопку для случайного числа:", reply_markup = markup)

@dp.callback_query_handler(lambda callback: callback.data == "random_number")
async def process_callback(callback: types.CallbackQuery):
    random_num = random.randint(1, 10)
    await callback.message.answer(f"Случайное число: {random_num}")
    await callback.answer()

@dp.message_handler(commands = ["openkeyboard"])
async def open_keyboard(msg: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard = True).add(KEYBOARD_BTN)
    await msg.answer(text = "Клавиатура активирована!", reply_markup = markup)

@dp.message_handler(commands = ["online"])
async def online_check(msg: types.Message):
    await msg.answer(text = "Бот онлайн и готов к работе!")

@dp.message_handler()
async def handle_text(msg: types.Message):
    if msg.text.lower() == "клавиатура":
        await msg.answer(text = "Вы активировали клавиатурную кнопку!", parse_mode = "HTML")
    else:
        await msg.answer("Неизвестная команда. Используй /help для справки.")

async def getMainKeyboard():
    return ReplyKeyboardMarkup(resize_keyboard = True).add(KEYBOARD_BTN)

if __name__ == "__main__":
    print("Бот запущен...")
    executor.start_polling(dp, skip_updates=True)