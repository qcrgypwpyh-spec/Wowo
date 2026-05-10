import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application, CommandHandler, CallbackQueryHandler,
MessageHandler, filters, ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8566763615:AAE5UxnpvRiNzrwcz6YtD2ghHNpW9ZjC-pw")


logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
level=logging.INFO
)
logger = logging.getLogger(**name**)

ABOUT_TEXT = """
\U0001f43e *WoWo Grooming Centre*

\u041c\u044b \u2014 \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0433\u0440\u0443\u043c\u0438\u043d\u0433-\u0446\u0435\u043d\u0442\u0440, \u0433\u0434\u0435 \u043a\u0430\u0436\u0434\u044b\u0439 \u043f\u0438\u0442\u043e\u043c\u0435\u0446 \u043f\u043e\u043b\u0443\u0447\u0430\u0435\u0442 \u0437\u0430\u0431\u043e\u0442\u0443 \u0438 \u043a\u0440\u0430\u0441\u043e\u0442\u0443 \u0441 \u043b\u044e\u0431\u043e\u0432\u044c\u044e! \u2728

\U0001f31f *\u041f\u043e\u0447\u0435\u043c\u0443 \u0432\u044b\u0431\u0438\u0440\u0430\u044e\u0442 \u043d\u0430\u0441:*
\u2022 \u041e\u043f\u044b\u0442\u043d\u044b\u0435 \u0433\u0440\u0443\u043c\u0435\u0440\u044b \u0441 \u0441\u0435\u0440\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u0430\u043c\u0438
\u2022 \u0422\u043e\u043b\u044c\u043a\u043e \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u0430\u044f \u043a\u043e\u0441\u043c\u0435\u0442\u0438\u043a\u0430 \u0434\u043b\u044f \u0436\u0438\u0432\u043e\u0442\u043d\u044b\u0445
\u2022 \u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u043e\u0434\u0445\u043e\u0434 \u043a \u043a\u0430\u0436\u0434\u043e\u043c\u0443 \u043f\u0438\u0442\u043e\u043c\u0446\u0443
\u2022 \u0423\u044e\u0442\u043d\u0430\u044f \u0430\u0442\u043c\u043e\u0441\u0444\u0435\u0440\u0430 \u0431\u0435\u0437 \u0441\u0442\u0440\u0435\u0441\u0441\u0430
\u2022 \u0424\u043e\u0442\u043e \u043f\u043e\u0441\u043b\u0435 \u043f\u0440\u043e\u0446\u0435\u0434\u0443\u0440\u044b \u0432 \u043f\u043e\u0434\u0430\u0440\u043e\u043a \U0001f4f8

\U0001f4de \u0422\u0435\u043b\u0435\u0444\u043e\u043d: +7 (999) 123-45-67
\U0001f4e7 Email: wowo@grooming.ru
\U0001f310 Instagram: @wowo_grooming
“””

BRANCHES = {
“branch_1”: {
"name": "\U0001f3d9 \u0424\u0438\u043b\u0438\u0430\u043b \u043d\u0430 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439",
"address": "\u0443\u043b. \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u0430\u044f, \u0434. 15",
“hours”: “\u041f\u043d\u2013\u0412\u0441: 9:00 \u2013 21:00”,
“phone”: “+7 (999) 111-11-11”,
“map”: “https://maps.google.com”,
},
“branch_2”: {
“name”: “\U0001f33f \u0424\u0438\u043b\u0438\u0430\u043b \u043d\u0430 \u041b\u0435\u0441\u043d\u043e\u0439”,
“address”: “\u0443\u043b. \u041b\u0435\u0441\u043d\u0430\u044f, \u0434. 42”,
“hours”: “\u041f\u043d\u2013\u0412\u0441: 10:00 \u2013 20:00”,
“phone”: “+7 (999) 222-22-22”,
“map”: “https://maps.google.com”,
},
“branch_3”: {
“name”: “\U0001f6cd \u0424\u0438\u043b\u0438\u0430\u043b \u0432 \u0422\u0426 \u0420\u0430\u0434\u0443\u0433\u0430”,
“address”: “\u0422\u0426 \u0420\u0430\u0434\u0443\u0433\u0430, 2 \u044d\u0442\u0430\u0436”,
“hours”: “\u041f\u043d\u2013\u0412\u0441: 10:00 \u2013 22:00”,
“phone”: “+7 (999) 333-33-33”,
“map”: “https://maps.google.com”,
},
}

PRODUCTS = {
“shampoo”: {
“name”: “\U0001f9f4 \u0428\u0430\u043c\u043f\u0443\u043d\u044c WoWo Pro”,
“desc”: “\u041f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0448\u0430\u043c\u043f\u0443\u043d\u044c \u0434\u043b\u044f \u0432\u0441\u0435\u0445 \u0442\u0438\u043f\u043e\u0432 \u0448\u0435\u0440\u0441\u0442\u0438.”,
“price”: “590 \u20bd”,
},
“conditioner”: {
“name”: “\U0001f4a7 \u041a\u043e\u043d\u0434\u0438\u0446\u0438\u043e\u043d\u0435\u0440 WoWo Soft”,
“desc”: “\u0423\u0432\u043b\u0430\u0436\u043d\u044f\u0435\u0442 \u0438 \u0440\u0430\u0441\u043f\u0443\u0442\u044b\u0432\u0430\u0435\u0442 \u0448\u0435\u0440\u0441\u0442\u044c.”,
“price”: “490 \u20bd”,
},
“perfume”: {
“name”: “\U0001f338 \u0422\u0443\u0430\u043b\u0435\u0442\u043d\u0430\u044f \u0432\u043e\u0434\u0430 \u0434\u043b\u044f \u043f\u0438\u0442\u043e\u043c\u0446\u0435\u0432”,
“desc”: “\u041b\u0451\u0433\u043a\u0438\u0439 \u0430\u0440\u043e\u043c\u0430\u0442. \u0413\u0438\u043f\u043e\u0430\u043b\u043b\u0435\u0440\u0433\u0435\u043d\u043d\u043e.”,
“price”: “350 \u20bd”,
},
“brush”: {
“name”: “\U0001f58c \u0429\u0451\u0442\u043a\u0430-\u043f\u0443\u0445\u043e\u0434\u0451\u0440\u043a\u0430”,
“desc”: “\u041f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u0440\u0430\u0441\u0447\u0451\u0441\u043a\u0430 \u0434\u043b\u044f \u0435\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u043e\u0433\u043e \u0443\u0445\u043e\u0434\u0430.”,
“price”: “780 \u20bd”,
},
“bow”: {
“name”: “\U0001f380 \u041d\u0430\u0431\u043e\u0440 \u0431\u0430\u043d\u0442\u0438\u043a\u043e\u0432”,
“desc”: “\u042f\u0440\u043a\u0438\u0435 \u0430\u043a\u0441\u0435\u0441\u0441\u0443\u0430\u0440\u044b. 10 \u0448\u0442\u0443\u043a \u0432 \u043d\u0430\u0431\u043e\u0440\u0435.”,
“price”: “290 \u20bd”,
},
}

def main_menu_keyboard():
return InlineKeyboardMarkup([
[InlineKeyboardButton(”\U0001f6d2 \u0417\u0430\u043a\u0430\u0437\u0430\u0442\u044c \u0442\u043e\u0432\u0430\u0440\u044b”, callback_data=“menu_products”)],
[InlineKeyboardButton(”\U0001f4cd \u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0438\u043b\u0438\u0430\u043b”, callback_data=“menu_branches”)],
[InlineKeyboardButton(”\u2139\ufe0f \u041e \u043d\u0430\u0441”, callback_data=“menu_about”)],
])

def products_keyboard():
buttons = []
for key, product in PRODUCTS.items():
buttons.append([InlineKeyboardButton(
product[“name”] + “ — “ + product[“price”],
callback_data=“product_” + key
)])
buttons.append([InlineKeyboardButton(”\u2b05\ufe0f \u041d\u0430\u0437\u0430\u0434”, callback_data=“back_main”)])
return InlineKeyboardMarkup(buttons)

def product_detail_keyboard(product_key):
return InlineKeyboardMarkup([
[InlineKeyboardButton(”\u2705 \u0417\u0430\u043a\u0430\u0437\u0430\u0442\u044c \u044d\u0442\u043e\u0442 \u0442\u043e\u0432\u0430\u0440”, callback_data=“order_” + product_key)],
[InlineKeyboardButton(”\u2b05\ufe0f \u041a \u0442\u043e\u0432\u0430\u0440\u0430\u043c”, callback_data=“menu_products”)],
])

def branches_keyboard():
buttons = []
for key, branch in BRANCHES.items():
num = key.split(”*”)[1]
buttons.append([InlineKeyboardButton(branch[“name”], callback_data=“branch*” + num)])
buttons.append([InlineKeyboardButton(”\u2b05\ufe0f \u041d\u0430\u0437\u0430\u0434”, callback_data=“back_main”)])
return InlineKeyboardMarkup(buttons)

def branch_detail_keyboard(map_url):
return InlineKeyboardMarkup([
[InlineKeyboardButton(”\U0001f5fa \u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043a\u0430\u0440\u0442\u0443”, url=map_url)],
[InlineKeyboardButton(”\U0001f4de \u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c\u0441\u044f”, callback_data=“call_us”)],
[InlineKeyboardButton(”\u2b05\ufe0f \u041a \u0444\u0438\u043b\u0438\u0430\u043b\u0430\u043c”, callback_data=“menu_branches”)],
])

def back_to_main_keyboard():
return InlineKeyboardMarkup([
[InlineKeyboardButton(”\U0001f3e0 \u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e”, callback_data=“back_main”)]
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.effective_user
text = (
“\u041f\u0440\u0438\u0432\u0435\u0442, “ + user.first_name + “! \U0001f436\U0001f431\n\n”
“\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c \u0432 *WoWo Grooming Centre* \u2014 “
“\u043c\u0435\u0441\u0442\u043e, \u0433\u0434\u0435 \u0432\u0430\u0448 \u043f\u0438\u0442\u043e\u043c\u0435\u0446 \u0441\u0442\u0430\u043d\u0435\u0442 \u0435\u0449\u0451 \u043a\u0440\u0430\u0441\u0438\u0432\u0435\u0435! \u2728\n\n”
“\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435, \u0447\u0442\u043e \u0432\u0430\u0441 \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u0443\u0435\u0442:”
)
await update.message.reply_text(text, parse_mode=“Markdown”, reply_markup=main_menu_keyboard())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()
data = query.data

```
if data == "back_main":
    await query.edit_message_text(
        "\U0001f43e *WoWo Grooming Centre*\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0440\u0430\u0437\u0434\u0435\u043b:",
        parse_mode="Markdown", reply_markup=main_menu_keyboard()
    )
elif data == "menu_about":
    await query.edit_message_text(ABOUT_TEXT, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
elif data == "menu_products":
    await query.edit_message_text(
        "\U0001f6d2 *\u041d\u0430\u0448\u0438 \u0442\u043e\u0432\u0430\u0440\u044b*\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0442\u043e\u0432\u0430\u0440:",
        parse_mode="Markdown", reply_markup=products_keyboard()
    )
elif data.startswith("product_"):
    key = data.replace("product_", "")
    if key in PRODUCTS:
        p = PRODUCTS[key]
        text = p["name"] + "\n\n\U0001f4dd " + p["desc"] + "\n\n\U0001f4b0 \u0426\u0435\u043d\u0430: *" + p["price"] + "*"
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=product_detail_keyboard(key))
elif data.startswith("order_"):
    key = data.replace("order_", "")
    if key in PRODUCTS:
        p = PRODUCTS[key]
        text = (
            "\u2705 \u0412\u044b \u0445\u043e\u0442\u0438\u0442\u0435 \u0437\u0430\u043a\u0430\u0437\u0430\u0442\u044c:\n*" + p["name"] + "* \u2014 " + p["price"] + "\n\n"
            "\u0414\u043b\u044f \u043e\u0444\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u044f \u0437\u0430\u043a\u0430\u0437\u0430:\n"
            "\U0001f4de *+7 (999) 123-45-67*\n"
            "\u0438\u043b\u0438 Instagram: *@wowo_grooming*\n\n"
            "\u041c\u044b \u043e\u0442\u0432\u0435\u0442\u0438\u043c \u0432 \u0442\u0435\u0447\u0435\u043d\u0438\u0435 15 \u043c\u0438\u043d\u0443\u0442! \U0001f43e"
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
elif data == "menu_branches":
    await query.edit_message_text(
        "\U0001f4cd *\u041d\u0430\u0448\u0438 \u0444\u0438\u043b\u0438\u0430\u043b\u044b*\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0443\u0434\u043e\u0431\u043d\u044b\u0439 \u0434\u043b\u044f \u0432\u0430\u0441:",
        parse_mode="Markdown", reply_markup=branches_keyboard()
    )
elif data.startswith("branch_"):
    num = data.replace("branch_", "")
    key = "branch_" + num
    if key in BRANCHES:
        b = BRANCHES[key]
        text = (
            b["name"] + "\n\n"
            "\U0001f4cd *\u0410\u0434\u0440\u0435\u0441:* " + b["address"] + "\n"
            "\U0001f550 *\u0420\u0435\u0436\u0438\u043c:* " + b["hours"] + "\n"
            "\U0001f4de *\u0422\u0435\u043b\u0435\u0444\u043e\u043d:* " + b["phone"]
        )
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=branch_detail_keyboard(b["map"]))
elif data == "call_us":
    text = (
        "\U0001f4de *\u0421\u0432\u044f\u0436\u0438\u0442\u0435\u0441\u044c \u0441 \u043d\u0430\u043c\u0438*\n\n"
        "\u2022 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u0430\u044f: +7 (999) 111-11-11\n"
        "\u2022 \u041b\u0435\u0441\u043d\u0430\u044f: +7 (999) 222-22-22\n"
        "\u2022 \u0422\u0426 \u0420\u0430\u0434\u0443\u0433\u0430: +7 (999) 333-33-33\n\n"
        "\U0001f43e \u041c\u044b \u0440\u0430\u0434\u044b \u043f\u043e\u043c\u043e\u0447\u044c!"
    )
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
```

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0440\u0430\u0437\u0434\u0435\u043b \U0001f447”,
reply_markup=main_menu_keyboard()
)

def main():
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler(“start”, start))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
logger.info(“WoWo Bot started!”)
app.run_polling(allowed_updates=Update.ALL_TYPES)

if **name** == “**main**”:
main()
