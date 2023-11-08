import requests
from bs4 import BeautifulSoup
import json
import re

# Получаем данные с исходной страницы и сохраняем их в файл
url = "https://ru.wikipedia.org/wiki/Список_рек_по_длине"

# get_request = requests.get(url).text

# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(get_request)

# С помощью класса BeautifulSoup преобразуем код в дерево объектов Python и собираем JSON
with open("index.html", "r", encoding="utf-8") as file:
    src = file.read()

data_json = []

soup = BeautifulSoup(src, "lxml")

trow_list = soup.find("table", class_="wikitable sortable").find_all("tr")[1:]

for tdata in trow_list:
    element_extract = tdata.find_all("td")

    # Инициализируем переменные для каждой ячейки
    river = ""
    length = None
    poolArea = None
    waterConsumption = None
    pools = []
    countries = []

    # Проверяем наличие и извлекаем данные из каждой ячейки
    if len(element_extract) >= 2:
        river = element_extract[1].text.strip()
    if len(element_extract) >= 3:
        length_match = re.search(r"\d+", element_extract[2].text)
        if length_match:
            length = int(length_match.group())
    if len(element_extract) >= 4:
        poolArea_match = re.search(r"\d+", element_extract[3].text)
        if poolArea_match:
            poolArea = int(poolArea_match.group())
    if len(element_extract) >= 5:
        waterConsumption_match = re.search(r"\d+", element_extract[4].text)
        if waterConsumption_match:
            waterConsumption = int(waterConsumption_match.group())
    if len(element_extract) >= 6:
        pools = ["".join(re.findall(r"[^\d\(\)][\w’ -]+", pool)) for pool in re.split(r",", element_extract[5].text) if re.findall(r"[^\d\(\)][\w’ -]+", pool)]
    if len(element_extract) >= 7:
        countries = ["".join(re.findall(r"[^\d\(\)][\w’ -]+", country)) for country in re.split(r",", element_extract[6].text) if re.findall(r"[^\d\(\)][\w’ -]+", country)]

    # Создаем объект для бассейнов
    pools_object = {}
    for i, pool in enumerate(pools, start=1):
        pools_object[f"pool{i}"] = pool.strip()

    # Создаем объект для стран
    country_object = {}
    for i, country in enumerate(countries, start=1):
        country_object[f"country{i}"] = country.strip()

    # Создаем структуру данных JSON и добавляем ее в список
    data_element = {
        "river": river,
        "length": length,
        "poolArea": poolArea,
        "waterConsumption": waterConsumption,
        "pool": pools_object,
        "countries": country_object
    }
    data_json.append(data_element)

with open("data.json", "a", encoding="utf-8") as file:
    json.dump(data_json, file, indent=4, ensure_ascii=False)
