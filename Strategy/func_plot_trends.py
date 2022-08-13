from func_cointegration import extract_close_prices
from func_cointegration import calculate_cointegration
from func_cointegration import calculate_spread 
from func_cointegration import calculate_zscore
import matplotlib.pyplot as plt
import pandas as pd

# Plot prices / trends

def plot_trends(sym_1, sym_2, price_data):
    
    prices_1 = extract_close_prices(price_data[sym_1])
    prices_2 = extract_close_prices(price_data[sym_2])

    cont_flag, p_value, t_value, c_value, hedge_ratio, zero_crossing = calculate_cointegration(prices_1, prices_2)
    spread = calculate_spread(prices_1, prices_2, hedge_ratio)
    z_score = calculate_zscore(spread)

    # calculate percentage changes
    df = pd.DataFrame(columns=[sym_1, sym_2])
    df[sym_1] = prices_1
    df[sym_2] = prices_2
    
    df[f"{sym_1}_pct"] = df[sym_1]/prices_1[0]
    df[f"{sym_2}_pct"] = df[sym_2]/prices_2[0]

    series_1 = df[f"{sym_1}_pct"].astype(float).values
    series_2 = df[f"{sym_2}_pct"].astype(float).values

    # Save results for backtesting
    df_2 = pd.DataFrame()
    df_2[sym_1] = prices_1
    df_2[sym_2] = prices_2
    df_2["Spread"] = spread
    df_2["Zscore"] = z_score
    df_2.to_csv("3_backtesting_file.csv")
    print("File for backtesting saved.")

    # Plot charts
    
    fig, axs = plt.subplots(3, figsize=(16, 8))
    fig.suptitle(f"Price and Spread = {sym_1} vs {sym_2}")
    axs[0].plot(series_1)
    axs[0].plot(series_2)
    axs[1].plot(spread)
    axs[2].plot(z_score)
    plt.show()