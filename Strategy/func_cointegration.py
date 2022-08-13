# calculate cointegrated pairs

from config_strategy_api import z_score_window
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd
import numpy as np
import math

# calculate z-score
def calculate_zscore(spread):

    #

    # https://robotwealth.com/rolling-and-expanding-windows-for-dummies/
    # rolling window
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window = z_score_window).mean()
    print(mean)
    std = df.rolling(center = False, window = z_score_window).std()
    print(std)
    x = df.rolling(center=False, window=1).mean()
    df["zscore"] = (x-mean)/std
    return df["zscore"].astype(float).values 


# Calculate spread
def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - (pd.Series(series_2) * hedge_ratio)
    return spread

# Calculate co-integration
def calculate_cointegration(series_1, series_2):

    # The null hypothesis is no cointegration

    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0] # t_value
    p_value = coint_res[1] # p_value
    critical_value = coint_res[2][1] # c_value
    model = sm.OLS(series_1, series_2).fit() # calculating hedge ratio
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)
    zero_corossings = len(np.where(np.diff(np.sign(spread)))[0])
    if p_value < 0.5 and coint_t < critical_value:
        coint_flag = 1
    return (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), round(hedge_ratio, 2), zero_corossings)



# Put close prices into a list
def extract_close_prices(prices):
    close_prices=[]
    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        close_prices.append(price_values["close"])
    # print(close_prices)
    return close_prices




def get_cointegrated_pairs(prices):
    # Loop through coins and check for co-integration
    coint_pair_list = []
    included_list = []
    for sym_1 in prices.keys():
        
        # Check each coin against the first (sym_1)
        for sym_2 in prices.keys():
            if sym_2 != sym_1:
                
                # get unique combination id and ensure one off check
                sorted_caharacters = sorted(sym_1 + sym_2)
                unique = "".join(sorted_caharacters)
                if unique in included_list:
                    break

                # get close prices
                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])
                

                #Check for cointegration and add cointegrated pair
                coint_flag, p_value, t_value, c_value, hedge_ration, zero_crossings = calculate_cointegration(series_1, series_2)

                if coint_flag == 1:
                    included_list.append(unique)
                    coint_pair_list.append({
                        "sym_1": sym_1,
                        "sym_2": sym_2,
                        "p_value": p_value,
                        "t_value": t_value,
                        "c_value": c_value,
                        "hedge_ratio": hedge_ration,
                        "zero_crossings":zero_crossings
                    })

    df_coint = pd.DataFrame(coint_pair_list)
    df_coint = df_coint.sort_values("zero_crossings", ascending=False)
    df_coint.to_csv("2_cointegrated_pairs.csv")
    return df_coint
                     
                