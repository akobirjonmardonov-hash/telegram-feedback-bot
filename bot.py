from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# ================= STATES =================
class Form(StatesGroup):
    category = State()
    identity = State()
    text = State()

# ================= KEYBOARDS =================
category_kb = ReplyKeyboardMarkup(resize_keyboard=True)
category_kb.add("📢 Taklif", "⚠️ E’tiroz")

identity_kb = ReplyKeyboardMarkup(resize_keyboard=True)
identity_kb.add(
    KeyboardButton("📞 Raqamim bilan", request_contact=True),
    KeyboardButton("🙈 Anonim")
)

# ================= HANDLERS =================
@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Assalomu alaykum!\nTaklif yoki e’tirozingizni tanlang:",
        reply_markup=category_kb
    )
    await Form.category.set()

@dp.message_handler(text=["📢 Taklif", "⚠️ E’tiroz"], state=Form.category)
async def choose_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer(
        "Raqam bilan yuborasizmi yoki anonim?",
        reply_markup=identity_kb
    )
    await Form.identity.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.identity)
async def with_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        "Marhamat, murojaatingizni yozing:",
        reply_markup=ReplyKeyboardRemove()
    )
    await Form.text.set()

@dp.message_handler(text="🙈 Anonim", state=Form.identity)
async def anonymous(message: types.Message, state: FSMContext):
    await state.update_data(phone="Anonim")
    await message.answer(
        "Marhamat, murojaatingizni yozing:",
        reply_markup=ReplyKeyboardRemove()
    )
    await Form.text.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=Form.text)
async def receive_text(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await bot.send_message(
        ADMIN_ID,
        f"🆕 Yangi murojaat\n"
        f"📌 Turi: {data['category']}\n"
        f"📞 Aloqa: {data['phone']}\n"
        f"👤 @{message.from_user.username or 'username yo‘q'}\n"
        f"📝 {message.text}"
    )

    await message.answer(
        "Rahmat! Murojaatingiz qabul qilindi ✅",
        reply_markup=category_kb
    )

    await state.finish()

# ================= START =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
