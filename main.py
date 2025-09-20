from bearer import login
from orders import place_order
from stream import StreamHandler
from logic import StrategyLogic
import time

if __name__ == '__main__':
    def activate_bot():

        print("Logging in...")
        print()
        jwt = login()

        bot = StreamHandler(jwt)
        strat = StrategyLogic()

        bot.connect()

        while True:
            signal = strat.signal()
            print("Signal: ", signal)
            if signal:  # make sure signal isn't None
                place_order(jwt, signal)
            time.sleep(60)

print("Welcome to Gold Digger V1.0")
print()
print("Choose Task: ")
print()
print("1. Activate gold_digger trading bot")
print()
print("* To stop bot: Ctrl C in terminal")
task = int(input("Task: "))

if task == 1:
    try:
        activate_bot()

    except KeyboardInterrupt:
        print("Stopping...")

