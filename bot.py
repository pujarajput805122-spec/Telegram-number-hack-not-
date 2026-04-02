
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8780643023:AAGySmrmk4WD9W5WW9mKc7IsjSQfbaPWM4M")


user_step = {}

# 🔥 FULL DATA (700–800)
data_list = [
("20260402100050700","9","Green","Big"),
("20260402100050701","8","Red","Big"),
("20260402100050702","9","Green","Big"),
("20260402100050703","4","Red","Small"),
("20260402100050704","4","Red","Small"),
("20260402100050705","3","Red","Small"),
("20260402100050706","2","Red","Small"),
("20260402100050707","3","Green","Small"),
("20260402100050708","5","Red+Violet","Big"),
("20260402100050709","3","Green","Small"),
("20260402100050710","0","Red+Violet","Small"),
# 👉 (tu chahe to pura list yaha continue kar sakta hai)
]

# 🔍 JOIN CHECK
async def check_join(user_id, context):
    try:
        m1 = await context.bot.get_chat_member(CHANNEL_1, user_id)
        m2 = await context.bot.get_chat_member(CHANNEL_2, user_id)

        return m1.status in ["member","administrator","creator"] and m2.status in ["member","administrator","creator"]
    except:
        return False

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ OK", callback_data="ok")]]
    text = "🚨🔥 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥 𝗣𝗘 𝗖𝗟𝗜𝗖𝗞 𝗞𝗔𝗥𝗢 🔥🚨"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# 👉 NEXT UI
async def ok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton("🔥 REGISTER 🔥", url="https://www.jaiclub14.com/#/register?invitationCode=38562107009")],
        [InlineKeyboardButton("📢 CHANNEL 1", url="https://t.me/+L-nAD5nRXCBlNTA1")],
        [InlineKeyboardButton("📢 CHANNEL 2", url="https://t.me/shelbyykachannelhaibsdk")],
        [InlineKeyboardButton("✅ VERIFY", callback_data="verify")]
    ]

    await q.message.edit_text("🚀 COMPLETE STEPS 🚀", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# 👉 VERIFY
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if not await check_join(q.from_user.id, context):
        await q.message.reply_text("❌ JOIN CHANNEL FIRST ❌", parse_mode="Markdown")
        return

    user_step[q.from_user.id] = True
    await q.message.reply_text("🧠 PERIOD NUMBER ENTER KARO:", parse_mode="Markdown")

# 🔥 PATTERN LOGIC (MAIN)
def predict(period):

    # find index
    index = None
    for i, d in enumerate(data_list):
        if d[0] == period:
            index = i
            break

    # 🎯 CASE 1: pattern found
    if index is not None and index+3 < len(data_list):
        next_data = data_list[index+1:index+4]

        colors = [d[2] for d in next_data]
        sizes = [d[3] for d in next_data]

        # majority logic
        color = max(set(colors), key=colors.count)
        size = max(set(sizes), key=sizes.count)

        if size == "Big":
            num = random.choice([5,6,7,8,9])
        else:
            num = random.choice([0,1,2,3,4])

        return color, size, num

    # 🎯 CASE 2: fallback pattern
    colors = [d[2] for d in data_list[-15:]]
    sizes = [d[3] for d in data_list[-15:]]

    color = max(set(colors), key=colors.count)
    size = max(set(sizes), key=sizes.count)

    if size == "Big":
        num = random.choice([5,6,7,8,9])
    else:
        num = random.choice([0,1,2,3,4])

    return color, size, num

# 📩 MESSAGE
async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if not user_step.get(user_id):
        await update.message.reply_text("❌ PEHLE /start DABAO ❌", parse_mode="Markdown")
        return

    period = update.message.text.strip()

    color, size, num = predict(period)

text = (
        "🔥🎯 FINAL RESULT 🎯🔥\n\n"
        f"🎨 COLOR: {color}\n"
        f"📊 SIZE: {size}\n"
        f"🔢 NUMBER: {num}"
    )

    await update.message.reply_text(text, parse_mode="Markdown")

# 🚀 MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(ok, pattern="ok"))
app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))

print("Bot Running...")
app.run_polling()
