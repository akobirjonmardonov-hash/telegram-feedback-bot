from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add("📢 Taklif", "⚠️ E’tiroz")

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaykum!\nTaklif yoki e’tirozingizni tanlang:",
        reply_markup=menu
    )

@dp.message_handler(lambda m: m.text in ["📢 Taklif", "⚠️ E’tiroz"])
async def choose_type(message: types.Message):
    await message.answer("Marhamat, fikringizni yozing:")

@dp.message_handler()
async def receive(message: types.Message):
    user = message.from_user
    await bot.send_message(
        ADMIN_ID,
        f"🆕 Yangi murojaat\n"
        f"👤 @{user.username}\n"
        f"📝 {message.text}"
    )
    await message.answer("Rahmat! Murojaatingiz qabul qilindi ✅", reply_markup=menu)

if __name__ == "__main__":
    executor.start_polling(dp)
