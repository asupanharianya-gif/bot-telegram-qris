import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== DATA CONFIGURATION ====================
TOKEN = "8131013410:AAGpvka3na2TS4EXVQE_rh-GkVOhB4osbvg"

# Link Gambar QRIS
QRIS_URL = "https://i.imgur.com/stDVDsN.jpeg"

# Data Channel & Pesan Price List
CHANNEL_USERNAME = "@asupanharianya1"
PRICE_LIST_MSG_ID = 46

ADMIN_USERNAME = "@Asupanexcya"
# ============================================================

bot = telebot.TeleBot(TOKEN)

# 1. MENAMPILKAN MENU UTAMA KETIKA PEMBELI KETIK /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    
    # Tombol Pilihan Paket
    markup.add(InlineKeyboardButton("1. ALL EXC GRUP (35k)", callback_data="paket_1"))
    markup.add(InlineKeyboardButton("2. ALTER GRUP (35k)", callback_data="paket_2"))
    markup.add(InlineKeyboardButton("3. DISKON 9.9 SPECIAL (55k)", callback_data="paket_3"))
    
    # Tombol Kirim Price List Langsung di Chat & Chat Admin
    markup.add(
        InlineKeyboardButton("📋 Lihat Price List", callback_data="show_pricelist"),
        InlineKeyboardButton("💬 Chat Admin", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")
    )
    
    pesan = (
        "Halo! Selamat datang 😊\n"
        "Silakan pilih paket pembayaran di bawah ini untuk mendapatkan QRIS:\n\n"
        "1. ALL EXC GRUP — Rp 35.000\n"
        "2. ALTER GRUP — Rp 35.000\n"
        "3. DISKON 9.9 SPECIAL 2 GRUP — Rp 55.000 (Harga Normal Rp 75.000)\n\n"
        f"📩 Admin: {ADMIN_USERNAME}"
    )
    bot.send_message(message.chat.id, pesan, reply_markup=markup)

# 2. LOGIKA TOMBOL PILIHAN PAKET, PRICE LIST LANGSUNG, & BATAL/HAPUS QRIS
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Opsi jika pembeli klik "Lihat Price List"
    if call.data == "show_pricelist":
        try:
            bot.forward_message(chat_id, CHANNEL_USERNAME, PRICE_LIST_MSG_ID)
        except Exception:
            bot.send_message(chat_id, "📋 **Price List:**\nhttps://t.me/asupanharianya1/46")
        return

    # Opsi Batal/Hapus QRIS
    if call.data == "cancel":
        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            pass
        bot.send_message(chat_id, "❌ Transaksi dibatalkan. Ketik /start jika ingin memesan ulang.")
        return

    cancel_markup = InlineKeyboardMarkup()
    cancel_markup.add(InlineKeyboardButton("❌ Batal / Hapus QRIS", callback_data="cancel"))

    if call.data == "paket_1":
        caption = (
            "🌟 **ALL EXC GRUP PAYMENT Rp 35.000**\n\n"
            "📍Harap kirimkan bukti paymentnya untuk verifikasi📍"
        )
        bot.send_photo(chat_id, QRIS_URL, caption=caption, parse_mode="Markdown", reply_markup=cancel_markup)
        
    elif call.data == "paket_2":
        caption = (
            "🔞 **ALTER GRUP PAYMENT Rp 35.000**\n\n"
            "📍Harap kirimkan bukti paymentnya untuk verifikasi📍"
        )
        bot.send_photo(chat_id, QRIS_URL, caption=caption, parse_mode="Markdown", reply_markup=cancel_markup)
        
    elif call.data == "paket_3":
        caption = (
            "💥 **DISKON 9.9 SPECIAL PAYMENT 2 GRUP (EXC & ALTER) Rp 75.000 Rp 55.000**\n\n"
            "📍Harap kirimkan bukti paymentnya untuk verifikasi📍"
        )
        bot.send_photo(chat_id, QRIS_URL, caption=caption, parse_mode="Markdown", reply_markup=cancel_markup)

# MENJALANKAN BOT
print("Bot Telegram berhasil dijalankan...")
bot.infinity_polling()
