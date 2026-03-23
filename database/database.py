import pandas as pd
from datetime import datetime
from utils.folders import foydalanuvchi_fayli
import os

def foydalanuvchini_yaratish(user_id):
    file=foydalanuvchi_fayli(user_id)
    if not os.path.exists(file):
        df=pd.DataFrame(columns=["date","amount","category","note"])
        df.to_csv(file,index=False)

def xarajat_qosh(user_id,summa,kategoriya,izoh):
    file=foydalanuvchi_fayli(user_id)
    foydalanuvchini_yaratish(user_id)
    df=pd.read_csv(file)
    yangi_qator={
        "date":datetime.now().strftime("%Y-%m-%d"),
        "amount":summa,
        "category":kategoriya,
        "note":izoh
    }
    df=pd.concat([df,pd.DataFrame([yangi_qator])],ignore_index=True)
    df.to_csv(file,index=False)