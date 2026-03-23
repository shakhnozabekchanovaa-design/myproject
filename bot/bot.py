from telegram import Update,ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,CallbackQueryHandler,filters,ContextTypes
from core.analytics import kunlik_maslahat,oylik_hisobot,bugungi_xarajatlar
from database.database import xarajat_qosh
from core.charts import kategoriya_pie
from core.finance import malumot_yuklash,malumot_saqlash
import os
from utils.folders import DATA_PAPKA,CHART_PAPKA

foydalanuvchi_holati={}

menu=ReplyKeyboardMarkup([
["📊 Xarajat qo‘shish"],
["📈 Kategoriyalar","🤖 Xarajat tahlili"],
["📅 Hisobot","💰 Oylik daromad"],
["📆 Bugungi xarajatlar"],
["🗑 Ma’lumotlarni tozalash"]
],resize_keyboard=True)

kategoriya_map={
"food":"🍔 Ovqatlanish",
"transport":"🚕 Transport",
"bills":"💡 To‘lovlar",
"shopping":"🛍 Xaridlar",
"education":"📚 Ta’lim",
"other":"📦 Boshqa"
}

def foydalanuvchi_malumotlarini_ochirish(user_id):
    file=os.path.join(DATA_PAPKA,f"user_{user_id}.csv")
    if os.path.exists(file):
        os.remove(file)

    for f in os.listdir(CHART_PAPKA):
        if str(user_id) in f:
            os.remove(os.path.join(CHART_PAPKA,f))

def kategoriya_tugmalari():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍔 Ovqatlanish",callback_data="food"),
         InlineKeyboardButton("🚕 Transport",callback_data="transport")],
        [InlineKeyboardButton("💡 To‘lovlar",callback_data="bills"),
         InlineKeyboardButton("🛍 Xaridlar",callback_data="shopping")],
        [InlineKeyboardButton("📚 Ta’lim",callback_data="education"),
         InlineKeyboardButton("📦 Boshqa",callback_data="other")]
    ])

def ochirish_tugmalari():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Ha", callback_data="delete_yes"),
            InlineKeyboardButton("❌ Yo‘q", callback_data="delete_no")
        ]
    ])

async def boshlash(update:Update,context:ContextTypes.DEFAULT_TYPE):
    ism=update.message.from_user.first_name
    matn=f"""Assalomu alaykum {ism} 👋

💰 Finance botga xush kelibsiz!

Men sizga yordam beraman:
✔ Xarajatlarni yozib borish
✔ Diagrammalar chiqarish
✔ Aqlli moliyaviy maslahat berish

━━━━━━━━━━━━━━━
👇 Boshlash uchun tugmani bosing"""
    await update.message.reply_text(matn,reply_markup=menu)

async def xabar_qabul_qilish(update:Update,context:ContextTypes.DEFAULT_TYPE):
    matn=update.message.text
    foydalanuvchi_id=update.message.from_user.id

    if matn=="🗑 Ma’lumotlarni tozalash":
        await update.message.reply_text(
            "⚠️ Rostdan ham barcha ma’lumotlarni o‘chirmoqchimisiz?",
            reply_markup=ochirish_tugmalari()
        )
        return

    if matn=="📊 Xarajat qo‘shish":
        await update.message.reply_text("📌 Kategoriya tanlang:",reply_markup=kategoriya_tugmalari())
        return

    if matn=="📈 Kategoriyalar":
        path=kategoriya_pie(foydalanuvchi_id)
        if path:
            await update.message.reply_photo(photo=open(path,"rb"))
        else:
            await update.message.reply_text("Ma'lumot yo‘q")
        return

    if matn=="🤖 Xarajat tahlili":
        await update.message.reply_text(kunlik_maslahat(foydalanuvchi_id))
        return

    if matn=="📅 Hisobot":
        await update.message.reply_text(oylik_hisobot(foydalanuvchi_id))
        return

    if matn=="📆 Bugungi xarajatlar":
        await update.message.reply_text(bugungi_xarajatlar(foydalanuvchi_id))
        return

    if matn=="💰 Oylik daromad":
        foydalanuvchi_holati[foydalanuvchi_id]={"bosqich":"daromad"}
        await update.message.reply_text("💰 Daromadingizni kiriting:")
        return

    if foydalanuvchi_id in foydalanuvchi_holati and foydalanuvchi_holati[foydalanuvchi_id]["bosqich"]=="daromad":
        try:
            val=float(matn)
            data=malumot_yuklash(foydalanuvchi_id)
            data["income"]=val
            malumot_saqlash(foydalanuvchi_id,data)
            await update.message.reply_text("✅ Saqlandi",reply_markup=menu)
            del foydalanuvchi_holati[foydalanuvchi_id]
        except:
            await update.message.reply_text("Faqat raqam kiriting")
        return

    if foydalanuvchi_id in foydalanuvchi_holati and foydalanuvchi_holati[foydalanuvchi_id]["bosqich"]=="summa":
        try:
            foydalanuvchi_holati[foydalanuvchi_id]["summa"]=float(matn)
            foydalanuvchi_holati[foydalanuvchi_id]["bosqich"]="izoh"
            await update.message.reply_text("📝 Izoh:")
        except:
            await update.message.reply_text("Masalan: 50000 yozing")
        return

    if foydalanuvchi_id in foydalanuvchi_holati and foydalanuvchi_holati[foydalanuvchi_id]["bosqich"]=="izoh":
        data=foydalanuvchi_holati[foydalanuvchi_id]
        xarajat_qosh(foydalanuvchi_id,data["summa"],data["kategoriya"],matn)

        await update.message.reply_text(f"""📌 Saqlandi

💰 {int(data["summa"]):,} so‘m
📂 {kategoriya_map[data["kategoriya"]]}
📝 {matn}
""",reply_markup=menu)

        del foydalanuvchi_holati[foydalanuvchi_id]
        return

    await update.message.reply_text("Iltimos tugmalardan foydalaning",reply_markup=menu)

async def tugma_bosildi(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    foydalanuvchi_id=query.from_user.id
   
    if query.data=="delete_yes":
        foydalanuvchi_malumotlarini_ochirish(foydalanuvchi_id)
        await query.message.reply_text("🗑 Barcha ma’lumotlar o‘chirildi",reply_markup=menu)
        return

    if query.data=="delete_no":
        await query.message.reply_text("❌ Bekor qilindi",reply_markup=menu)
        return

    kategoriya=query.data
    foydalanuvchi_holati[foydalanuvchi_id]={"bosqich":"summa","kategoriya":kategoriya}
    await query.message.reply_text("💰 Qancha sarfladingiz?")