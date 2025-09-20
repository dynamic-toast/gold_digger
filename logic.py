import pandas as pd
import talib

class StrategyLogic:
    def __init__(self, bars_file="bars.csv"):
        self.bars_file = bars_file

    def signal(self):
        df = pd.read_csv(self.bars_file, parse_dates=["timestamp"])

        if df.empty:
            return None
        if len(df) < 40:
            return "INSUFFICIENT INDICATOR DATA"

        close = df["close"].astype(float).to_numpy()
        high = df["high"].astype(float).to_numpy()
        low = df["low"].astype(float).to_numpy()

        sma = talib.SMA(close, timeperiod=40)
        k, d = talib.STOCH(
            high, low, close,
            fastk_period=14,
            slowk_period=5, slowk_matype=1,
            slowd_period=5, slowd_matype=1
        )

        price = close[-1]
        sma_line = sma[-1]
        k_line, d_line = k[-1], d[-1]

        bullish = k_line > d_line and k[-2] <= d[-2]
        bearish = d_line > k_line and d[-2] <= k[-2]

        uptrend   = price > sma_line
        downtrend = price < sma_line

        if bullish and uptrend:
            signal = "BUY"
        elif bearish and downtrend:
            signal = "SELL"
        else:
            signal = "HOLD"

        return signal


