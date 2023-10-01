import random
from typing import Callable
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示负号

from baseanalyzer import BaseAnalyzer

class FinancialSimulator():
    
    def set_model(self,price_model:Callable[['FinancialSimulator'],float]):
        self.price_model = price_model

    def __init__(self,base_price,price_model:Callable[['FinancialSimulator'],float], debug = False):
        self.base_price = base_price
        self.price = base_price
        self.price_list = [self.price]
        self.analyzers:map[str,BaseAnalyzer] = {}
        self.set_model(price_model)
        self.loop = 0
    
    def add_analyzer(self,name:str,analyzer:BaseAnalyzer):
        self.analyzers[name]=analyzer
    
    def checkout(self):
        price = self.price_model(self)
        self.price = price
        self.price_list.append(price)
        # 补充一个逻辑，当价格跌到基础价格的10%以下时，立刻全抛，同时无视负数
        if price < self.base_price*0.1:
            price = max(0,price)
            self.sell_all()
            return True
        for name,analyzer in self.analyzers.items():
            if not analyzer.end:
                analyzer.analyze(price)
        return all(analyzer.end for name,analyzer in self.analyzers.items())
    
    def main(self):
        while not self.checkout():
            self.loop += 1
            if self.loop%10 == 0:
                print('当前循环第{}次'.format(self.loop))
            if self.loop >= 100000:
                break
        self.sell_all()
        
    def sell_all(self):
        for n, a in self.analyzers.items():
            a.sell(a.incount,self.price)
    
    def print_statistics(self):
        print("模拟过程中金融产品的价格变化情况：")
        print(self.price_list)
        print("模拟过程中各个虚拟投资者的买入，卖出情况，以及虚拟投资者的资产(wealth),利润(资产和初始资产的差值)的变化情况：")
        profit_ranking = []
        duration_ranking = []
        for name, analyzer in self.analyzers.items():
            print(f"虚拟投资者{name}的买入，卖出情况：")
            print(f"买入次数：{analyzer.buy_count}，卖出次数：{analyzer.sell_count}")
            print(f"虚拟投资者{name}的资产变化情况：")
            print(analyzer.wealth_list)
            print(f"虚拟投资者{name}的利润变化情况：")
            profit = analyzer.wealth - analyzer.base_wealth
            profit_list = [wealth - analyzer.base_wealth for wealth in analyzer.wealth_list]
            print(profit_list)
            print(f"虚拟投资者{name}的持有数变化情况：")
            print(analyzer.count_list)
            # 添加到排名列表
            profit_ranking.append((name, profit))
            duration_ranking.append((name, len(profit_list)))
        # 输出排名
        profit_ranking.sort(key=lambda x: x[1], reverse=True)
        duration_ranking.sort(key=lambda x: x[1], reverse=True)
        print("利润排名：")
        for i, (name, profit) in enumerate(profit_ranking):
            print(f"{i+1}. {name}: {profit}")
        print("持续周期数排名：")
        for i, (name, duration) in enumerate(duration_ranking):
            print(f"{i+1}. {name}: {duration}")
        print("剩余份数")
        for n, a in self.analyzers.items():
            print('名称:{}, 剩余份数: {}'.format(n, a.incount))

    def plot_statistics(self):
        plt.figure(figsize=(10, 6))
        # 绘制金融产品价格变化图
        plt.subplot(221)
        plt.plot(self.price_list)
        plt.title("金融产品价格变化")
        plt.grid(True)
        min_price = min(self.price_list)
        max_price = max(self.price_list)
        plt.annotate(f'最低点: {min_price}', xy=(self.price_list.index(min_price), min_price), xytext=(self.price_list.index(min_price), min_price+5),
                    arrowprops=dict(facecolor='red', shrink=0.05))
        plt.annotate(f'最高点: {max_price}', xy=(self.price_list.index(max_price), max_price), xytext=(self.price_list.index(max_price), max_price+5),
                    arrowprops=dict(facecolor='green', shrink=0.05))
        
        # 绘制各个虚拟投资者的资产变化图
        plt.subplot(222)
        for name, analyzer in self.analyzers.items():
            wealth_list = analyzer.wealth_list
            plt.plot(wealth_list, label=name)
            min_wealth = min(wealth_list)
            max_wealth = max(wealth_list)
            plt.annotate(f'最低点: {min_wealth}', xy=(wealth_list.index(min_wealth), min_wealth), xytext=(wealth_list.index(min_wealth), min_wealth+5),
                        arrowprops=dict(facecolor='red', shrink=0.05))
            plt.annotate(f'最高点: {max_wealth}', xy=(wealth_list.index(max_wealth), max_wealth), xytext=(wealth_list.index(max_wealth), max_wealth+5),
                        arrowprops=dict(facecolor='green', shrink=0.05))
        plt.title("虚拟投资者资金变化")
        plt.grid(True)

        # 绘制投资者总收益变化图
        plt.subplot(223)
        for name, analyzer in self.analyzers.items():
            enr_list = [w-analyzer.base_wealth for w in analyzer.wealth_list]
            plt.plot(enr_list, label=name)
            min_enr = min(enr_list)
            max_enr = max(enr_list)
            plt.annotate(f'最低点: {min_enr}', xy=(enr_list.index(min_enr), min_enr), xytext=(enr_list.index(min_enr), min_enr+5),
                        arrowprops=dict(facecolor='red', shrink=0.05))
            plt.annotate(f'最高点: {max_enr}', xy=(enr_list.index(max_enr), max_enr), xytext=(enr_list.index(max_enr), max_enr+5),
                        arrowprops=dict(facecolor='green', shrink=0.05))
        plt.title('投资者总收益变化')
        plt.legend()
        plt.grid(True)

        # 绘制总资产变化图
        plt.subplot(224)
        for name, analyzer in self.analyzers.items():
            own_list = [analyzer.wealth_list[i] + analyzer.count_list[i]*self.price_list[i] for i in range(len(analyzer.wealth_list))]
            plt.plot(own_list, label=name)
            min_own = min(own_list)
            max_own = max(own_list)
            plt.annotate(f'最低点: {min_own}', xy=(own_list.index(min_own), min_own), xytext=(own_list.index(min_own), min_own+5),
                        arrowprops=dict(facecolor='red', shrink=0.05))
            plt.annotate(f'最高点: {max_own}', xy=(own_list.index(max_own), max_own), xytext=(own_list.index(max_own), max_own+5),
                        arrowprops=dict(facecolor='green', shrink=0.05))
        plt.title('投资者总资产变化')
        plt.legend()
        plt.grid(True)


        # 优化布局并显示图像
        plt.tight_layout()
        plt.show()


