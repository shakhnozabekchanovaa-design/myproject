import os

ASOSIY_PAPKA="finance_bot"
DATA_PAPKA=os.path.join(ASOSIY_PAPKA,"data")
CHART_PAPKA=os.path.join(ASOSIY_PAPKA,"charts")

os.makedirs(DATA_PAPKA,exist_ok=True)
os.makedirs(CHART_PAPKA,exist_ok=True)

def foydalanuvchi_fayli(user_id):
    return os.path.join(DATA_PAPKA,f"user_{user_id}.csv")