import csv, time
import pandas as pd
from signalrcore.hub_connection_builder import HubConnectionBuilder
from datetime import datetime, time
from secretz import CONTRACT_ID


class StreamHandler:
    def __init__(self, jwt, contract_id=CONTRACT_ID):
        self.jwt = jwt
        self.contract_id = contract_id
        self.hub = None
        self.aggregate_time = "5min"

        # storage for current bar
        self.current_bar = None

        # CSV file paths
        self.ticks_csv = "ticks.csv"
        self.bars_csv = "bars.csv"

        # reset output files on start
        self._init_csv_files()

    def _init_csv_files(self):
        # ticks file
        with open(self.ticks_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["contract_id","symbolId","price","volume","timestamp"])
            writer.writeheader()

        # bars file
        with open(self.bars_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp","open","high","low","close","volume"])
            writer.writeheader()

    def connect(self):
        url = f"https://rtc.topstepx.com/hubs/market?access_token={self.jwt}"

        self.hub = (
            HubConnectionBuilder()
            .with_url(url, options={"access_token_factory": lambda: self.jwt})
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                "max_attempts": 999
            })
            .build()
        )

        self.hub.on_open(self._on_open)
        self.hub.on_close(lambda: print("Connection closed..."))
        self.hub.on_error(lambda e: print("Connection error:", e))
        self.hub.on("GatewayTrade", self._on_trade)

        print("Attempting connection…")
        self.hub.start()

    def _on_open(self):
        print("Connection successful!")
        self.hub.send("SubscribeContractTrades", [self.contract_id])
        print("Subscribed to:", self.contract_id)

    def in_rth_utc(ts: datetime):

        return time(14,30) <= ts.time() <= time(21,0)

    def _on_trade(self, args):
        try:
            contract_id, trades = args
            for trade in trades:
                ts = pd.to_datetime(trade["timestamp"], utc=True).to_pydatetime()
                if not self.in_rth_utc(ts):
                    continue

                self._write_tick(contract_id, trade)
                self._process_tick(trade)
        except Exception as e:
            print("Bad trade payload:", args, e)

    def _write_tick(self, contract_id, trade):
        row = {
            "contract_id": contract_id,
            "symbolId": trade.get("symbolId"),
            "price": trade.get("price"),
            "volume": trade.get("volume"),
            "timestamp": trade.get("timestamp"),
        }
        with open(self.ticks_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writerow(row)

    def _process_tick(self, trade):
        bar_time = pd.to_datetime(trade["timestamp"]).floor(self.aggregate_time)

        if (self.current_bar is None) or (bar_time != self.current_bar["timestamp"]):
            # write old bar if exists
            if self.current_bar is not None:
                with open(self.bars_csv, "a", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=self.current_bar.keys())
                    writer.writerow(self.current_bar)
                print("Bar Printed:", self.current_bar)

            # start new bar
            self.current_bar = {
                "timestamp": bar_time,
                "open": trade["price"],
                "high": trade["price"],
                "low": trade["price"],
                "close": trade["price"],
                "volume": trade["volume"]
            }
        else:
            # update bar
            self.current_bar["high"] = max(self.current_bar["high"], trade["price"])
            self.current_bar["low"] = min(self.current_bar["low"], trade["price"])
            self.current_bar["close"] = trade["price"]
            self.current_bar["volume"] += trade["volume"]