import pandas as pd
from datetime import datetime
from utils.folders import foydalanuvchi_fayli
from core.finance import malumot_yuklash
import os
import calendar

def kunlik_maslahat(user_id):
    data=malumot_yuklash(user_id)
    income=data.get("income",0)
    if income==0:
        return "💰 Avval oylik daromadingizni kiriting." \
        "Daromadingizni oylik daromad tugmasini bosib kiritishingiz mumkin."
    monthly_budget=income*0.9
    today=datetime.now()
    days_in_month=calendar.monthrange(today.year,today.month)[1]
    daily_limit=monthly_budget/days_in_month
    file=foydalanuvchi_fayli(user_id)
    if not os.path.exists(file):
        return f"📅 Kunlik limit: {int(daily_limit):,} so‘m"
    df=pd.read_csv(file)
    if df.empty:
        return f"📅 Kunlik limit: {int(daily_limit):,} so‘m"
    df['date']=pd.to_datetime(df['date'])
    today_spent=df[df['date'].dt.date==today.date()]['amount'].sum()
    message=f"""
💡 Kunlik moliyaviy maslahat

💰 Oylik budget: {int(monthly_budget):,}
📅 Kunlik limit: {int(daily_limit):,}

━━━━━━━━━━━━━━━
📊 Bugungi sarf: {int(today_spent):,}
"""
    if today_spent>daily_limit:
        farq=int(today_spent-daily_limit)
        message+=f"\n⚠️ Siz {farq:,} so‘mga limitdan oshdingiz!"
    else:
        qolgan=int(daily_limit-today_spent)
        message+=f"\n✅ Yaxshi! Yana {qolgan:,} so‘m sarflashingiz mumkin"
    return message

def haftalik_tahlil(user_id):
    file=foydalanuvchi_fayli(user_id)
    if not os.path.exists(file):
        return "Ma'lumot yo‘q"
    df=pd.read_csv(file)
    if df.empty:
        return "Ma'lumot yo‘q"
    df['date']=pd.to_datetime(df['date'])
    last_week=df[df['date']>=datetime.now()-pd.Timedelta(days=7)]
    prev_week=df[(df['date']<datetime.now()-pd.Timedelta(days=7)) &
                 (df['date']>=datetime.now()-pd.Timedelta(days=14))]
    last_sum=last_week.groupby("category")['amount'].sum()
    prev_sum=prev_week.groupby("category")['amount'].sum()
    natija=[]
    for cat in last_sum.index:
        if cat in prev_sum and prev_sum[cat]!=0:
            change=((last_sum[cat]-prev_sum[cat])/prev_sum[cat])*100
            if change>0:
                natija.append(f"📈 {cat}: {change:.0f}% ko‘proq sarfladingiz")
            else:
                natija.append(f"📉 {cat}: {abs(change):.0f}% kam sarfladingiz")
    return "\n".join(natija) if natija else "Yetarli data yo‘q"

def bugungi_xarajatlar(user_id):
    import pandas as pd
    from datetime import datetime
    from utils.folders import foydalanuvchi_fayli
    import os

    file=foydalanuvchi_fayli(user_id)

    if not os.path.exists(file):
        return "📆 Bugun hech qanday xarajat yo‘q"

    df=pd.read_csv(file)

    if df.empty:
        return "📆 Bugun hech qanday xarajat yo‘q"

    df['date']=pd.to_datetime(df['date'])

    bugun=datetime.now().date()
    bugungi=df[df['date'].dt.date==bugun]

    if bugungi.empty:
        return "📆 Bugun xarajat qilinmadi"

    natija="📆 Bugungi xarajatlaringiz:\n\n"

    for _,row in bugungi.iterrows():
        natija+=(
            f"💰 {int(row['amount']):,} so‘m\n"
            f"📂 {row['category']}\n"
            f"📝 {row['note']}\n"
            f"───────────────\n"
        )

    return natija

def oylik_hisobot(user_id):
    file=foydalanuvchi_fayli(user_id)
    if not os.path.exists(file):
        return "Ma'lumot yo‘q"
    df=pd.read_csv(file)
    if df.empty:
        return "Ma'lumot yo‘q"
    df['date']=pd.to_datetime(df['date'])
    this_month=df[df['date'].dt.month==datetime.now().month]
    if this_month.empty:
        return "Bu oy uchun data yo‘q"
    total=this_month['amount'].sum()
    by_category=this_month.groupby("category")['amount'].sum()
    top_category=by_category.idxmax()
    avg=this_month['amount'].mean()
    return f"""
📊 Oylik hisobot

💰 Jami sarfladingiz: {int(total):,}
🏆 Eng ko‘p pul ketgan: {top_category}
📈 Kunlik o‘rtacha: {int(avg):,}

━━━━━━━━━━━━━━━
📌 Xarajatlaringiz nazoratda
"""

def aqlli_maslahat(user_id):
    file=foydalanuvchi_fayli(user_id)
    if not os.path.exists(file):
        return "Ma'lumot yo‘q"
    df=pd.read_csv(file)
    if df.empty:
        return "Ma'lumot yo‘q"
    by_category=df.groupby("category")['amount'].sum()
    top=by_category.idxmax()
    top_value=by_category.max()
    total=df['amount'].sum()
    message=f"""
🤖 Aqlli tahlil

📊 Eng katta xarajat: {top} ({int(top_value):,} so‘m)
"""
    if top=="food":
        message+="\n🍔 Ovqatga juda ko‘p sarflayapsiz — kamaytirishga harakat qiling"
    elif top=="transport":
        message+="\n🚕 Transport xarajatlarini optimallashtirish mumkin"
    elif top=="shopping":
        message+="\n🛍 Xaridlar ko‘p — ehtiyot bo‘ling"
    elif top=="education":
        message+="\n📚 Ta’limga sarf yaxshi investitsiya 👍"
    return message

def umumiy_tahlil(user_id):
    return f"""
📊 Haftalik tahlil:
{haftalik_tahlil(user_id)}
━━━━━━━━━━━━━━━
💡 Kunlik maslahat:
{kunlik_maslahat(user_id)}
━━━━━━━━━━━━━━━
🤖 Aqlli fikr:
{aqlli_maslahat(user_id)}
"""