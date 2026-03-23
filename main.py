from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,CallbackQueryHandler,filters

from config.config import TOKEN
from bot.bot import boshlash,xabar_qabul_qilish,tugma_bosildi

def asosiy():
    ilova=ApplicationBuilder().token(TOKEN).build()
    ilova.add_handler(CommandHandler("start",boshlash))
    ilova.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,xabar_qabul_qilish))
    ilova.add_handler(CallbackQueryHandler(tugma_bosildi))

    print("Bot ishga tushdi...")
    ilova.run_polling()

if __name__=="__main__":
    asosiy()