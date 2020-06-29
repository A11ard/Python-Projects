import scipy.stats as st
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from stock import stock

"""
unit of t is days. To adjust to match with the risk free rate (it is a yearly risk free rate),
it will be: e^(-r*(t/365)). The continuous dividend rate is also years

all options formulas from the book: Understanding Options, by Robert Kolb
"""

def pv_cont(A, time, dis):#present value, continuously discounted
    return A * math.exp(-(dis) * time / 365)

def nprime(x):
    return math.exp(-.5 * x * x) / (math.sqrt(2 * math.pi))

class bsm:
    def __init__(self, call, x, r, t, price=None, cdiv=0, stockprice=None, vol=None, stock=None, time_stock=None):
        self.call = call
        self.price = price
        self.x = x #exercise price
        self.r = r #risk free rate
        self.dte = t #days til expiration
        self.t = t/365 #this is what is actually put into the model
        self.cdiv = cdiv #continuously distributed dividend rate
        if (stock is not None) and (time_stock is not None):
            self.stockprice = stock.frame.loc[time_stock]['price']
            self.vol = stock.frame.loc[time_stock]['annual_vola']
            self.stock = stock
            self.time_stock = time_stock
            # self.history = [{
            #                     'option': self.get_price(),
            #                     'delta': self.delta(),
            #                     'theta': self.theta()/365, #divide by 365 to get the effect on price given a 1 DAY change
            #                     'vega': self.vega()/100, #divide by 100 because this represents a 1 POINT change in Volatility, which is a percetage
            #                     'rho' : self.rho(),
            #                     'gamma': self.gamma(),
            #                     'vol': self.vol,
            #                     'underlying': self.stockprice,
            #                     'time_stock': time_stock
            #                 }]
            self.history = pd.DataFrame(columns=['underlying', 'vol', 'option', 'dte','delta', 'theta', 'vega'])
            self.history.loc[time_stock] = [ self.stockprice, self.vol, self.get_price(), self.dte, self.delta(), self.theta()/365, self.vega()/100]
        else:
            self.stockprice = stockprice
            self.vol = vol #volatility (normally historical)

    def __str__(self):
        ret = 'CALL OPTION | ' if self.call else 'PUT OPTION | '
        ret += "risk free rate: {r} ".format(r = self.r)
        try:
            self.stock
            ret += '\n' + self.history.to_string()
            return ret
        except:
            ret += '| days til expiration: {dte} | volatility: {v} | continuous dividend: {cdiv} | stock price: {stock} | exercise price: {x}'.format(dte=self.dte, v=self.vol, cdiv=self.cdiv, stock=self.stockprice, x=self.x)
            ret += '\n option price: {pp}'.format(pp = self.get_price())
            return ret

    def d(self):
        try:
            d1 = (math.log(self.stockprice/self.x) + (self.r - self.cdiv + .5*self.vol*self.vol)*(self.t))/ (math.sqrt(self.t) * self.vol)
            d2 = d1 - (math.sqrt(self.t) * self.vol)
            return (d1,d2)
        except MissingInputError:
            print('Needed inputs are missing!')

    def get_price(self): #black-scholes, merton adjustment for continuous dividends
        if self.t <= 0: return 0
        d1, d2 = self.d()
        if self.call:
            return self.stockprice*st.norm.cdf(d1)*math.exp(-(self.cdiv)*(self.t)) - self.x*math.exp(-(self.r * self.t))*st.norm.cdf(d2)
        else:
            return self.x*math.exp(-(self.r * self.t))*st.norm.cdf(-(d2)) - self.stockprice*st.norm.cdf(-(d1))*math.exp(-(self.cdiv)*(self.t))

    def iv(self):
        lo = 0.001
        hi = 2
        while lo < hi:
            mid = int((lo + hi)/2 * 1000) / 1000
            self.vol = mid
            c = self.get_price()
            if c < self.price:
                lo = mid
            else:
                if abs(c - self.price) < .01:
                    return mid
                hi = mid
        return mid

    def delta(self):
        if self.t <= 0: return 0
        d1, d2 = self.d()
        if self.call:
            return math.exp(-(self.cdiv)*self.t)*st.norm.cdf(d1)
        else:
            return math.exp(-(self.cdiv)*self.t)*(st.norm.cdf(d1)-1)

    def theta(self):
        if self.t <= 0: return 0
        d1, d2 = self.d()
        f = -1 * self.stockprice * nprime(d1) * self.vol * math.exp(-(self.cdiv)*self.t) / (2 * math.sqrt(self.t))
        s = self.r * self.x * math.exp(-(self.r) * self.t)
        if self.call:
            return f + self.cdiv * self.stockprice * st.norm.cdf(d1) * math.exp(-(self.cdiv)*self.t) - s * st.norm.cdf(d2)
        else:
            return f - self.cdiv * self.stockprice * st.norm.cdf(-(d1)) * math.exp(-(self.cdiv)*self.t) + s * st.norm.cdf(-(d2))

    def vega(self): #call and put vegas are identical
        if self.t <= 0: return 0
        d1, d2 = self.d()
        return self.stockprice * math.sqrt(self.t) * nprime(d1) * math.exp(-(self.cdiv)*(self.t))

    def rho(self):
        if self.t <= 0: return 0
        d1, d2 = self.d()
        if self.call:
            return self.stockprice * self.t * math.exp(-(self.r)*(self.t)) * st.norm.cdf(d2)
        else:
            return -1 * self.stockprice * self.t * math.exp(-(self.r)*(self.t)) * st.norm.cdf(-(d2))

    def gamma(self): #call and put gammas are identical when all else are equal
        if self.t <= 0: return 0
        d1, d2 = self.d()
        return nprime(d1) * math.exp(-(self.cdiv)*(self.t)) / (self.stockprice * self.vol * math.sqrt(self.t))

    def known_div_price(self, divs): #take a list of dividends and how far out they are from today (in days)
        # example: [(3,56),(3,86),(4,120)] ==> $3 dividend 56 days later, $3 86 days later, and $4 120 days later
        pv_divs = 0
        discount = self.r
        for date in divs:
            if date[1] < self.t * 365:
                pv_divs += pv_cont(date[0],date[1],discount)
        self.stockprice -= pv_divs
        ret = self.get_price()
        self.stockprice += pv_divs
        return ret

    def kd_to_cont_price(self, div, days): #transforms a known dividend to continuous dividend rate
        #asdf
        save = self.cdiv
        self.cdiv += -(math.log((self.stockprice - div) / self.stockprice) * 365 / days)
        ret = self.get_price()
        self.cdiv = save
        return ret

    def fill(s): #fill for the Greeks, volatility, and underlying for all the remaining avaiable times
        try:
            s.stock
        except NoUnderLyingStock:
            pass
        df = s.stock.frame
        for i in range(s.time_stock+1, df.shape[0]):
            s.stockprice = df.loc[i]['price']
            s.vol = df.loc[i]['annual_vola']
            s.dte -= 1
            s.t = s.dte / 365
            s.history.loc[i] = [s.stockprice, s.vol, s.get_price(), s.dte, s.delta(), s.theta()/365, s.vega()/100]
            if s.dte == 1:
                break

    def graph(self, deth = True):
        df = self.history
        option = df['option']
        delta = df['delta']
        theta = df['theta']
        vega = df['vega']
        underlying = df['underlying']
        volatility = df['vol']
        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        plt.ylabel('premium')
        ax1.plot(option ,'red')
        if deth:
            ax2 = fig.add_subplot(222)
            plt.ylabel('delta')
            ax2.plot(delta ,'blue')
            ax3 = fig.add_subplot(223)
            plt.ylabel('theta')
            ax3.plot(theta ,'blue')
        else:
            ax2 = fig.add_subplot(222)
            plt.ylabel('vega')
            ax2.plot(vega ,'blue')
            ax3 = fig.add_subplot(223)
            plt.ylabel('volatility')
            ax3.plot(volatility ,'blue')
        ax4 = fig.add_subplot(224)
        plt.ylabel('Price of underlying')
        ax4.plot(underlying ,'red')


if __name__ == '__main__':
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    s1 = stock(100, .005, .05)
    s1.gbm(100)
    c1 = bsm(call=True, x=100, r=.05, t=45, stock=s1, time_stock=40)
    c1.fill()
    c2 = bsm(call=True, x=100, r=.05, t=30, stock=s1, time_stock=40)
    c2.fill()
    plt.xlabel('stock days')
    plt.ylabel('vega')
    plt.plot(c1.history['vega'], 'orange', label='t=45')
    plt.plot(c2.history['vega'], 'grey', label='t=30')
    plt.legend(loc="upper right")
    plt.show()
