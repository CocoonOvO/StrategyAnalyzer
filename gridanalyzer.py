from math import floor
from baseanalyzer import BaseAnalyzer,Post

class Grid():
    def __init__(self,gird_wid,first_value,base_value=0):
        # 实现网格机制。
        # gird_wid：网格宽度，固定值
        # first_value: 起始位置，也就是初始价格，初始化时会自动调整到最近的网格边上
        # base_value，网格基准，可以认为是0坐标，用于配合宽度计算网格线的具体位置。默认为0方便计算，也可以设置为和first_value相同从而让初始值做网格基准
        self.wid = gird_wid
        self.base_value = base_value
        self.value = self.round(first_value)
    
    def round(self, value):
        # 得到与某个点最接近的网格值
        return round((value-self.base_value)/self.wid)*self.wid+self.base_value
    
    def gird_up(self,delta:int,start_value=None):
        # 获得某个位置上升/下降一定格子后的位置
        start_value = round(start_value) if start_value else self.value
        return start_value+delta*self.wid

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

class PostGridAnalyzer(BaseAnalyzer):
    def __init__(self,wealth,base_count,base_price,meta_count,gird_wid,buyin_weight=5):
        super().__init__(wealth, base_count, base_price)
        self.gird_wid = gird_wid
        self.price = base_price
        self.meta_count = meta_count
        self.buyin_weight = buyin_weight
        # 网格初始化，添加初始挂单
        self.gird = Grid(gird_wid,base_price)
        for i in range(1,6):
            self.post(Post(Post.SELL,self.gird.gird_up(i),meta_count))
        self.post(Post(Post.BUY,self.gird.gird_up(-5),meta_count))
    
    def analyze(self, price):
        # 核心的算法，考虑中
        return super().analyze(price)