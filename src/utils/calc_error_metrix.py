import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def symmetric_mean_absolute_percentage_error(y_true, y_pred):
    return 100 * np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred)))


def normalized_root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred)) / (np.max(y_true) - np.min(y_true))


def mean_absolute_range_normalized_error(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred) / (np.max(y_true) - np.min(y_true))


def mean_absolute_scaled_error(y_true, y_pred):
    naive_forecast = y_true.shift(1).dropna()
    return mean_absolute_error(y_true[1:], y_pred[1:]) / mean_absolute_error(y_true[1:], naive_forecast)


def weighted_mean_absolute_percentage_error(y_true, y_pred):
    return np.sum(np.abs(y_true - y_pred)) / np.sum(np.abs(y_true)) * 100


def metrix_all(col_time, col_target, df_evaluetion, df_comparative):
    y_true = df_comparative[col_target].values
    min_non_zero = np.min(y_true[y_true != 0])

    # Заменяем нули на минимальное ненулевое значение
    y_true = np.where(y_true == 0, min_non_zero, y_true)
    y_pred = df_evaluetion[col_target].values

    # Преобразуем в массивы numpy для работы с математическими функциями
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    y_true = pd.to_numeric(y_true, errors='coerce')
    y_pred = pd.to_numeric(y_pred, errors='coerce')


    if np.any(np.isnan(y_true)) or np.any(np.isnan(y_pred)):
        raise ValueError("y_true или y_pred содержат NaN значения.")
    if np.any(np.isinf(y_true)) or np.any(np.isinf(y_pred)):
        raise ValueError("y_true или y_pred содержат бесконечные значения.")

    metrics = {
        'MAE': mean_absolute_error(y_true, y_pred),
        'MSE': mean_squared_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'MAPE': mean_absolute_percentage_error(y_true, y_pred),
        'R2': r2_score(y_true, y_pred),
        'sMAPE': symmetric_mean_absolute_percentage_error(y_true, y_pred),
        'NRMSE': normalized_root_mean_squared_error(y_true, y_pred),
        'MARNE': mean_absolute_range_normalized_error(y_true, y_pred),
        'WMAPE': weighted_mean_absolute_percentage_error(y_true, y_pred)
    }
    df_metrics = pd.DataFrame({
        col_time: df_comparative[col_time],
        'MAE': np.abs(y_true - y_pred),
        'MSE': (y_true - y_pred) ** 2,
        'RMSE': np.sqrt((y_true - y_pred) ** 2),
        'MAPE': np.abs((y_true - y_pred) / y_true) * 100,
        'sMAPE': 100 * 2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred)),
        'NRMSE': np.sqrt((y_true - y_pred) ** 2) / (np.max(y_true) - np.min(y_true)),
        'MARNE': np.abs(y_true - y_pred) / (np.max(y_true) - np.min(y_true)),
        'WMAPE': np.abs(y_true - y_pred) / np.abs(y_true) * 100
    })
    return metrics, df_metrics
