from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7867528322:AAHrXGZ6sTJdYKZ_MCqsOlY3njaM5PFPFV0'  # Substitua pelo token do BotFather

# Função para lidar com o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Envia o texto
    await context.bot.send_message(chat_id=chat_id, text="Bem-vindo! Aqui está o vídeo que prometi:")

    # Envia o vídeo (pode ser um arquivo local ou URL)
    await context.bot.send_video(chat_id=chat_id, video=open('https://firebasestorage.googleapis.com/v0/b/typebot-7660e.appspot.com/o/video_2025-06-09_15-12-24.mp4?alt=media&token=b58e3913-43e6-42ff-8f3e-2bbc0b0f604a', 'rb'))  # ou use uma URL no lugar de open(...)

# Roda o bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
