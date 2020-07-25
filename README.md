# method_stock_indicators
包含各种股票技术指标的计算方法

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
