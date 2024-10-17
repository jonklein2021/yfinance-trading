import backtrader as bt
import yfinance as yf

# basic simple moving average crossover strategy from tutorial
class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

# get historical data from yfinance
data_df = yf.download('MSFT', start='2020-01-01', end='2022-01-01')

# convert yfinance df into bt's DataFeed format
data = bt.feeds.PandasData(dataname=data_df)

# int Cerebro 
cerebro = bt.Cerebro()

# add the data feed and strategy to Cerebro
cerebro.adddata(data)
cerebro.addstrategy(SmaCross)

# run and plot the strategy
cerebro.run()
cerebro.plot()
