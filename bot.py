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

FILM_DATEI = "filme.json"
VIDEO_ORDNER = "videos"

# Ordner erstellen falls nicht vorhanden
if not os.path.exists(VIDEO_ORDNER):
    os.makedirs(VIDEO_ORDNER)

# Filme laden
def lade_filme():
    if not os.path.exists(FILM_DATEI):
        return []
    with open(FILM_DATEI, "r") as f:
        return json.load(f)

# Filme speichern
def speichere_filme(filme):
    with open(FILM_DATEI, "w") as f:
        json.dump(filme, f)

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Willkommen beim Film Manager!\n\nSende mir einfach einen Film 🎥")

# Liste Command
async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filme = lade_filme()

    if not filme:
        await update.message.reply_text("Keine Filme gespeichert.")
        return

    text = "📽️ Deine Filme:\n"
    for film in filme:
        text += f"\n🎬 {film['name']}"

    await update.message.reply_text(text)

# 🎥 VIDEO HANDLER (GANZ WICHTIG!)
async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    video = update.message.video

    file = await context.bot.get_file(video.file_id)

    dateiname = f"{video.file_unique_id}.mp4"
    pfad = os.path.join(VIDEO_ORDNER, dateiname)

    await file.download_to_drive(pfad)

    filme = lade_filme()
    filme.append({
        "name": dateiname,
        "pfad": pfad
    })

    speichere_filme(filme)

    await update.message.reply_text("✅ Film gespeichert!")

# MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("liste", liste))

    # 👇 Damit Videos funktionieren!
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
