import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

#st.norm.cdf(d1)

class stock:
    def __init__(s, price=None, mu=None, sd=None ):
        s.price = price
        s.mu = mu
        s.sd = sd
        s.time = 0
        s.frame = pd.DataFrame(columns=['time', 'price', 'lreturn', 'stdv_last10', 'annual_vola'])

    def __str__(s):
        ret = s.frame.to_string(index=False)
        return ret
        """
    def expected(s, dt):
        return s.price * math.exp(s.mu * dt)

    def var(s, dt): #variance of stock when lognormal distribution
        return s.price ** 2 * math.exp(2 * s.mu * dt) * (math.exp(s.sd**2 * dt) - 1)
        """
    def gbm(s, length): #fills the frame up for a given length of time using geometric brownian motion model
        df = s.frame
        if df.shape[0] == 0:
            df.loc[0] = [s.time, s.price, None, None, None ]
        for i in range(1,length):
            log_return = np.random.normal( (s.mu - 0.5 * s.sd * s.sd), s.sd )
            s.time += 1
            last = s.price
            s.price *= math.exp(log_return)
            lreturn = math.log(s.price / last)
            df.loc[i] = [s.time, s.price, lreturn, None, None]
        df['stdv_last10'] = df['lreturn'].rolling(window=10, min_periods=10).std()
        df['annual_vola'] = df['stdv_last10'] * math.sqrt(252)

    def fill(s): #used if we already have the price history already-- now just find the volatilities
        df = s.frame
        price = df['price']
        lreturn = [None]
        for i in range(1,df.shape[0]):
            lreturn.append(math.log(price[i] / price[i-1]))
        df['time'] = [i for i in range(len(price))]
        df['lreturn'] = lreturn
        df['stdv_last10'] = df['lreturn'].rolling(window=10, min_periods=10).std()
        df['annual_vola'] = df['stdv_last10'] * math.sqrt(252)

    def graph(s, start=10): # start is the start time of the graph (ie if 10, then the graphing begins at t=10)
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        plt.ylabel("Price of stock")
        price_plot = s.frame['price'][start:]
        ax1.plot( price_plot,'red')
        ax2 =  fig.add_subplot(212)
        vola_plot = s.frame['annual_vola'][start:]
        plt.ylabel("Historical volatility")
        ax2.plot( vola_plot, 'blue')
        plt.show()

if __name__ == '__main__':
    s1 = stock(100, .005, .05)
    s1.gbm(100)
    #temp = s1.frame['price'].tolist()
    print(s1)
    print(s1.frame.index)
    s1.graph(20)
