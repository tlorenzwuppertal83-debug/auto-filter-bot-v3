import os
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN:", TOKEN)

FILM_DATEI = "filme.json"
VIDEO_ORDNER = "videos"

if not os.path.exists(VIDEO_ORDNER):
    os.makedirs(VIDEO_ORDNER)

if not os.path.exists(FILM_DATEI):
    with open(FILM_DATEI, "w") as f:
        json.dump([], f)

def lade_filme():
    with open(FILM_DATEI, "r") as f:
        return json.load(f)

def speichere_filme(filme):
    with open(FILM_DATEI, "w") as f:
        json.dump(filme, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Willkommen! Sende mir einen Film (Video) mit Titel als Caption.")

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    titel = update.message.caption

    if not titel:
        await update.message.reply_text("❗ Bitte sende das Video mit einem Titel in der Caption.")
        return

    file = await context.bot.get_file(video.file_id)
    dateipfad = os.path.join(VIDEO_ORDNER, f"{video.file_id}.mp4")
    await file.download_to_drive(dateipfad)

    filme = lade_filme()
    filme.append({"titel": titel, "datei": dateipfad})
    speichere_filme(filme)

    await update.message.reply_text(f"✅ Film '{titel}' gespeichert!")

async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filme = lade_filme()
    if not filme:
        await update.message.reply_text("📭 Keine Filme gespeichert.")
        return

    nachricht = "\n".join([f"{i+1}. {film['titel']}" for i, film in enumerate(filme)])
    await update.message.reply_text("🎞️ Gespeicherte Filme:\n" + nachricht)

async def suche(update: Update, context: ContextTypes.DEFAULT_TYPE):
    suchbegriff = " ".join(context.args).lower()
    filme = lade_filme()

    for film in filme:
        if suchbegriff in film["titel"].lower():
            with open(film["datei"], "rb") as v:
                await update.message.reply_video(video=v, caption=film["titel"])
            return

    await update.message.reply_text("❌ Kein Film gefunden.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("liste", liste))
    app.add_handler(CommandHandler("suche", suche))
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
