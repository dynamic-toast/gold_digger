# gold_digger
Compatible with TopstepX API

***USE BOT AT OWN RISK: Users are fully responsible for their own gains/losses.

***IMPORTANT NOTES PLEASE READ: Live data stream will not print indicators until the bars.csv file has a sufficient amount of data. Ex. If SMA length is =40, 40 bars are needed to print that indicator, therefore it is recommended to warm up the bot with sufficient data.
If active 24/7 the bot will collect data from 9:30am to 4:00pm EST. Script does not remove bars.csv data, making it ideal for collecting historical data (needed for indicators). Fair warning, stop losses and take profits are not implemented directly in script. Risk          settings should be configured in TopstepX account settings. Script automatically aggregates data stream to 5 minute bars, to edit go to stream.py and change "5min". EX. self.aggregate_time = "1min", "5min", "15min", "1Hr". To stop the bot from running, enter Ctrl C.

Stochastics slow indicator uses line crossovers to signal a buy or sell response. Price also needs to be > SMA to long and < SMA to short.

created by Warren buffet
