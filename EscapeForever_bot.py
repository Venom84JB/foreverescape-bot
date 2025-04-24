import logging
logging.basicConfig(level=logging.INFO)

import matplotlib.pyplot as plt
import io
import datetime
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔐 Je Telegram-bot token
BOT_TOKEN = "7589002786:AAF6aiv42VXmmZOQKR3ut6LnvUByJDXVP7s"

# 📈 OHLCV-endpoint van GeckoTerminal (5-min candles)
API_URL = (
    "https://api.geckoterminal.com/api/v2/"
    "networks/pepe-unchained/pools/"
    "0xc257f8d622ab18eb6f97980c56ebc3627fd21344/"
    "ohlcv/minute?aggregate=5"
)

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            if resp.status != 200:
                await update.message.reply_text("❌ Kon data niet ophalen van GeckoTerminal.")
                return
            data = await resp.json()


    ohlcv = data["data"]["attributes"]["ohlcv_list"]
    dates = [datetime.datetime.fromtimestamp(c[0]) for c in ohlcv]
    closes = [float(c[4]) for c in ohlcv]

  
    plt.figure()
    plt.plot(dates, closes, label="Sluitprijs")
    plt.title("Forever Escape Token (5-min candles)")
    plt.xlabel("Tijd")
    plt.ylabel("Prijs (USD)")
    plt.gcf().autofmt_xdate()
    plt.grid(True)

  
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Stuur de grafiek terug naar de gebruiker
    await update.message.reply_photo(photo=buf)

if __name__ == "__main__":
    # Bouw en start de Telegram-bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("chart", chart))
    logging.info("Bot gestart, wacht op /chart commando...")
    app.run_polling()