def fixedprobability(upprob:float,delta:float):
    def model(self:FinancialSimulator):
        p = random.random()
        if p <= upprob:
            return self.price + delta
        else:
            return self.price - delta
    return model

def dynamicfixedprobability(upprob:float,deltapercent:float):
    def model(self:FinancialSimulator):
        p = random.random()
        if p <= upprob:
            return self.price*(1+deltapercent)
        else:
            return self.price*(1-deltapercent)
    return model

def momentum_reversal_model(momentum_prob: float, reversal_prob: float, delta: float):
    def model(self: FinancialSimulator):
        p = random.random()
        if len(self.price_list) < 2:
            # 如果没有足够的历史数据，就使用固定概率模型
            if p <= momentum_prob:
                return self.price + delta
            else:
                return self.price - delta
        else:
            # 如果有足够的历史数据，就考虑动量效应和反转效应
            if self.price_list[-1] > self.price_list[-2]:
                # 如果最近的价格上涨，那么有momentum_prob的概率继续上涨，
                # 有reversal_prob的概率发生反转下跌
                if p <= momentum_prob:
                    return self.price + delta
                elif p <= momentum_prob + reversal_prob:
                    return self.price - delta
                else:
                    return self.price
            else:
                # 如果最近的价格下跌，那么有momentum_prob的概率继续下跌，
                # 有reversal_prob的概率发生反转上涨
                if p <= momentum_prob:
                    return self.price - delta
                elif p <= momentum_prob + reversal_prob:
                    return self.price + delta
                else:
                    return self.price
    return model
