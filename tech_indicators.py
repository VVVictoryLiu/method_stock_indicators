import numpy as np
import pandas as pd


def MA(series,days):
    '''
    n日简单移动平均
    '''
    dict={}
    dict[0] = series
    for day in range(1,days):
        dict[day] = series.shift(day)
    temp = pd.DataFrame(dict)
    temp = pd.DataFrame(temp.mean(skipna=False, axis=1),columns=['MA'])
    return temp['MA']

def EMA(series,n):
    '''
    n日指数移动平均，由于需要用到历史移动平均值，故该值将逐步回归真实值
    '''
    ema = series[0]
    EMA = []
    for i in series:
        ema = (2*i + (n-1)*ema)/(n+1)
        EMA.append(ema)
    return pd.Series(EMA)


def MACD(series):
    '''
    MACD值
    '''
    quick_line = EMA(series, 12)
    slow_line = EMA(series, 26)
    DIF = quick_line - slow_line
    DEA = EMA(DIF, 9)
    macd = 2 * (DIF - DEA)

    return macd

def macd_trigger(series):
    '''
    基于MACD值构建的买卖信号
    '''
    def gen_flag(dataframe):
        muti = dataframe['pre_macd'] * dataframe['macd']
        if muti <0:
            if dataframe['pre_macd']<0:
                return 'buy' #买点信号
            else:
                return 'sale' #卖点信号
        else:
            return 'waitting'

    pre_macd = series.shift(1)
    data = pd.DataFrame({'pre_macd':pre_macd,'macd':series})
    data['macd_trigger'] = data.apply(gen_flag,axis=1)
    return data['macd_trigger']


def SAR(price_high, price_low, price_close, n=4, af=0.04, step=0.04, extrme=0.2):
    '''
    抛物线指标SAR，由于需要用到历史的SAR值，故该值将逐步回归真实值

    参数：
    n:  转向后计算的最高/最低价
    af: 初始动量
    step:   递增动量
    extrem: 最高动量
    '''
    price_high = price_high.copy().reset_index(drop=True)
    price_low = price_low.copy().reset_index(drop=True)
    price_close = price_close.copy().reset_index(drop=True)
    sar = []
    sar_channel_type = []
    af = 0.04
    step = 0.04
    # 前n-1天无法计算，使用收盘价代替
    sar.extend(price_close[:n - 1])
    sar_channel_type.extend([0 for _ in range(n - 1)])
    # 第n天另行计算

    if price_close[n - 1] >= sar[0]:
        sar.append(min(price_low[:n]))
        sar_channel_type.append(1)
        ep = price_high[n-1]
        trend = 1
    else:
        sar.append(max(price_high[:n]))
        sar_channel_type.append(-1)
        ep = price_low[n-1]
        trend = 0

    # n天后开始循环计算
    for i in range(len(sar), len(price_close)):
        if trend == 1:  # 上升通道
            last_sar = sar[i-1]
            if last_sar >= price_low[i]:  # 最低价下穿通道底部，下一个循环进入下降通道
                af = 0.04
                if(price_high[i-1]<price_high[i]):
                    sar_high = 2*price_high[i] - price_high[i-1]
                else:
                    sar_high = price_high[i-1]
                sar.append(sar_high)
                sar_channel_type.append(-1)
                trend = 0
                ep = price_low[i]
                continue
            else:  # 上升通道
                if price_high[i] > ep:
                    ep = price_high[i]
                    if (af < 0.2):
                        af = af + step

                new_sar = last_sar + af * (ep - last_sar)

                ceiling = min(price_low[i-1],price_low[i])
                if new_sar > ceiling:  # 通道底部不可高于股价
                    new_sar = ceiling

                sar.append(new_sar)
                sar_channel_type.append(1)


        else:  # 下降通道
            last_sar = sar[i-1]
            if last_sar < price_high[i]:  # 弹进上升通道
                af = 0.04
                if(price_low[i]<price_low[i-1]):
                    sar_low = 2*price_low[i]-price_low[i-1]
                else:
                    sar_low = price_low[i-1]
                sar.append(sar_low)
                sar_channel_type.append(1)
                trend = 1
                ep = price_high[i]

                continue
            else:
                if price_low[i] < ep:
                    ep = price_low[i]
                    if (af < 0.2):
                        af = af + step

                new_sar = last_sar - af * (-ep + last_sar)
                floor = min(price_high[i-1],price_high[i])
                if new_sar < floor:  # 下降通道不可低于股价
                    new_sar = floor
                sar.append(new_sar)
                sar_channel_type.append(-1)


    return pd.Series(sar,name=None), pd.Series(sar_channel_type,name=None)


def draw_sar_point(channel):
    '''
    基于SAR指标的买卖信号

    channel为sar方法返回的sar序列
    '''
    def generate_sign(dataframe):
        if dataframe['sign_num'] == -1:
            if dataframe['channel'] ==1:
                return 'sale'
            else:
                return 'buy'
        else:
            return 'waitting'
    channel_tom = channel.shift(-1)
    sign_num = channel_tom * channel
    temp = pd.DataFrame({'channel_tom':channel_tom,'sign_num':sign_num,'channel':channel})
    sign = temp.apply(generate_sign,axis=1)
    return sign

def boll(series,n):
    '''
    boll线，返回简单N日移动平均和上下布林线
    '''
    boll = MA(series,n)
    std = []
    std.extend([np.nan for _ in range(n-1)])
    for i in range(n-1,len(series)):
        frame = series[i-n+1:i+1]
        std.append(np.std(frame))
    std = pd.Series(std)
    ub = boll + 2*std
    lb = boll - 2*std
    return boll,ub,lb

def HisCost(price,pre_price,turn):
    '''
    基于换手率的成本估算，返回对应的筹码成本
    '''
    hiscost=[]
    for i in range(len(price)):
        if i==0:
            hiscost.append(pre_price[i]*(1-0.01*turn[i])+price[i]*0.01*turn[i])
        else:
            hiscost.append(hiscost[i-1]*(1-0.01*turn[i])+price[i]*0.01*turn[i])
    return pd.Series(hiscost)


def ROC(series,N=6,M=12):
    '''
    ROC与MAROC指标计算，N为滞后天数，默认为6；M为移动平均天数，默认12
    '''
    temp = pd.DataFrame({'ori_series':series,'BX':series.shift(N)})
    temp['AX'] = temp['ori_series'] - temp['BX']
    temp['ROC'] = temp['AX']/temp['BX']
    temp['MAROC'] = MA(temp['ROC'],M)
    
    return temp['ROC'],temp['MAROC']
    
    
def CCI(high,low,close,N=13):
    '''
    计算CCI指标
    '''
    tp = (high+low+close) / 3
    ma = MA(close,N)
    md = MA(ma-close,N)
    cci = (tp-ma) / md / 0.015
    return cci
