import json
import random
import numpy as np
import pandas as pd


def generate_random(length: int = 30, value_range: tuple = (0, 100)) -> str:
    """
    Генерирует JSON-строку с данными заданной длины, содержащими 'index' и 'value'.

    :param length: Длина DataFrame.
    :param value_range: Кортеж (min, max) задающий диапазон случайных значений.
    :return: JSON-строка с данными.
    """
    df = pd.DataFrame({
        'datetime': pd.date_range(end=pd.Timestamp.today(), periods=length, freq='D'),
        'value': np.random.uniform(value_range[0], value_range[1], length)
    })
    return json.loads(df.to_json(orient='records'))


async def mini_charts_data():
    """
    Генерирует случайные данные для 4 мини-графиков, расположенных в верхней части
    главной страницы инструмента [Horizon Tool](https://horizon-tool.ru).

    В текущей реализации данные носят демонстрационный характер и включают:
    - Температуру
    - Скорость ветра
    - Влажность
    - Давление

    Для каждого показателя формируются:
    - Случайное текущее значение
    - Процент изменения и направление (положительное/отрицательное)
    - Массив данных за последние 24 часа (288 точек)

    **Примечание:** в будущем эти данные должны быть заменены на реальные метрики заказчика,
    такие как погодные условия, нагрузка на систему или другие показатели, отражающие действительность.
    """
    random_values_temp = [16, 32]
    random_values_wind_speed = [1, 10]
    random_values_humidity = [25, 100]
    random_values_pressure = [25, 30]

    random_value_temp = round(np.random.uniform(random_values_temp[0], random_values_temp[1]), 2)
    random_value_wind_speed = round(np.random.uniform(random_values_wind_speed[0], random_values_wind_speed[1]), 2)
    random_value_humidity = round(np.random.uniform(random_values_humidity[0], random_values_humidity[1]), 2)
    random_value_pressure = round(np.random.uniform(random_values_pressure[0], random_values_pressure[1]), 2)

    percentages_random_temp =  round(np.random.uniform(1, 100), 2)
    percentages_random_wind_speed =  round(np.random.uniform(1, 100), 2)
    percentages_random_humidity =  round(np.random.uniform(1, 100), 2)
    percentages_random_pressure =  round(np.random.uniform(1, 100), 2)

    mark_random_temp = random.choice(["negative", "positive"])
    mark_random_wind_speed = random.choice(["negative", "positive"])
    mark_random_humidity = random.choice(["negative", "positive"])
    mark_random_pressure = random.choice(["negative", "positive"])

    length = 288

    data_temp = generate_random(length=length, value_range=random_values_temp)
    data_wind_speed = generate_random(length=length, value_range=random_values_wind_speed)
    data_humidity = generate_random(length=length, value_range=random_values_humidity)
    data_pressure = generate_random(length=length, value_range=random_values_pressure)

    response = [
        {
            "title": {
                "en": "Temperature",
                "ru": "Температура",
                "zh": "温度",
                "it": "Temperatura",
                "fr": "Température",
                "de": "Temperatur"
            },
            "values": f"+{random_value_temp}°C",
            "description": {
                "en": "The last 24 hours",
                "ru": "Последние 24 часа",
                "zh": "过去24小时",
                "it": "Le ultime 24 ore",
                "fr": "Les dernières 24 heures",
                "de": "Die letzten 24 Stunden"
            },
            "percentages": {
                "value": percentages_random_temp,
                "mark": mark_random_temp,
            },
            "data": data_temp,
        },
        {
            "title": {
                "en": "Wind speed",
                "ru": "Скорость ветра",
                "zh": "风速",
                "it": "Velocità del vento",
                "fr": "Vitesse du vent",
                "de": "Windgeschwindigkeit"
            },
            "values": f"{random_value_wind_speed}km/h",
            "description": {
                "en": "The last 24 hours",
                "ru": "Последние 24 часа",
                "zh": "过去24小时",
                "it": "Le ultime 24 ore",
                "fr": "Les dernières 24 heures",
                "de": "Die letzten 24 Stunden"
            },
            "percentages": {
                "value": percentages_random_wind_speed,
                "mark": mark_random_wind_speed,
            },
            "data": data_wind_speed,
        },
        {
            "title": {
                "en": "Humidity",
                "ru": "Влажность",
                "zh": "湿度",
                "it": "Umidità",
                "fr": "Humidité",
                "de": "Luftfeuchtigkeit"
            },
            "values": f"{random_value_humidity}%",
            "description": {
                "en": "The last 24 hours",
                "ru": "Последние 24 часа",
                "zh": "过去24小时",
                "it": "Le ultime 24 ore",
                "fr": "Les dernières 24 heures",
                "de": "Die letzten 24 Stunden"
            },
            "percentages": {
                "value": percentages_random_humidity,
                "mark": mark_random_humidity,
            },
            "data": data_humidity,
        },
        {
            "title": {
                "en": "Pressure",
                "ru": "Давление",
                "zh": "气压",
                "it": "Pressione",
                "fr": "Pression",
                "de": "Druck"
            },
            "values": f"{random_value_pressure} inHg",
            "description": {
                "en": "The last 24 hours",
                "ru": "Последние 24 часа",
                "zh": "过去24小时",
                "it": "Le ultime 24 ore",
                "fr": "Les dernières 24 heures",
                "de": "Die letzten 24 Stunden"
            },
            "percentages": {
                "value": percentages_random_pressure,
                "mark": mark_random_pressure,
            },
            "data": data_pressure,
        },
    ]

    return response
