from bearer import login
from orders import place_order
from stream import StreamHandler
from logic import StrategyLogic
import time

start_time = time.time()

def server_run_time():
    seconds = int(time.time() - start_time)
    hrs, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

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
            print("Signal: ", signal, "| Uptime: ", server_run_time())
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


