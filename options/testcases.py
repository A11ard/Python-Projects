
"""
yyyinput = {"call": , "option": , "stock": ,
        "x" : , "r" : , "t": , "vol": , "cdiv": }

yyy = bsm(**yyyinput)

a = bsm(False,None, 75, 70, .09, 150/365, .35, 0)
print(a.get_price())

a.call = True
print(a.get_price())

b = bsm(True, None, 110, 105, .11, 43/365, .25, 0)
print(b.get_price())
print(a)

c = bsm(False,None, 110, 140, .11, 43/365, .25, 0)
print(c.get_price())


c.vol = None
a.option = 10.826
print("out", a.iv())


print("-------------------greeks-----------------------")

yyyinput = {"call":True , "option": None , "stock": 60 ,
        "x" : 70, "r" : .06, "t": 90, "vol": .4, "cdiv": 0}

yyy = bsm(**yyyinput)

print(yyy.get_price())
print(yyy.delta())
print(yyy.gamma())
print(yyy.theta())
print(yyy.vega())
print(yyy.rho())

print("---------------------greeks---------------------")

yyyinput = {"call":False , "option": None , "stock": 60 ,
        "x" : 70, "r" : .06, "t": 90, "vol": .4, "cdiv": 0}

yyy = bsm(**yyyinput)

print(yyy.get_price())
print(yyy.delta())
print(yyy.gamma())
print(yyy.theta())
print(yyy.vega())
print(yyy.rho())

print("---------------------------------known_div_price---------------")

yyyinput = {"call":False , "option": None , "stock":102 ,
        "x" : 100, "r" : .09, "t": 150, "vol": .3, "cdiv": 0}

yyy = bsm(**yyyinput)

print(yyy)
print(yyy.get_price())
print(yyy.known_div_price([(3,90)]))

print("---------------------------------known_div_price---------------")

yyyinput = {"call":True , "option": None , "stock":102 ,
        "x" : 100, "r" : .09, "t": 150, "vol": .3, "cdiv": 0}

yyy = bsm(**yyyinput)

print(yyy)
print(yyy.get_price())
print(yyy.known_div_price([(3,90)]))

"""
