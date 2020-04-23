import scipy.stats as st
import math

"""
unit of t is days. To adjust to match with the risk free rate (it is a yearly risk free rate),
it will be: e^(-r*(t/365). The continuous dividend rate is also years

all options formulas from the book: Understanding Options, by Robert Kolb
"""

def pv_cont(A, time, dis):
    return A * math.exp(-(dis) * time / 365)

def nprime(x):
    return math.exp(-.5 * x * x) / (math.sqrt(2 * math.pi))

class bsm:
    def __init__(self, call, option, stock, x, r, t, vol, cdiv):
        self.call = call
        self.option = option
        self.stock = stock
        self.x = x
        self.r = r
        self.t = t/365
        self.vol = vol
        self.cdiv = cdiv

    def __str__(self):
        type = "call" if self.call else "put"
        ret =  """
        {ty} option
        option price: {price}
        stock price: {stock}
        strike price: {x}
        risk free rate: {r}
        time until expiration (days): {t}
        volatility: {vol}
        continuous dividend: {cdiv} """
        return ret.format(ty = type, price = self.option, stock = self.stock, x = self.x, r = self.r, t = self.t * 365, vol = self.vol, cdiv = self.cdiv)

    def d(self):
        d1 = (math.log(self.stock/self.x) + (self.r - self.cdiv + .5*self.vol*self.vol)*(self.t))/ (math.sqrt(self.t) * self.vol)
        d2 = d1 - (math.sqrt(self.t) * self.vol)
        return (d1,d2)

    def get_price(self): #black-scholes, merton adjustment for continuous dividends
        d1, d2 = self.d()
        if self.call:
            return self.stock*st.norm.cdf(d1)*math.exp(-(self.cdiv)*(self.t)) - self.x*math.exp(-(self.r * self.t))*st.norm.cdf(d2)
        else:
            return self.x*math.exp(-(self.r * self.t))*st.norm.cdf(-(d2)) - self.stock*st.norm.cdf(-(d1))*math.exp(-(self.cdiv)*(self.t))

    def iv(self):
        lo = 0.001
        hi = 2
        while lo < hi:
            mid = int((lo + hi)/2 * 1000) / 1000
            self.vol = mid
            c = self.get_price()
            if c < self.option:
                lo = mid
            else:
                if abs(c - self.option) < .01:
                    return mid
                hi = mid
        return mid

    def delta(self):
        d1, d2 = self.d()
        if self.call:
            return math.exp(-(self.cdiv)*self.t)*st.norm.cdf(d1)
        else:
            return math.exp(-(self.cdiv)*self.t)*(st.norm.cdf(d1)-1)

    def theta(self):
        d1, d2 = self.d()
        f = -1 * self.stock * nprime(d1) * self.vol * math.exp(-(self.cdiv)*self.t) / (2 * math.sqrt(self.t))
        s = self.r * self.x * math.exp(-(self.r) * self.t)
        if self.call:
            return f + self.cdiv * self.stock * st.norm.cdf(d1) * math.exp(-(self.cdiv)*self.t) - s * st.norm.cdf(d2)
        else:
            return f - self.cdiv * self.stock * st.norm.cdf(-(d1)) * math.exp(-(self.cdiv)*self.t) + s * st.norm.cdf(-(d2))

    def vega(self): #call and put vegas are identical
        d1, d2 = self.d()
        return self.stock * math.sqrt(self.t) * nprime(d1) * math.exp(-(self.cdiv)*(self.t))

    def rho(self):
        d1, d2 = self.d()
        if self.call:
            return self.stock * self.t * math.exp(-(self.r)*(self.t)) * st.norm.cdf(d2)
        else:
            return -1 * self.stock * self.t * math.exp(-(self.r)*(self.t)) * st.norm.cdf(-(d2))

    def gamma(self): #call and put gammas are identical when all else are equal
        d1, d2 = self.d()
        return nprime(d1) * math.exp(-(self.cdiv)*(self.t)) / (self.stock * self.vol * math.sqrt(self.t))

    def known_div_price(self, divs): #take a list of dividends and how far out they are from today (in days)
        # example: [(3,56),(3,86),(4,120)] ==> $3 dividend 56 days later, $3 86 days later, and $4 120 days later
        pv_divs = 0
        discount = self.r
        for date in divs:
            if date[1] < self.t * 365:
                pv_divs += pv_cont(date[0],date[1],discount)
        self.stock -= pv_divs
        ret = self.get_price()
        self.stock += pv_divs
        return ret

    def kd_to_cont_price(self, div, days): #transforms a known dividend to continuous dividend rate
        #asdf
        save = self.cdiv
        self.cdiv += -(math.log((self.stock - div) / self.stock) * 365 / days)
        ret = self.get_price()
        self.cdiv = save
        return ret

print("---------------------------------kd_to_cont_price---------------")

yyyinput = {"call":False , "option": None , "stock":60 ,
        "x" : 60, "r" : .09, "t": 180, "vol": .2, "cdiv": 0}

yyy = bsm(**yyyinput)

print(yyy)
print(yyy.get_price())
print(yyy.known_div_price([(2,90)]))
print(yyy.kd_to_cont_price(2,90))
