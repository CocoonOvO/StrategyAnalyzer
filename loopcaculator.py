from financialsimulator import FinancialSimulator
from baseanalyzer import BaseAnalyzer

import copy

class LoopCaculatry:
    # 重复多次模拟，记录结果并统计
    # 其实需要考虑策略。其一是给simulator和analyzer都添加重置功能，然后重复运行，重置的循环，并记录必要的结果
    # 其二是初始化的simulator不更改，每次运行时复制一份出来用，并报错运行后的simulator。内从占用更大，不过更简单
    # 还是二吧，不差那些内存
    def __init__(self,simulator:FinancialSimulator):
        self.simulator = simulator
        self.analyzers = simulator.analyzers.keys()
        self.results:list[FinancialSimulator] = []
    
    def run(self, loop = 1):
        self.results = []
        for i in range(loop):
            sim:FinancialSimulator = copy.deepcopy(self.simulator)
            sim.main()
            self.results.append(sim)
    
    def report(self):
        # 统计结果
        print('***运行结果统计***')
        print('装载的投资策略: '+', '.join(self.analyzers))
        print('总分析次数: '+str(len(self.results)))
        print('**行情变化分析**')
        print('行情整体上升趋势的模拟数: {}, 占比{}'.format(len([i for i in self.results if i.price_list[-1]>i.price_list[0]]),str((len([i for i in self.results if i.price_list[-1]>i.price_list[0]])/len(self.results))*100)+'%'))
        print('模拟的初始价格: {}, 结束时的平均价格: {}'.format(self.simulator.base_price, sum([i.price_list[-1] for i in self.results])/len(self.results)))
        print('最高结束时价格: {}'.format(max([i.price_list[-1] for i in self.results])))
        print('最低结束时价格: {}'.format(min([i.price_list[-1] for i in self.results])))
        print('**不同投资策略分析**')
        for a in self.analyzers:
            print('*{}*'.format(a))
            print('最终盈利数: {}, 占比{}'.format(len([s for s in self.results if s.analyzers[a].wealth_list[-1]>s.analyzers[a].base_wealth]),str(len([s for s in self.results if s.analyzers[a].wealth_list[-1]>s.analyzers[a].base_wealth])/len(self.results)*100)+'%'))
            avg_a_wealth = sum([s.analyzers[a].wealth_list[-1]-s.analyzers[a].base_wealth for s in self.results])/len(self.results)
            print('平均利润: {}, 平均利润率: {}'.format(avg_a_wealth,str(avg_a_wealth/self.simulator.analyzers[a].base_wealth*100)+'%'))
            max_a_wealth = max([s.analyzers[a].wealth_list[-1]-s.analyzers[a].base_wealth for s in self.results])
            print('最高利润: {}, 最大利润率: {}'.format(max_a_wealth,str(max_a_wealth/self.simulator.analyzers[a].base_wealth*100)+'%'))
            min_a_wealth = min([s.analyzers[a].wealth_list[-1]-s.analyzers[a].base_wealth for s in self.results])
            print('最大亏损: {}, 最大亏损率: {}'.format(min_a_wealth,str(min_a_wealth/self.simulator.analyzers[a].base_wealth*100)+'%'))