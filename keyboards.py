from aiogram import types


def markup():
    main = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("📝Kursga yozilish")
    btn2 = types.KeyboardButton('🚗Manzilimiz')
    btn3 = types.KeyboardButton('💵Narxlarimiz')
    btn4 = types.KeyboardButton("💻Ish bo'yicha")
    btn5 = types.KeyboardButton("📞Biz bilan bog'lanish")
    btn6 = types.KeyboardButton("❓Taklif va shikoyatlar")
    # btn7 = types.KeyboardButton("✉️Ijtimoiy tarmoqlar")
    main.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return main
def courses():
    main = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("💻IT")
    btn2 = types.KeyboardButton("🇺🇸English")
    btn3 = types.KeyboardButton("➕Matematika")
    btn4 = types.KeyboardButton("🇷🇺Rus tili")
    btn5 = types.KeyboardButton("🧠Mnemonika")
    btn6 = types.KeyboardButton("✍️Pochemuchka")
    btn7 = types.KeyboardButton("🎓IELTS")
    btn8 = types.KeyboardButton("➕➖Mental arifmetika")
    btn9 = types.KeyboardButton("🎨Rasm chizish")
    btn10 = types.KeyboardButton("📊Marketing")
    btn11 = types.KeyboardButton("♟Shaxmat")
    main.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    return main

def tasdiqlash():
    confirmation = types.ReplyKeyboardMarkup()
    btn17 = types.KeyboardButton("Tasdiqlash ✅")
    confirmation.add(btn17)
    return confirmation

def ortga_qaytish():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('🔙Ortga')
    markup.add(btn1)
    return markup

# def course():
#     kurs = types.ReplyKeyboardMarkup(row_width=2)
#     btn5 = types.KeyboardButton('💻IT')
#     btn6 = types.KeyboardButton('🧠Mnemonika')
#     btn7 = types.KeyboardButton('🔢Matematika')
#     btn8 = types.KeyboardButton('🔤Ingiliz tili')
#     btn9 = types.KeyboardButton('🔙Orqaga qaytish')
#     kurs.add(btn5, btn6, btn7, btn8, btn9)
#     return kurs
# def telegram():
#     tg = types.InlineKeyboardMarkup()
#     btn10 = types.InlineKeyboardButton("telegram:", url='https://t.me/saturn_on_academy1')
#     tg.add(btn10)
#     return tg
# def tarmoqlar():
#     tarmoq = types.InlineKeyboardMarkup()
#     btn11 = types.InlineKeyboardButton("instagram:", url='https://instagram.com/saturn_on_academy?igshid=MzRlODBiNWFlZA==')
#     tarmoq.add(btn11)
#     return tarmoq
# def it_course():
#     it = types.ReplyKeyboardMarkup(row_width=2)
#     btn12 = types.KeyboardButton('Backend')
#     btn13 = types.KeyboardButton('Frontend')
#     btn14 = types.KeyboardButton('🔙Menyuga qaytish')
#     it.add(btn12, btn13, btn14)
#     return it
# def back_1():
#     backend = types.InlineKeyboardMarkup(row_width=2)
#     btn15 = types.InlineKeyboardButton("Telegram", url="https://t.me/saturn_on_academy1")
#     backend.add(btn15)
#     return backend
# def front_1():
#     frontend = types.InlineKeyboardMarkup(row_width=2)
#     btn16 = types.InlineKeyboardButton("Telegram", url="https://t.me/saturn_on_academy1")
#     frontend.add(btn16)
#     return frontend
# def tasdiqlash():
#     confirmation = types.ReplyKeyboardMarkup()
#     btn17 = types.KeyboardButton("Tasdiqlash ✅")
#     confirmation.add(btn17)
#     return confirmation
