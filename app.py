import requests
import time

BOT_TOKEN = '8025992022:AAFQ2DrBKQPUuH-daCgWBqoEdevh8-pw7j8'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

last_update_id = None
user_products = {}

payment_links = {
    "produto_a": "https://pay.sunize.com.br/jEOvLGkU",
    "produto_b": "https://pay.sunize.com.br/xvCobaWe",
    "produto_c": "https://pay.sunize.com.br/lIdtYPEi"
}

video_previews = {
    "produto_a": ["https://firebasestorage.googleapis.com/v0/b/typebot-7660e.appspot.com/o/video_2025-06-05_18-26-30.mp4?alt=media&token=80414ba8-9123-401f-9953-38b03ed2e51d"],
    "produto_b": ["https://firebasestorage.googleapis.com/v0/b/typebot-7660e.appspot.com/o/video_2025-06-05_18-26-30.mp4?alt=media&token=80414ba8-9123-401f-9953-38b03ed2e51d"],
    "produto_c": ["https://firebasestorage.googleapis.com/v0/b/typebot-7660e.appspot.com/o/video_2025-06-05_18-26-30.mp4?alt=media&token=80414ba8-9123-401f-9953-38b03ed2e51d"]
}

def get_updates():
    url = f'{BASE_URL}/getUpdates'
    if last_update_id:
        url += f'?offset={last_update_id + 1}'
    return requests.get(url).json()

def send_voice(chat_id, file_path):
    url = f'{BASE_URL}/sendVoice'
    with open(file_path, 'rb') as audio:
        files = {'voice': audio}
        data = {'chat_id': chat_id}
        requests.post(url, data=data, files=files)

def send_buttons(chat_id):
    url = f"{BASE_URL}/sendMessage"
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ SIM", "callback_data": "sim"}]
        ]
    }
    data = {
        "chat_id": chat_id,
        "text": "😈",
        "reply_markup": keyboard
    }
    requests.post(url, json=data)

def send_product_table(chat_id):
    tabela = (
        "📦 *Nossos VIPS:*\n\n"
        "1️⃣ *Proibidão* - R$9,90\n"
        "2️⃣ *Master (Amador, incesto, vazados)* - R$19,90\n"
        "3️⃣ *Novinhas virgens* - R$29,90\n\n"
        "Clique abaixo para escolher:"
    )
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": tabela,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def send_product_buttons(chat_id):
    url = f"{BASE_URL}/sendMessage"
    keyboard = {
        "inline_keyboard": [
            [{"text": "- Proibidão", "callback_data": "produto_a"}],
            [{"text": "Master", "callback_data": "produto_b"}],
            [{"text": "Novinhas", "callback_data": "produto_c"}]
        ]
    }
    data = {
        "chat_id": chat_id,
        "text": "Selecione um produto abaixo:",
        "reply_markup": keyboard
    }
    requests.post(url, json=data)

def send_confirm_button(chat_id):
    url = f"{BASE_URL}/sendMessage"
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ SIM", "callback_data": "confirmar_compra"}]
        ]
    }
    data = {
        "chat_id": chat_id,
        "text": "Gostou do que viu? Deseja receber o link de pagamento?",
        "reply_markup": keyboard
    }
    requests.post(url, json=data)

def send_previews(chat_id, product_key):
    msg = f"Você escolheu {product_key.replace('_', ' ').title()}. Vou te mostrar como é o VIP por dentro 😈 👇🏻"
    requests.post(f"{BASE_URL}/sendMessage", data={"chat_id": chat_id, "text": msg})

    for video_url in video_previews.get(product_key, []):
        url = f"{BASE_URL}/sendVideo"
        data = {
            "chat_id": chat_id,
            "video": video_url
        }
        requests.post(url, data=data)

    send_voice(chat_id, "audio3.ogg")
    send_confirm_button(chat_id)

def answer_callback(callback_query_id, text=""):
    url = f"{BASE_URL}/answerCallbackQuery"
    data = {
        "callback_query_id": callback_query_id,
        "text": text,
        "show_alert": False
    }
    requests.post(url, data=data)

def main():
    global last_update_id
    print("Bot rodando...")

    while True:
        updates = get_updates()
        for result in updates.get("result", []):
            update_id = result["update_id"]

            if "message" in result:
                message = result["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text == "/start":
                    send_voice(chat_id, "audio1.ogg")
                    send_buttons(chat_id)

            elif "callback_query" in result:
                callback = result["callback_query"]
                chat_id = callback["from"]["id"]
                data = callback["data"]
                callback_id = callback["id"]

                if data == "sim":
                    answer_callback(callback_id, "Você escolheu SIM ✅")
                    send_product_table(chat_id)
                    send_voice(chat_id, "audio2.ogg")
                    send_product_buttons(chat_id)

                elif data in ["produto_a", "produto_b", "produto_c"]:
                    answer_callback(callback_id)
                    user_products[chat_id] = data
                    send_previews(chat_id, data)

                elif data == "confirmar_compra":
                    answer_callback(callback_id)
                    produto = user_products.get(chat_id)

                    if produto:
                        link = payment_links.get(produto, "https://pay.sunize.com.br")
                        msg = f"💳 Aqui está seu link de pagamento:\n{link}"
                        requests.post(f"{BASE_URL}/sendMessage", data={"chat_id": chat_id, "text": msg})
                        send_voice(chat_id, "audio4.ogg")
                    else:
                        requests.post(f"{BASE_URL}/sendMessage", data={"chat_id": chat_id, "text": "❗ Produto não identificado."})

            last_update_id = update_id

        time.sleep(1)

if __name__ == "__main__":
    main()
