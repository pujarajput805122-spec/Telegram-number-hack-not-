
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random

TOKEN = "8780643023:AAGySmrmk4WD9W5WW9mKc7IsjSQfbaPWM4M"

history = [
("Green","Big"),("Red","Big"),("Green","Big"),("Red","Small"),
("Red","Small"),("Red","Small"),("Red","Small"),("Green","Small"),
("Red+Violet","Big"),("Green","Small"),("Red+Violet","Small"),
("Red","Small"),("Red","Big"),("Green+Violet","Big"),
("Green","Small"),("Green","Big"),("Green","Big"),("Green","Big"),
("Red","Big"),("Green","Small"),("Green","Big"),("Green","Small"),
("Green","Big"),("Red+Violet","Small"),("Red","Big"),("Green","Big"),
("Green","Small"),("Red","Small"),("Red","Big"),("Red","Big"),
("Green","Big"),("Green","Small"),("Green","Small"),("Green","Big"),
("Red","Big"),("Green","Small"),("Red+Violet","Small"),
("Red+Violet","Small"),("Green+Violet","Big"),("Green","Small"),
("Red","Small"),("Green","Big"),("Red","Big"),("Red+Violet","Small"),
("Red","Small"),("Green","Big"),("Green","Big"),("Red","Big"),
("Red","Small"),("Green","Small"),("Red","Small"),("Green","Big"),
("Green","Big"),("Red+Violet","Small"),("Green","Small"),
("Red","Small"),("Green","Small"),("Red+Violet","Small"),
("Red","Small"),("Green","Small"),("Red","Small"),("Red","Big")
]

user_step = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔐 REGISTER NOW", url="https://www.jaiclub14.com/#/register?invitationCode=38562107009")],
        [InlineKeyboardButton("📢 JOIN CHANNEL 1", url="https://t.me/+L-nAD5nRXCBlNTA1")],
        [InlineKeyboardButton("📢 JOIN CHANNEL 2", url="https://t.me/shelbyykachannelhaibsdk")],
        [InlineKeyboardButton("✅ I HAVE COMPLETED ALL", callback_data="joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📌 STEP 1: REGISTER KRO\n"
        "📌 STEP 2: DONO CHANNEL JOIN KRO\n\n"
        "USKE BAAD BUTTON CLICK KRO 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# BUTTON
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "joined":
        user_step[query.from_user.id] = "ENTER_PERIOD"
        await query.message.reply_text(
            "🧠 AB 30 SEC PERIOD NUMBER ENTER KRO:",
            parse_mode="Markdown"
        )

# MESSAGE
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if user_step.get(user_id) != "ENTER_PERIOD":
        await update.message.reply_text("❌ PEHLE /start DABAO", parse_mode="Markdown")
        return

    if update.message.text.isdigit():
        period = int(update.message.text)

        prediction = analyze_real_data()

        keyboard = [
            [InlineKeyboardButton("📊 SHOW RESULT", callback_data=f"result_{prediction}")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"📊 PERIOD: {period}\nPREDICTION READY ✅",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# RESULT
async def result_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_",1)[1]

    await query.message.reply_text(
        f"🔮 PREDICTION RESULT:\n{data}",
        parse_mode="Markdown"
    )

# ANALYSIS
def analyze_real_data():
    last_data = history[-20:]   # thoda bada sample liya

    green = sum(1 for c, s in last_data if "Green" in c)
    red = sum(1 for c, s in last_data if "Red" in c)

    big = sum(1 for c, s in last_data if s == "Big")
    small = sum(1 for c, s in last_data if s == "Small")

    # 🔥 LAST TREND CHECK (pattern)
    last_colors = [c for c, s in last_data[-3:]]
    last_sizes = [s for c, s in last_data[-3:]]

    # 🎯 COLOR LOGIC
    if last_colors.count(last_colors[-1]) >= 2:
        # agar same 2–3 baar aya → change karo
        color = "Red" if "Green" in last_colors[-1] else "Green"
    else:
        # warna majority follow karo
        color = "Green" if green >= red else "Red"

    # 🎯 SIZE LOGIC
    if last_sizes.count(last_sizes[-1]) >= 2:
        size = "Small" if last_sizes[-1] == "Big" else "Big"
    else:
        size = "Big" if big >= small else "Small"

    # 🎯 NUMBER PICK (controlled)
    if size == "Big":
        possible = [5, 6, 7, 8, 9]
    else:
        possible = [0, 1, 2, 3, 4]

    number = random.choice(possible)

    # 🎯 VIOLET CONTROL (pattern ke hisaab se rare)
    violet_count = sum(1 for c, s in last_data if "Violet" in c)

    if number in [0, 5] and violet_count < 3:
        color += " + Violet"

    return f"{color} | {size} | Number: {number}"

# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button, pattern="joined"))
app.add_handler(CallbackQueryHandler(result_button, pattern="result_"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

print("Bot Running...")
app.run_polling()
