import os
from utils.folders import DATA_PAPKA, CHART_PAPKA

def foydalanuvchi_malumotlarini_ochirish(user_id):
    data_file=os.path.join(DATA_PAPKA,f"user_{user_id}.csv")
    if os.path.exists(data_file):
        os.remove(data_file)

    for file in os.listdir(CHART_PAPKA):
        if str(user_id) in file:
            os.remove(os.path.join(CHART_PAPKA,file))
        

