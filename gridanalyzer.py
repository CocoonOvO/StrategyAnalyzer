from math import floor
from baseanalyzer import BaseAnalyzer

class DynamicGridAnalyzer(BaseAnalyzer):
    def __init__(self, wealth, base_count, base_price, meta_count, grid_percent=0.001,buyin_weight=5):
        super().__init__(wealth, base_count, base_price)
        self.grid_percent = grid_percent
        self.price = base_price
        self.meta_count = meta_count
        self.buyin_weight = buyin_weight
    
    def analyze(self, price):
        deltap = (price-self.price)/self.price
        if deltap > 0:
            grids = floor(deltap/self.grid_percent)
            if not self.sell(self.meta_count*grids,price):
                self.end = True
            self.price += self.base_price*self.grid_percent*grids
        elif deltap < 0:
            deltap = -deltap
            grids = floor(deltap/(self.grid_percent*self.buyin_weight))
            if not self.buy(self.meta_count*grids,price):
                self.end = True
            self.price -= self.base_price*self.grid_percent*grids
        return super().analyze(price)

class StaticGridAnalyzer(BaseAnalyzer):
    def __init__(self, wealth, base_count, base_price, meta_count, grid_percent=0.001,buyin_weight=5):
        super().__init__(wealth, base_count, base_price)
        self.grid_percent = grid_percent
        self.price = base_price
        self.meta_count = meta_count
        self.buyin_weight = buyin_weight
    
    def analyze(self, price):
        deltap = (price-self.price)/self.base_price
        if deltap > 0:
            grids = floor(deltap/self.grid_percent)
            if not self.sell(self.meta_count*grids,price):
                self.end = True
            self.price += self.base_price*self.grid_percent*grids
        elif deltap < 0:
            deltap = -deltap
            grids = floor(deltap/(self.grid_percent*self.buyin_weight))
            if not self.buy(self.meta_count*grids,price):
                self.end = True
            self.price -= self.base_price*self.grid_percent*grids
        return super().analyze(price)