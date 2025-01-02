import os
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# Telegram bot tokeni
TOKEN = "7761216602:AAHjsWdWqS8yLcwTDMZ6fuyAwbxXoWxFh1k"  # O'z tokeningizni shu yerga kiriting


# YouTube videolarini yuklash funksiyasi
def download_youtube_video(url, download_path="downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)  # Yuklab olish uchun katalog yaratish
    options = {
        'format': 'mp4/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)  # Yuklangan fayl yo'lini qaytaradi


# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Men YouTube videolarini yuklab beruvchi botman. "
        "Menga har qanday YouTube havolasini yuboring."
    )


# YouTube videoni yuklab olish va jo'natish
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text.strip()
    try:
        await update.message.reply_text("Videoni yuklab olishni boshlayapman. Iltimos, kuting...")

        # Videoni yuklab olish
        file_path = download_youtube_video(url)

        # Yuklangan videoni foydalanuvchiga yuborish
        with open(file_path, "rb") as video:
            await update.message.reply_video(video=video)

        # Yuklangan faylni o'chirish
        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")


# Asosiy dastur
if __name__ == "__main__":
    # Botni ishga tushirish
    application = Application.builder().token(TOKEN).build()

    # Komanda va xabar handlerlarini qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot ishlayapti...")
    application.run_polling()
