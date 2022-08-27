# calculate cointegrated pairs

from config_execution import z_score_window
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd
import numpy as np

# calculate z-score
def calculate_zscore(spread):

    # https://robotwealth.com/rolling-and-expanding-windows-for-dummies/
    # rolling window
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window = z_score_window).mean()
    std = df.rolling(center = False, window = z_score_window).std()
    x = df.rolling(center=False, window=1).mean()
    df["zscore"] = (x-mean)/std
    return df["zscore"].astype(float).values 


# Calculate spread
def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - (pd.Series(series_2) * hedge_ratio)
    return spread

# Calculate co-integration
def calculate_metrics(series_1, series_2):
    # The null hypothesis is no cointegration
    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0] # t_value
    p_value = coint_res[1] # p_value
    critical_value = coint_res[2][1] # c_value
    model = sm.OLS(series_1, series_2).fit() # calculating hedge ratio
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)
    zscore_list = calculate_zscore(spread)
    if p_value < 0.5 and coint_t < critical_value:
        coint_flag = 1
    return (coint_flag, zscore_list.tolist())
                     


