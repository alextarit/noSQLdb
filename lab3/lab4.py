import json
from pymongo import MongoClient
from pymongo import DESCENDING

# Создание клиента и подключение к серверу
client = MongoClient()

# Выбор db
db = client['my_database']  

# Выбор коллекции
collection = db['my_collection'] 
# Загрузrа JSON-файла и вставка его данных в коллекцию
with open('data.json', 'r') as file:  
    data = json.load(file)
    collection.insert_many(data)

# # 1. Сортировка по длине в убывающем порядке
# result = collection.find().sort("length", -1)

# print(f"\n\n\nСортировка по длину в убывающем порядке:")
# for river in result:
#     print(river['river'])

# # 2. Поиск по бассейну (например, "Амазонка")
# result = collection.find({"pool.pool1": "Атлантический океан"})

# print(f"\n\n\nПоиск по бассейну:")
# for river in result:
#     print(river['river'])

# # 3. Наибольший бассейн
# result = collection.find_one(sort=[("poolArea", -1)])

# print("\n\n\nРека с самым большим бассейном:", result['river'])

# 4. Статистика длин рек
from statistics import mean

river_lengths = [river['length'] for river in collection.find()]

average_length = mean(river_lengths)
min_length = min(river_lengths)
max_length = max(river_lengths)

print("\n\n\nСтатистика длин рек:")
print("Средняя длина:", average_length)
print("Минимальная длина:", min_length)
print("Максимальная длина:", max_length)

# # 5. Реки в определенном диапазоне длин (например, от 1000 км до 2000 км)
# result = collection.find({"length": {"$gte": 1000, "$lte": 2000}})

# print("\n\n\nРеки в определенном диапазоне:")
# for river in result:
#     print(river['river'])

# 6. Найти топ-10 рек по размеру бассейна и отсортировать их в порядке убывания
# Группировка по странам и суммирование размеров бассейнов
# pipeline = [
#     {
#         "$group": {
#             "_id": "$countries.country1",
#             "totalPoolArea": {"$sum": "$poolArea"}
#         }
#     },
#     {
#         "$sort": {"totalPoolArea": DESCENDING}
#     },
#     {
#         "$limit": 10
#     }
# ]

# result = list(collection.aggregate(pipeline))

# # Вывести результат
# for entry in result:
#     print(f"Страна: {entry['_id']}, Общая площадь бассейнов: {entry['totalPoolArea']} кв. км")