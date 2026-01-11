import random

def generate_data(rows=10):
    data = []
    for i in range (rows):
        row={
            "time": i,
            "temperature": round(20 + random.random()*5, 2),
            "pressure": round(100 + random.random()*2, 2),
            "vibration": round(random.random()*5, 2)
        }
        data.append(row)
    return data