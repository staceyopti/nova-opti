import os
import json
import random
import string
import threading
from flask import Flask, request, jsonify
import telebot

# --- НАСТРОЙКИ ---
TOKEN = "СЮДА_ВСТАВЬ_ТОКЕН_ИЗ_BOTFATHER"
ADMIN_ID = 123456789  # Твой числовой Telegram ID (можно узнать в @myidbot)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
DATA_FILE = "codes.json"

def load_codes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def save_codes(codes):
    with open(DATA_FILE, "w") as f:
        json.dump(codes, f)

# --- API ДЛЯ ПРОВЕРКИ ИЗ ПРОГРАММЫ ---
@app.route('/check', methods=['GET'])
def check_code():
    code = request.args.get('code')
    if not code:
        return jsonify({"valid": False})
        
    codes = load_codes()
    if code in codes:
        codes.remove(code)  # Удаляем код после использования (одноразовый)
        save_codes(codes)
        return jsonify({"valid": True})
    return jsonify({"valid": False})

# --- КОМАНДЫ ТЕЛЕГРАМ БОТА ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Доступ закрыт.")
        return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎁 Создать промокод", "📋 Активные коды")
    bot.send_message(message.chat.id, "🌙 Панель управления Nova Opti", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎁 Создать промокод")
def generate_promo(message):
    if message.from_user.id != ADMIN_ID: return
    rand_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    new_code = f"NOVA-{rand_str}"
    codes = load_codes()
    codes.append(new_code)
    save_codes(codes)
    bot.send_message(message.chat.id, f"✅ **Промокод создан:**\n\n`{new_code}`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📋 Активные коды")
def list_promos(message):
    if message.from_user.id != ADMIN_ID: return
    codes = load_codes()
    if not codes:
        bot.send_message(message.chat.id, "📦 Кодов нет.")
        return
    bot.send_message(message.chat.id, "📋 **Активные коды:**\n\n" + "\n".join([f"• `{c}`" for c in codes]), parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)