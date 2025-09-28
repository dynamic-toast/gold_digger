import pandas as pd
import talib

class GoldDigger:
    def __init__(self, bars_file="bars.csv"):
        self.bars_file = bars_file

    def signal(self):
        
        df = pd.read_csv(self.bars_file, parse_dates=["timestamp"])

        if df.empty:
            return "INSUFFICIENT DATA"
        if len(df) < 180:
            return "INSUFFICIENT DATA"

        close = df["close"].astype(float).to_numpy()
        high = df["high"].astype(float).to_numpy()
        low = df["low"].astype(float).to_numpy()

        sma = talib.SMA(close, timeperiod=180)
        k, d = talib.STOCH(
            high, low, close,
            fastk_period=18,
            slowk_period=3, slowk_matype=3,
            slowd_period=3, slowd_matype=3
        )

        price = close[-1]
        sma_line = sma[-1]
        k_line, d_line = k[-1], d[-1]
        print(f"LOG: K_line current price: {k_line}", f"D_line current price: {d_line}")

        bullish = (k_line > 75) and (d_line > 75)
        bearish = (k_line < 20) and (d_line < 20)

        uptrend   = price > sma_line
        downtrend = price < sma_line

        if bullish and uptrend:
            return  {"side": "BUY", "close": price}
        elif bearish and downtrend:
            return {"side": "SELL", "close": price}
        else:
            return {"side": "HOLD", "close": price}

