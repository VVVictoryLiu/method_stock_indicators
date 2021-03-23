# method_stock_indicators
股票/期货技术指标计算方法包，每日更新

### MA(series,n)
关于series的n日移动平均

### EMA(series,n)
关于series的n日指数移动平均

### MACD(series)
计算关于series的MACD指标

### macd_trigger(series_macd)
返回基于macd指标的买卖信号

### SAR(price_high, price_low, price_close, n=4, af=0.04, step=0.04, extrme=0.2)
抛物线指标，返回sar值和sar通道种类

### draw_sar_point(channel)
基于sar通道种类的买卖信号

### boll(series,n)
n日布林线

### HisCost(price,pre_price,turn)
基于换手率和价格的成本估算

### ROC(Series,N,M)

ROC和MAROC指标的计算

### CCI(high,low,close,N)

CCI指标的计算

### MTM(Series,N,M)

返回MTM和MTMMA指标

### WR(close,high,low,N)

返回N日威廉指标

### PSY(close,preclose,N)

返回N日PSY指标

### BS_option(S, K, T, r, sigma, option='call')

基于bs公式的期权价格

### BS_option_withQ(S, K, T,t, r,q, sigma, option='call')

带有股息的期权价格
