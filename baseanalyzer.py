from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    def __init__(self,wealth,base_count,base_price):
        self.base_wealth = wealth
        self.base_price = base_price
        self.wealth = wealth - base_count*base_price
        self.incount = base_count
        self.end = False
        self.wealth_list = [self.wealth]
        self.count_list = [self.incount]
        self.buy_count = 0
        self.sell_count = 0
    
    def buy(self,count,price):
        total_price = count*price
        if total_price > self.wealth:
            return False
        self.wealth -= total_price
        self.incount += count
        self.wealth_list.append(self.wealth)
        self.count_list.append(self.incount)
        self.buy_count += 1
        return True
    
    def sell(self,count,price):
        if count > self.incount:
            return False
        self.incount -= count
        self.wealth += count*price
        self.wealth_list.append(self.wealth)
        self.count_list.append(self.incount)
        self.sell_count += 1
        return True

    @abstractmethod
    def analyze(self,price):
        pass