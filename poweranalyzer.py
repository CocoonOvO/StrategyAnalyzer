from baseanalyzer import BaseAnalyzer

class PowerAnalyzer(BaseAnalyzer):
    def __init__(self, wealth, base_count, base_price,meta_count,delta_percent=0.001,pow=2):
        super().__init__(wealth, base_count, base_price)
        self.meta_count = meta_count
        self.price = base_price
        self.delta_percent = delta_percent
        self.pow = pow
        self.p = 1
    
    def analyze(self, price):
        if price-self.price > self.base_price*self.delta_percent:
            if not self.sell(self.meta_count*self.p,price):
                self.end = True
                return super().analyze(price)
            self.p = max(1, self.p/self.pow)
        elif self.price - price > self.base_price*self.delta_percent:
            if not self.buy(self.meta_count*self.p,price):
                self.end = True
                return super().analyze(price)
            self.p = self.p*self.pow
        return super().analyze(price)