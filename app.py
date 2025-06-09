from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7867528322:AAHrXGZ6sTJdYKZ_MCqsOlY3njaM5PFPFV0'  # Coloque seu token aqui

# Função /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Envia o vídeo via URL
    video_url = 'https://firebasestorage.googleapis.com/v0/b/typebot-7660e.appspot.com/o/video_2025-06-09_15-12-24.mp4?alt=media&token=b58e3913-43e6-42ff-8f3e-2bbc0b0f604a'
    await context.bot.send_video(chat_id=chat_id, video=video_url)

    # Texto de venda
    texto = (
        "Só hoje: *Vitalício do Funk Clube por 5,00 + 2 grupos Bônus proibidos liberado na hora* ⚡️\n\n"
        "🔞 *+50k de mídias nunca vista na internet*\n"
        "🍿 *Recheado de N0vinhas safadas*\n"
        "😈 *Chat exclusivo e lotado de vídeos proibidos*\n\n"
        "👉🏽 *Vagas limitadas!!*\n\n"
        "⭐️ *Para fazer pagamento via Pix*\n\n"
        "Envie o valor de *5,90* nesse link: 👇🏻\n"
        "https://pay.sunize.com.br/mXoVtugT\n\n"
        "Depois é só enviar o comprovante para o suporte abaixo e você já vai estar *LIBERADO!* 😈🔥\n"
        "@supvipoficial"
    )

    # Envia o texto com formatação
    await context.bot.send_message(chat_id=chat_id, text=texto, parse_mode="Markdown")

# Inicializa o bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
