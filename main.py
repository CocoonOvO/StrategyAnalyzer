from financialsimulator import FinancialSimulator,dynamicfixedprobability,momentum_reversal_model
from gridanalyzer import StaticGridAnalyzer,DynamicGridAnalyzer
from poweranalyzer import PowerAnalyzer
from loopcaculator import LoopCaculatry

# 初始化模拟器
simulator = FinancialSimulator(base_price=5, price_model=momentum_reversal_model(momentum_prob=0.6, reversal_prob=0.3, delta=0.01)) 
#simulator = FinancialSimulator(base_price=100, price_model=dynamicfixedprobability(0,0.01)) 

# 添加分析器
simulator.add_analyzer('dynamic', DynamicGridAnalyzer(wealth=1000, base_count=100, base_price=simulator.base_price, meta_count=10, grid_percent=0.01,buyin_weight=5))
simulator.add_analyzer('static', StaticGridAnalyzer(wealth=1000, base_count=100, base_price=simulator.base_price, meta_count=10, grid_percent=0.01,buyin_weight=5))
#simulator.add_analyzer('power',PowerAnalyzer(wealth=1000,base_count=100,base_price=simulator.base_price,meta_count=10,delta_percent=0.01, pow=2))

''' 运行模拟器
simulator.main()

 打印和绘制统计信息
simulator.print_statistics()
simulator.plot_statistics()'''

# 进行重复模拟
loopc = LoopCaculatry(simulator=simulator)
loopc.run(loop = 1000)
loopc.report()