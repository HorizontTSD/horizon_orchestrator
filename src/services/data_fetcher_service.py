import json
import pandas as pd
import numpy as np
from src.utils.calc_error_metrix import metrix_all
from src.clients.timescaledb import get_db_connection

# По идее это должно быть получено по id организации, какие датчики настроены для прогноза
id_sensor_mapping = {
    "arithmetic_1464947681": "load_consumption",
    "arithmetic_1464947681_2": "load_consumption"
}

async def data_fetcher(sensor_ids):

    """
    Служит для получения данных для главного графика прогноза,
    который можно увидеть на странице [Horizon Tool](https://horizon-tool.ru).

    Данные извлекаются по конкретным `sensor_ids`.
    В перспективе функция будет обращаться к базе данных, где `id` организации
    и связанные с ней настроенные датчики будут использоваться для выборки данных.

    Планируемый пайплайн работы:
    1. При регистрации пользователь создает свою организацию.
    2. Переходит во вкладку **DB connections** и настраивает подключение к БД.
    3. Выбирает таблицу, затем в ней — колонку времени и целевую метрику (таргет) для прогноза.
    4. Нажимает кнопку наподобие **"Настроить прогноз"**.
    5. На стороне сервиса (или клиента, решение будет принято позже) создается таблица
       с пометкой `forecast_<initial_table_name>`.
    6. Прогноз пишется в `forecast_<initial_table_name>`

    При вызове этого метода:
    - Из основной таблицы организации берутся *n* последних строк для левой (синей) части графика.
    - Из таблицы с прогнозом берутся *n* строк для правой (бирюзовой) части графика.

    Параметры:
        sensor_ids (list | str): Идентификаторы датчиков, по которым необходимо получить данные.

    Возвращает:
        str: Статус выполнения с указанными `sensor_ids`.
    """

    horizon = 288
    limit = 300
    response = []

    for sensor_id in sensor_ids:

        sensor = {}

        sensor[sensor_id] = {}

        # ------------------------------------- Получение Last real data -------------------------------------
        # На этом этапе мы получаем последние реальные данные из базы данных конкретной организации.
        # При регистрации пользователь создаёт организацию, у которой появляется уникальный id.
        # По этому id мы обращаемся к хранилищу данных, чтобы достать:
        #   - указанные кредиты (credentials) для доступа к БД организации,
        #   - информацию о том, как создан клиент для работы с этой БД.
        # Пока предполагается использование PostgreSQL с расширением TimescaleDB.
        # В будущем коллекцию можно расширить для работы с другими типами БД.
        # На основе id организации и настроек доступа мы достаём данные из конкретной таблицы реальных данных.
        # Предполагается, что до этого пользователь в разделе "DB Connections":
        #   - указал кредиты для своей БД,
        #   - выбрал таблицу с данными,
        #   - указал значения для прогнозирования.
        # Эти настройки мы сохраняем и теперь используем для формирования запроса к БД.
        # Ниже  это частный случай

        table_name = id_sensor_mapping[sensor_id]
        table_name_prediction = f'predict_{table_name}'
        table_name_prediction_xgb = f'xgb_predict_{table_name}'
        measurement = table_name


        conn = get_db_connection()
        cur = conn.cursor()

        select_query = f"""
        SELECT * FROM {table_name} ORDER BY datetime DESC LIMIT {limit};
        """

        cur.execute(select_query)
        rows = cur.fetchall()

        df_last_real_data = pd.DataFrame(rows, columns=["datetime", measurement])
        df_last_real_data["datetime"] = pd.to_datetime(df_last_real_data["datetime"]).dt.tz_localize(None)

        if sensor_id == "arithmetic_1464947681_2":
            df_last_real_data[measurement] = df_last_real_data[measurement] * np.random.uniform(0.5, 1.2, size=len(df_last_real_data))

        # Это значение последней известной даты используется для "приклеивания" его к прогнозным данным.
        # Делается это, чтобы на графике визуально создавался плавный переход от реальных данных к прогнозу.
        df_last_real_line = df_last_real_data.iloc[0]
        last_know_data = df_last_real_line["datetime"]

        df_real_data_to_comparison = df_last_real_data[:horizon]

        # ------------------------------------- LSTM prediction -------------------------------------
        # ------------------------------------- Получение Last real data -------------------------------------
        # На этом этапе мы получаем последние предсказанные данные из базы данных конкретной организации.
        # При регистрации пользователь создаёт организацию, у которой появляется уникальный id.
        # По этому id мы обращаемся к хранилищу данных, чтобы достать:
        #   - указанные кредиты (credentials) для доступа к БД организации,
        #   - информацию о том, как создан клиент для работы с этой БД.
        # Пока предполагается использование PostgreSQL с расширением TimescaleDB.
        # В будущем коллекцию можно расширить для работы с другими типами БД.
        # На основе id организации и настроек доступа мы достаём данные из конкретной таблицы реальных данных.
        # Предполагается, что до этого пользователь в разделе "DB Connections":
        #   - указал кредиты для своей БД,
        #   - выбрал таблицу с данными,
        #   - указал значения для прогнозирования.
        # Эти настройки мы сохраняем и теперь используем для формирования запроса к БД.
        # Ниже  это частный случай

        select_query_predict = f"""
        SELECT * FROM {table_name_prediction} ORDER BY datetime DESC LIMIT 1000;
        """
        cur.execute(select_query_predict)
        rows = cur.fetchall()

        df_prediction = pd.DataFrame(rows, columns=["datetime", measurement])

        df_prediction["datetime"] = pd.to_datetime(df_prediction["datetime"]).dt.tz_localize(None)

        df_actual_prediction = df_prediction[df_prediction["datetime"] > last_know_data]

        # Здесь приклеиваем последнее значение известной даты к прогнозным данным.
        # Делается это, чтобы на графике визуально создавался плавный переход от реальных данных к прогнозу.
        df_actual_prediction = pd.concat(
            [df_actual_prediction, df_last_real_line.to_frame().T],
            ignore_index=True
        )

        df_actual_prediction = df_actual_prediction.iloc[:2]

        df_previous_prediction = df_prediction[df_prediction["datetime"] < last_know_data]

        df_previous_prediction = pd.concat(
            [df_last_real_line.to_frame().T, df_previous_prediction],
            ignore_index=True
        )
        df_previous_LSTM_prediction_to_comparison = df_previous_prediction[:horizon]

        # Это  было сделано для теста, чтобы проверить работоспособность если выбран другой датчик
        if sensor_id == "arithmetic_1464947681_2":
            df_actual_prediction[measurement] = df_actual_prediction[measurement] * np.random.uniform(0.5, 1.2, size=len(df_actual_prediction))

        df_real = df_real_data_to_comparison.copy()
        df_real = df_real.iloc[:len(df_previous_LSTM_prediction_to_comparison)]

        metrics, df_metrics = metrix_all(
            col_time="datetime",
            col_target=measurement,
            df_evaluetion=df_previous_LSTM_prediction_to_comparison,
            df_comparative=df_real)


        actual_col = f"Actual {measurement}"

        df_metrics["R2"] = metrics["R2"]

        df_metrics[actual_col] = df_real_data_to_comparison[measurement]
        df_metrics["LSTM predicted"] = df_previous_LSTM_prediction_to_comparison[measurement]

        metrix_to_show_LSTM = ["datetime", actual_col, "LSTM predicted", "MAPE", "RMSE", "MAE"]

        col_to_round = ["MAPE", "RMSE", "MAE"]

        df_metrics[col_to_round] = df_metrics[col_to_round].round(2)

        df_metrics["LSTM predicted"] = pd.to_numeric(df_metrics["LSTM predicted"], errors="coerce").round(2)


        df_metrics = df_metrics[metrix_to_show_LSTM]

        df_metrics = df_metrics.rename(columns={"datetime": "Time"})

        df_metrics_LSTM = df_metrics

        # ------------------------------------- XGBoost prediction -------------------------------------

        select_query_predict = f"""
        SELECT * FROM {table_name_prediction_xgb} ORDER BY datetime DESC LIMIT 1000;
        """
        cur.execute(select_query_predict)
        rows = cur.fetchall()

        df_prediction_xgb = pd.DataFrame(rows, columns=["datetime", measurement])

        df_prediction_xgb["datetime"] = pd.to_datetime(df_prediction_xgb["datetime"]).dt.tz_localize(None)

        df_actual_prediction_xgb = df_prediction_xgb[df_prediction_xgb["datetime"] > last_know_data]

        df_actual_prediction_xgb = pd.concat(
            [df_actual_prediction_xgb, df_last_real_line.to_frame().T],
            ignore_index=True
        )

        if sensor_id == "arithmetic_1464947681_2":
            df_actual_prediction_xgb[measurement] = df_actual_prediction_xgb[measurement] * np.random.uniform(0.5, 1.2, size=len(df_actual_prediction_xgb))

        df_previous_prediction_xgb = df_prediction_xgb[df_prediction_xgb["datetime"] < last_know_data]

        df_previous_prediction_xgb = pd.concat(
            [df_last_real_line.to_frame().T, df_previous_prediction_xgb],
            ignore_index=True
        )

        df_previous_prediction_xgb_to_comparison = df_previous_prediction_xgb[:horizon]

        metrics, df_metrics = metrix_all(
            col_time="datetime",
            col_target=measurement,
            df_evaluetion=df_previous_prediction_xgb_to_comparison,
            df_comparative=df_real_data_to_comparison)

        df_metrics["R2"] = metrics["R2"]

        df_metrics[actual_col] = df_real_data_to_comparison[measurement]
        df_metrics["XGBoost predicted"] = df_previous_prediction_xgb_to_comparison[measurement]

        df_metrics_XGBoost = df_metrics

        metrix_to_show_XGBoost = ["datetime", actual_col, "XGBoost predicted", "MAPE", "RMSE", "MAE"]

        col_to_round = ["MAPE", "RMSE", "MAE"]

        df_metrics_XGBoost[col_to_round] = df_metrics_XGBoost[col_to_round].round(2)

        df_metrics["XGBoost predicted"] = pd.to_numeric(df_metrics["XGBoost predicted"], errors="coerce").round(2)

        df_metrics_XGBoost = df_metrics_XGBoost[metrix_to_show_XGBoost]

        df_metrics_XGBoost = df_metrics_XGBoost.rename(columns={"datetime": "Time"})

        cur.close()
        conn.close()

        # ------------------------------------- ensemble prediction -------------------------------------

        weight_xgb = 0.5
        weight_other = 0.5
        total_weight = weight_xgb + weight_other

        ensemble_prediction = (df_actual_prediction_xgb['load_consumption'] * weight_xgb +
                               df_actual_prediction['load_consumption'] * weight_other) / total_weight

        df_ensemble = pd.DataFrame({'datetime': df_actual_prediction_xgb['datetime'],
                                    'load_consumption': ensemble_prediction})

        table_to_download = df_actual_prediction_xgb.copy()

        df_table_to_download = table_to_download.rename(columns={"load_consumption": "XGBoost_predict"})
        df_table_to_download["LSTM_predict"] = df_actual_prediction["load_consumption"]
        df_table_to_download["ensemble_predict"] = df_ensemble["load_consumption"]

        last_real_data = json.loads(df_last_real_data.to_json(orient="records", force_ascii=False))
        actual_prediction_lstm = json.loads(df_actual_prediction.to_json(orient="records", force_ascii=False))
        actual_prediction_xgboost = json.loads(df_actual_prediction_xgb.to_json(orient="records", force_ascii=False))
        ensemble = json.loads(df_ensemble.to_json(orient="records", force_ascii=False))

        table_to_download = json.loads(df_table_to_download.to_json(orient="records", force_ascii=False))
        metrics_table_XGBoost = json.loads(df_metrics_XGBoost.to_json(orient="records", force_ascii=False))
        metrics_table_LSTM = json.loads(df_metrics_LSTM.to_json(orient="records", force_ascii=False))

        last_know_data = last_know_data.strftime("%Y-%m-%d %H:%M:%S")


        if sensor_id == 'arithmetic_1464947681_2':
            table_name = 'test_load_consumption'

        description = {
            "sensor_name": table_name,
            "sensor_id": sensor_id
        }
        data = {
            "last_real_data": last_real_data,
            "actual_prediction_lstm": actual_prediction_lstm,
            "actual_prediction_xgboost": actual_prediction_xgboost,
            "ensemble": ensemble,
        }

        map_data = {
            "data": data,
            "last_know_data": last_know_data,
            "legend": {
                "last_know_data_line": {
                    "text": {
                        "en": "Last known date",
                        "ru": "Последняя известная дата",
                        "zh": "最后已知日期",
                        "it": "Ultima data conosciuta",
                        "fr": "Dernière date connue",
                        "de": "Letztes bekanntes Datum"
                    },
                    "color": "#A9A9A9"
                },
                "real_data_line": {
                    "text": {
                        "en": "Real data",
                        "ru": "Реальные данные",
                        "zh": "真实数据",
                        "it": "Dati reali",
                        "fr": "Données réelles",
                        "de": "Echte Daten"
                    },
                    "color": "#0000FF"
                },
                "LSTM_data_line": {
                    "text": {
                        "en": "LSTM current forecast",
                        "ru": "LSTM актуальный прогноз",
                        "zh": "LSTM 当前预测",
                        "it": "Previsione attuale LSTM",
                        "fr": "Prévision actuelle LSTM",
                        "de": "Aktuelle LSTM-Vorhersage"
                    },
                    "color": "#FFA500"
                },
                "XGBoost_data_line": {
                    "text": {
                        "en": "XGBoost current forecast",
                        "ru": "XGBoost актуальный прогноз",
                        "zh": "XGBoost 当前预测",
                        "it": "Previsione attuale XGBoost",
                        "fr": "Prévision actuelle XGBoost",
                        "de": "Aktuelle XGBoost-Vorhersage"
                    },
                    "color": "#a7f3d0"
                },
                "Ensemble_data_line": {
                    "text": {
                        "en": "Ensemble forecast",
                        "ru": "Ансамбль прогноз",
                        "zh": "集成预测",
                        "it": "Previsione dell'ensemble",
                        "fr": "Prévision d'ensemble",
                        "de": "Ensemble-Vorhersage"
                    },
                    "color": " #FFFF00"
                },
            }
        }

        metrix_tables = {
            "XGBoost": {
                "metrics_table": metrics_table_XGBoost,
                "text": {
                    "en": "Forecast accuracy metrics for XGBoost",
                    "ru": "Метрики точности прогноза для XGBoost",
                    "zh": "XGBoost 预测准确性指标",
                    "it": "Metriche di accuratezza delle previsioni per XGBoost",
                    "fr": "Métriques de précision des prévisions pour XGBoost",
                    "de": "Prognosegenauigkeitsmetriken für XGBoost"
                },
            },
            "LSTM": {
                "metrics_table": metrics_table_LSTM,
                "text": {
                    "en": "Forecast accuracy metrics for LSTM",
                    "ru": "Метрики точности прогноза для LSTM",
                    "zh": "LSTM 预测准确性指标",
                    "it": "Metriche di accuratezza delle previsioni per LSTM",
                    "fr": "Métriques de précision des prévisions pour LSTM",
                    "de": "Prognosegenauigkeitsmetriken für LSTM"
                },
            },
        }

        sensor[sensor_id]["description"] = description
        sensor[sensor_id]["map_data"] = map_data
        sensor[sensor_id]["table_to_download"] = table_to_download
        sensor[sensor_id]["metrix_tables"] = metrix_tables

        response.append(sensor)


    return response
