from financialsimulator import FinancialSimulator,dynamicfixedprobability,momentum_reversal_model
from gridanalyzer import StaticGridAnalyzer,DynamicGridAnalyzer
from poweranalyzer import PowerAnalyzer

# 初始化模拟器
simulator = FinancialSimulator(base_price=100, price_model=momentum_reversal_model(momentum_prob=0.6, reversal_prob=0.3, delta=1)) 
#simulator = FinancialSimulator(base_price=100, price_model=dynamicfixedprobability(0,0.01)) 

# 添加分析器
#simulator.add_analyzer('dynamic', DynamicGridAnalyzer(wealth=100000000, base_count=1000, base_price=simulator.base_price, meta_count=10, grid_percent=0.01,buyin_weight=10))
simulator.add_analyzer('static', StaticGridAnalyzer(wealth=100000000, base_count=1000, base_price=simulator.base_price, meta_count=10, grid_percent=0.01,buyin_weight=10))
#simulator.add_analyzer('power',PowerAnalyzer(wealth=100000000,base_count=1000,base_price=simulator.base_price,meta_count=10,delta_percent=0.01, pow=2))

# 运行模拟器
simulator.main()

# 打印和绘制统计信息
simulator.print_statistics()
simulator.plot_statistics()

