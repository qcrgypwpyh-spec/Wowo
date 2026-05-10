import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application, CommandHandler, CallbackQueryHandler,
MessageHandler, filters, ContextTypes
)

# ─── Настройки ────────────────────────────────────────────────────────────────

BOT_TOKEN = “8566763615:AAEIKXD2u0vTItPL1N9xLINugLirIJMje5U”

logging.basicConfig(
format=”%(asctime)s - %(name)s - %(levelname)s - %(message)s”,
level=logging.INFO
)
logger = logging.getLogger(**name**)

# ─── Данные центра ─────────────────────────────────────────────────────────────

ABOUT_TEXT = “””
🐾 *WoWo Grooming Centre*

Мы — профессиональный груминг-центр, где каждый питомец получает
заботу и красоту с любовью! ✨

🌟 *Почему выбирают нас:*
• Опытные грумеры с сертификатами
• Только безопасная косметика для животных
• Индивидуальный подход к каждому питомцу
• Уютная атмосфера без стресса
• Фото после процедуры в подарок 📸

📞 Телефон: +7 (999) 123-45-67
📧 Email: wowo@grooming.ru
🌐 Instagram: @wowo_grooming
“””

BRANCHES = {
“branch_1”: {
“name”: “🏙 Филиал на Центральной”,
“address”: “ул. Центральная, д. 15”,
“hours”: “Пн–Вс: 9:00 – 21:00”,
“phone”: “+7 (999) 111-11-11”,
“map”: “https://maps.google.com/?q=Центральная+15”,
},
“branch_2”: {
“name”: “🌿 Филиал на Лесной”,
“address”: “ул. Лесная, д. 42”,
“hours”: “Пн–Вс: 10:00 – 20:00”,
“phone”: “+7 (999) 222-22-22”,
“map”: “https://maps.google.com/?q=Лесная+42”,
},
“branch_3”: {
“name”: “🛍 Филиал в ТЦ Радуга”,
“address”: “ТЦ Радуга, 2 этаж”,
“hours”: “Пн–Вс: 10:00 – 22:00”,
“phone”: “+7 (999) 333-33-33”,
“map”: “https://maps.google.com/?q=ТЦ+Радуга”,
},
}

PRODUCTS = {
“shampoo”: {
“name”: “🧴 Шампунь WoWo Pro”,
“desc”: “Профессиональный шампунь для всех типов шерсти. Без парабенов.”,
“price”: “590 ₽”,
},
“conditioner”: {
“name”: “💧 Кондиционер WoWo Soft”,
“desc”: “Увлажняет и распутывает шерсть. Приятный аромат.”,
“price”: “490 ₽”,
},
“perfume”: {
“name”: “🌸 Туалетная вода для питомцев”,
“desc”: “Лёгкий аромат для вашего любимца. Гипоаллергенно.”,
“price”: “350 ₽”,
},
“brush”: {
“name”: “🖌 Щётка-пуходёрка”,
“desc”: “Профессиональная расчёска для ежедневного ухода.”,
“price”: “780 ₽”,
},
“bow”: {
“name”: “🎀 Набор бантиков”,
“desc”: “Яркие аксессуары для стильного образа. 10 штук в наборе.”,
“price”: “290 ₽”,
},
}

# ─── Клавиатуры ───────────────────────────────────────────────────────────────

def main_menu_keyboard():
return InlineKeyboardMarkup([
[InlineKeyboardButton(“🛒 Заказать товары”, callback_data=“menu_products”)],
[InlineKeyboardButton(“📍 Выбрать филиал”, callback_data=“menu_branches”)],
[InlineKeyboardButton(“ℹ️ О нас”, callback_data=“menu_about”)],
])

def products_keyboard():
buttons = []
for key, product in PRODUCTS.items():
buttons.append([InlineKeyboardButton(
f”{product[‘name’]} — {product[‘price’]}”,
callback_data=f”product_{key}”
)])
buttons.append([InlineKeyboardButton(“⬅️ Назад”, callback_data=“back_main”)])
return InlineKeyboardMarkup(buttons)

def product_detail_keyboard(product_key: str):
return InlineKeyboardMarkup([
[InlineKeyboardButton(“✅ Заказать этот товар”, callback_data=f”order_{product_key}”)],
[InlineKeyboardButton(“⬅️ К товарам”, callback_data=“menu_products”)],
])

