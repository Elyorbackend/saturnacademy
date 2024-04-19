from aiogram import Bot, Dispatcher, executor
from keyboards import *
from states import RegisterStatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from configs import TOKEN
from aiogram import types

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

course = None


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Assalomu aleykum, savolingiz bo'yicha ma'lumot olish uchun quyidagilardan birini tanlang:",
                         reply_markup=markup())
@dp.message_handler(commands=['security'])
async def security(message: types.Message):
    await bot.send_message(message.chat.id,message.from_user.username)


@dp.message_handler(text=["🔙Ortga"])
async def ortga(message: types.Message):
    await message.answer("quyidagilardan birini tanlang:", reply_markup=markup())


@dp.message_handler(text=["🚗Manzilimiz"])
async def manzilimiz(message: types.Message):
    await message.answer(
        '<a href="https://maps.app.goo.gl/DkipgJYrD5E6Tg95A">Bizning Manzilimiz</a>',
        reply_markup=ortga_qaytish(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(text=["💵Narxlarimiz"])
async def narx(message: types.Message):
    await message.answer(
        "Bizning kurslarimizning narxlarini ko'rsangiz boladi:\n💻IT - 1.000.000so'm,\n🇺🇸English - 400.000so'm ,\n➕Matematika - 400.000so'm,\n🇷🇺Rus tili - 400.000so'm,\n🧠Mnemonika - 500.000so'm,\n✍️Pochemuchka - 500.000so'm,\n🎓IELTS - 600.000so'm,\n➕➖Mental arifmetika - 400.000so'm,\n🎨Rasm chizish - 700.000so'm,\n📊Marketing - 2.000.000so'm,\n♟Shaxmat - 500.000so'm",
        reply_markup=ortga_qaytish())


@dp.message_handler(text=["💻Ish bo'yicha"])
async def phone_number(message: types.Message):
    await message.answer("<a href='https://t.me/Saturn_Academy_Admin'>Murojat uchun</a>",
                         reply_markup=ortga_qaytish(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(text=["📞Biz bilan bog'lanish"])
async def boglanish(message: types.Message):
    await message.answer("<a href='https://t.me/Saturn_Academy_Admin'>Murojat uchun</a>",
                         reply_markup=ortga_qaytish(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(text=["❓Taklif va shikoyatlar"])
async def tf_va_sht(message: types.Message):
    await message.answer(
        "<a href='https://t.me/Dior_adrenalin'>Taklif yoki shikoyatingizni ularga yozsangiz bo'ladi</a>",
        reply_markup=ortga_qaytish(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(text=['📝Kursga yozilish'])
async def kursga_yozilish(message: types.Message):
    await message.answer("Quyidagi kurslardan yozilmoqchi bo'lganingizni tanlang:", reply_markup=courses())


# @dp.message_handler(text=["✉️Ijtimoiy tarmoqlar"])
# async def phone_number(message: types.Message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     btn1 = types.InlineKeyboardButton("telegram:", url='https://t.me/saturn_on_academy1'),
#     btn2 = types.InlineKeyboardButton("instagram:",
#                                       url='https://instagram.com/saturn_on_academy?igshid=MzRlODBiNWFlZA=='),
#     markup.add(btn1, btn2)
#     await message.answer("Ijtimoiy tarmoqlarimiz:", reply_markup=markup)


@dp.message_handler(text=['💻IT'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}
        telegram akkaunt: https://t.me/{message.from_user.username}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['🇺🇸English'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['➕Matematika'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['🇷🇺Rus tili'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['🧠Mnemonika'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['❔Pochemuchka'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['🎓IELTS'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['➕➖Mental arifmetika'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['🎨Rasm chizish'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['📊Marketing'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['♟Shaxmat'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


@dp.message_handler(text=['💻IT'])
async def ask_user_full_name(message: Message):
    global course
    course = message.text.split()
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"""<b>Ism va familiyangizni yozing: 👤</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.full_name.set()


@dp.message_handler(content_types=['text'], state=RegisterStatesGroup.full_name)
async def ask_user_contact(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_full_name = message.text
    async with state.proxy() as data:
        data[chat_id] = {
            "chat_id": chat_id,
            "full_name": user_full_name
        }
        print(data)
    await bot.send_message(chat_id, f"""<b>Telefon raqamingizni jonating: 📱</b>""", parse_mode=types.ParseMode.HTML)
    await RegisterStatesGroup.contact.set()


@dp.message_handler(content_types=['contact', 'text'],
                    state=RegisterStatesGroup.contact)
async def ask_submitting_user_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'contact':
        user_contact = message.contact.phone_number
    elif message.content_type == 'text':
        user_contact = message.text
        async with state.proxy() as data:

            data[chat_id].update({"contact": user_contact})
            print(data)
            await RegisterStatesGroup.full_name.set()
            await RegisterStatesGroup.submitting.set()
            await message.answer("Ma'lumotlaringizni tasdiqlang:", reply_markup=tasdiqlash())

    @dp.message_handler(state=RegisterStatesGroup.submitting)
    async def checking_user_answer_for_submitting(message: Message, state: FSMContext):
        chat_id = message.chat.id
        if message.text == "Tasdiqlash ✅":
            async with state.proxy() as data:
                fullname = data[chat_id]['full_name']
                contact = data[chat_id]['contact']

                await bot.send_message("-1002043647569", f"""Yangi foydalanuvchining malumotlari:
        Kursi: {course}
        Ism-familiyasi:  {fullname}
        Telefon nomeri:  {contact}""")
                data.pop(chat_id)
                await state.finish()
                await bot.send_message(message.chat.id,
                                       "Siz muvaffaqiyatli registratsiyadan o'tdingiz 'Saturn academy'dan yana ma'lumot olish uchun quyidagilardan birini tanlang: ",
                                       reply_markup=markup())


if __name__ == '__main__':
    executor.start_polling(dp)
