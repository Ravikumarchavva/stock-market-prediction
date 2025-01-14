from datetime import datetime
from time import sleep

from lumibot.backtesting import YahooDataBacktesting
from lumibot.credentials import broker
from lumibot.credentials import IS_BACKTESTING
from lumibot.strategies import Strategy
from lumibot.traders import Trader

# Define the strategy
class BuyAndHold(Strategy):
    def __init__(self, broker=None):
        super().__init__(broker=broker)
        self.sleep_time = '10s'

    def on_trading_iteration(self):
        if self.first_iteration:
            symbol = 'NVDA'
            price = self.get_last_price(symbol)
            quantity = self.cash // price
            order = self.create_order(symbol, quantity, 'buy')
            self.submit_order(order)

if __name__ == '__main__':
    if IS_BACKTESTING:
        start = datetime(2023, 11, 12)
        end = datetime(2024, 11, 11)
        BuyAndHold.backtest(YahooDataBacktesting, start, end)
    else:
        strategy = BuyAndHold(broker=broker)
        trader = Trader()
        trader.add_strategy(strategy)

        # Add delay to avoid rate limit
        while True:
            try:
                trader.run_all()
                break
            except Exception as e:
                print(f"Error: {e}")
                sleep(60)  # Wait for 60 seconds before retrying
