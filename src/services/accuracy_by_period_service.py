import pandas as pd
import numpy as np
from src.clients.timescaledb import get_db_connection
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import asyncio
from datetime import timedelta


# По идее это должно быть получено по id организации, какие датчики настроены для прогноза
id_sensor_mapping = {
    "arithmetic_1464947681": "load_consumption",
    "arithmetic_1464947681_2": "load_consumption"
}


async def calculate_metrics(df_merged,  measurement):
    y_true = df_merged[measurement]
    y_pred_xgb = df_merged['load_xgb']
    # y_pred_lstm = df_merged['load_lstm']

    # XGBoost
    mae_xgb = await asyncio.to_thread(mean_absolute_error, y_true, y_pred_xgb)
    mse_xgb = await asyncio.to_thread(mean_squared_error, y_true, y_pred_xgb)
    rmse_xgb = np.sqrt(mse_xgb)
    r2_xgb = await asyncio.to_thread(r2_score, y_true, y_pred_xgb)
    mape_xgb = await asyncio.to_thread(np.mean, np.abs((y_true - y_pred_xgb) / y_true)) * 100


    # LSTM
    # mae_lstm = await asyncio.to_thread(mean_absolute_error, y_true, y_pred_lstm)
    # mse_lstm = await asyncio.to_thread(mean_squared_error, y_true, y_pred_lstm)
    # rmse_lstm = np.sqrt(mse_lstm)
    # r2_lstm = await asyncio.to_thread(r2_score, y_true, y_pred_lstm)
    # mape_lstm = await asyncio.to_thread(np.mean, np.abs((y_true - y_pred_lstm) / y_true)) * 100

    # Округление
    results = {
        "XGBoost": {
            "MAE": round(mae_xgb, 2),
            "RMSE": round(rmse_xgb, 2),
            "R2": round(r2_xgb, 2),
            "MAPE": float(round(mape_xgb, 2)),
        },
        # "LSTM": {
        #     "MAE": round(mae_lstm, 2),
        #     "RMSE": round(rmse_lstm, 2),
        #     "R2": round(r2_lstm, 2),
        #     "MAPE": float(round(mape_lstm, 2)),
        # }
        "LSTM": {
            "MAE": 0,
            "RMSE": 0,
            "R2": 0,
            "MAPE": 0,
        }
    }

    return results


async def calc_accuracy_by_period(sensor_ids, date_start, date_end):

    conn = get_db_connection()
    cur = conn.cursor()

    response = []
    for sensor_id in sensor_ids:
        table_name = id_sensor_mapping[sensor_id]
        table_name_prediction = f'predict_{table_name}' # LSTM predict
        table_name_prediction_xgb = f'xgb_predict_{table_name}'
        measurement = table_name

        #  ---------------- Real data -----------------------------

        select_query_predict = f"""
        SELECT * 
        FROM {table_name} 
        WHERE datetime > '{date_start}' AND datetime <= '{date_end}' 
        ORDER BY datetime DESC;
        """

        cur.execute(select_query_predict)
        rows = cur.fetchall()

        df_real = pd.DataFrame(rows, columns=["datetime", measurement])


        #  ---------------- XGBoost data -----------------------------
        select_query_predict = f"""
        SELECT * 
        FROM {table_name_prediction_xgb} 
        WHERE datetime >= '{date_start}' AND datetime < '{date_end}' 
        ORDER BY datetime DESC;
        """

        cur.execute(select_query_predict)
        rows = cur.fetchall()

        df_prediction_xgb = pd.DataFrame(rows, columns=["datetime", measurement])

        #  ---------------- LSTM data -----------------------------
        select_query_predict = f"""
        SELECT * 
        FROM {table_name_prediction} 
        WHERE datetime >= '{date_start}' AND datetime < '{date_end}' 
        ORDER BY datetime DESC;
        """

        cur.execute(select_query_predict)
        rows = cur.fetchall()

        df_prediction_lstm = pd.DataFrame(rows, columns=["datetime", measurement])

        df_real['datetime'] = pd.to_datetime(df_real['datetime'])
        df_prediction_xgb['datetime'] = pd.to_datetime(df_prediction_xgb['datetime'])
        df_prediction_lstm['datetime'] = pd.to_datetime(df_prediction_lstm['datetime'])

        df_real = df_real.sort_values('datetime')
        df_prediction_xgb = df_prediction_xgb.sort_values('datetime')
        df_prediction_lstm = df_prediction_lstm.sort_values('datetime')

        tolerance = pd.Timedelta(seconds=300)

        df_real['datetime'] = df_real['datetime'].dt.tz_localize(None)
        df_prediction_xgb['datetime'] = df_prediction_xgb['datetime'].dt.tz_localize(None)

        df_merged = pd.merge_asof(
            df_real,
            df_prediction_xgb.rename(columns={'load_consumption': 'load_xgb'}),
            on='datetime',
            direction='nearest',
            tolerance=tolerance
        )

        df_merged['datetime'] = df_merged['datetime'].dt.tz_localize(None)
        df_prediction_lstm['datetime'] = df_prediction_lstm['datetime'].dt.tz_localize(None)

        df_merged = pd.merge_asof(
            df_merged,
            df_prediction_lstm.rename(columns={'load_consumption': 'load_lstm'}),
            on='datetime',
            direction='nearest',
            tolerance=tolerance
        )

        df_merged = df_merged.drop(columns=['load_lstm'])

        df_merged = df_merged.dropna()
        data = await calculate_metrics(df_merged, measurement)

        response.append(data)

    return response


async def fetch_possible_date_for_metrix(sensor_ids):

    conn = get_db_connection()
    cur = conn.cursor()

    response = {}
    for sensor_id in sensor_ids:
        response[sensor_id] = {}
        table_name = id_sensor_mapping[sensor_id]
        table_name_prediction = f'predict_{table_name}'
        table_name_prediction_xgb = f'xgb_predict_{table_name}'

        select_min_date_query = f"SELECT MIN(datetime) FROM {table_name_prediction};"
        cur.execute(select_min_date_query)
        min_date_lstm = cur.fetchone()[0]

        select_min_date_query = f"SELECT MIN(datetime) FROM {table_name_prediction_xgb};"
        cur.execute(select_min_date_query)
        min_date_xgboost = cur.fetchone()[0]

        earliest_date = min(min_date_lstm, min_date_xgboost)

        select_max_date_query = f"SELECT MAX(datetime) FROM {table_name};"
        cur.execute(select_max_date_query)
        max_date = cur.fetchone()[0]

        start_default_date = max_date - timedelta(days=1)


        response[sensor_id]["earliest_date"] = earliest_date
        response[sensor_id]["max_date"] = max_date
        response[sensor_id]["start_default_date"] = start_default_date
        response[sensor_id]["end_default_date"] = max_date

    cur.close()
    conn.close()

    return response
