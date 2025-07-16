from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters
import csv

TOKEN = "7776065669:AAEWGA0PI1Hs0NwuNTRQUGU8Atkeuhbetdg"

# مراحل گفت‌وگو
NAME, AGE, GENDER = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Veteriner asistan botuna hoş geldiniz 🐾\nLütfen adınızı yazınız:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["owner_name"] = update.message.text
    await update.message.reply_text("Hayvanınızın yaşını giriniz (örnek: 3 yaş):")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pet_age"] = update.message.text

    keyboard = [["Erkek", "Dişi"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Lütfen hayvanınızın cinsiyetini seçiniz:", reply_markup=reply_markup)
    return GENDER

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pet_gender"] = update.message.text

    # ذخیره اطلاعات در فایل CSV
    with open("data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([context.user_data["owner_name"], context.user_data["pet_age"], context.user_data["pet_gender"]])

    await update.message.reply_text("Bilgiler kaydedildi. Teşekkür ederiz 🐶🐱")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("İşlem iptal edildi.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gender)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