def branches_keyboard():
buttons = []
for key, branch in BRANCHES.items():
buttons.append([InlineKeyboardButton(branch[“name”], callback_data=f”branch_{key.split(’_’)[1]}”)])
buttons.append([InlineKeyboardButton(“⬅️ Назад”, callback_data=“back_main”)])
return InlineKeyboardMarkup(buttons)

def branch_detail_keyboard(map_url: str):
return InlineKeyboardMarkup([
[InlineKeyboardButton(“🗺 Открыть карту”, url=map_url)],
[InlineKeyboardButton(“📞 Записаться по телефону”, callback_data=“call_us”)],
[InlineKeyboardButton(“⬅️ К филиалам”, callback_data=“menu_branches”)],
])

def back_to_main_keyboard():
return InlineKeyboardMarkup([
[InlineKeyboardButton(“🏠 Главное меню”, callback_data=“back_main”)]
])

# ─── Хэндлеры ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.effective_user
text = (
f”Привет, {user.first_name}! 🐶🐱\n\n”
“Добро пожаловать в *WoWo Grooming Centre* — “
“место, где ваш питомец станет ещё красивее! ✨\n\n”
“Выберите, что вас интересует:”
)
await update.message.reply_text(
text,
parse_mode=“Markdown”,
reply_markup=main_menu_keyboard()
)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()
data = query.data

```
# ── Главное меню ──
if data == "back_main":
    await query.edit_message_text(
        "🐾 *WoWo Grooming Centre*\n\nВыберите раздел:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# ── О нас ──
elif data == "menu_about":
    await query.edit_message_text(
        ABOUT_TEXT,
        parse_mode="Markdown",
        reply_markup=back_to_main_keyboard()
    )

# ── Список товаров ──
elif data == "menu_products":
    await query.edit_message_text(
        "🛒 *Наши товары*\n\nВыберите товар для подробного описания:",
        parse_mode="Markdown",
        reply_markup=products_keyboard()
    )

# ── Детали товара ──
elif data.startswith("product_"):
    key = data.replace("product_", "")
    if key in PRODUCTS:
        p = PRODUCTS[key]
        text = (
            f"{p['name']}\n\n"
            f"📝 {p['desc']}\n\n"
            f"💰 Цена: *{p['price']}*"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=product_detail_keyboard(key)
        )

# ── Заказ товара ──
elif data.startswith("order_"):
    key = data.replace("order_", "")
    if key in PRODUCTS:
        p = PRODUCTS[key]
        text = (
            f"✅ Вы хотите заказать:\n*{p['name']}* — {p['price']}\n\n"
            "Для оформления заказа, пожалуйста, свяжитесь с нами:\n"
            "📞 *+7 (999) 123-45-67*\n"
            "или напишите в Instagram: *@wowo_grooming*\n\n"
            "Мы ответим в течение 15 минут! 🐾"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )

# ── Список филиалов ──
elif data == "menu_branches":
    await query.edit_message_text(
        "📍 *Наши филиалы*\n\nВыберите удобный для вас:",
        parse_mode="Markdown",
        reply_markup=branches_keyboard()
    )

# ── Детали филиала ──
elif data.startswith("branch_"):
    num = data.replace("branch_", "")
    key = f"branch_{num}"
    if key in BRANCHES:
        b = BRANCHES[key]
        text = (
            f"{b['name']}\n\n"
            f"📍 *Адрес:* {b['address']}\n"
            f"🕐 *Режим работы:* {b['hours']}\n"
            f"📞 *Телефон:* {b['phone']}"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=branch_detail_keyboard(b["map"])
        )

# ── Позвонить ──
elif data == "call_us":
    await query.edit_message_text(
        "📞 *Свяжитесь с нами*\n\n"
        "Позвоните на любой номер или запишитесь онлайн:\n\n"
        "• Центральная: +7 (999) 111-11-11\n"
        "• Лесная: +7 (999) 222-22-22\n"
        "• ТЦ Радуга: +7 (999) 333-33-33\n\n"
        "Мы рады помочь! 🐾",
        parse_mode="Markdown",
        reply_markup=back_to_main_keyboard()
    )
```

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
“”“Любое текстовое сообщение → показываем меню.”””
await update.message.reply_text(
“Выберите раздел 👇”,
reply_markup=main_menu_keyboard()
)

# ─── Запуск ───────────────────────────────────────────────────────────────────

def main():
app = Application.builder().token(BOT_TOKEN).build()

```
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

logger.info("WoWo Bot запущен...")
app.run_polling(allowed_updates=Update.ALL_TYPES)
```

if **name** == “**main**”:
main()
