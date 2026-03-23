import pandas as pd
import matplotlib.pyplot as plt
from utils.folders import foydalanuvchi_fayli, CHART_PAPKA
import os

def kategoriya_pie(user_id):
    file=foydalanuvchi_fayli(user_id)
    if not os.path.exists(file):
        return None
    df=pd.read_csv(file)
    if df.empty:
        return None
    grouped=df.groupby("category")["amount"].sum()
    plt.figure(figsize=(5,5))
    grouped.plot(
        kind="pie",
        autopct="%1.1f%%"
    )
    plt.title("📊 Xarajatlar kategoriyalar bo‘yicha")
    plt.ylabel("")
    path=os.path.join(CHART_PAPKA,f"{user_id}_pie.png")
    plt.savefig(path)
    plt.close()
    return path