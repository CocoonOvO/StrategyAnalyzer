from abc import ABC, abstractmethod

class Post():
    BUY = 'buy'
    SELL = 'sell'
    def __init__(self,post_type,post_price,count):
        self.post_type = post_type if (post_type==Post.BUY or post_type==Post.SELL) else Post.SELL
        self.post_price = post_price
        self.count = count

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
        self.posts:list[Post] = []

    def buy(self,count,price,fet=0):
        total_price = count*price
        if total_price > self.wealth:
            return False
        self.wealth -= total_price*(1+fet)
        self.incount += count
        self.wealth_list.append(self.wealth)
        self.count_list.append(self.incount)
        self.buy_count += 1
        return True
    
    def sell(self,count,price,fet=0):
        if count > self.incount:
            return False
        self.incount -= count
        self.wealth += count*price*(1-fet)
        self.wealth_list.append(self.wealth)
        self.count_list.append(self.incount)
        self.sell_count += 1
        return True
    
    def post(self,post:Post):
        self.posts.append(post)
    
    @abstractmethod
    def analyze(self,price):
        pass
