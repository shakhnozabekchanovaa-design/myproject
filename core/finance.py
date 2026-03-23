import os
import json
from utils.folders import DATA_PAPKA

def foydalanuvchi_fayli(user_id):
    return os.path.join(DATA_PAPKA,f"user_{user_id}_finance.json")

def malumot_yuklash(user_id):
    file=foydalanuvchi_fayli(user_id)
    if not os.path.exists(file):
        return {}
    try:
        with open(file,"r") as f:
            return json.load(f)
    except:
        return {}

def malumot_saqlash(user_id,data):
    file=foydalanuvchi_fayli(user_id)
    with open(file,"w") as f:
        json.dump(data,f,indent=4)

