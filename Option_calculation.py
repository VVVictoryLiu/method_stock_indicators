# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 10:27:52 2020

@author: ErwinLIU
"""
import numpy as np
from scipy.stats import norm
import math

def BS_option(S, K, T, r, sigma, option='call'):
    """
    S: spot price
    K: strike price
    T: time to maturity
    r: risk-free interest rate
    sigma: standard deviation of price of underlying asset
    """
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K) + (r - 0.5*sigma**2)*T)/(sigma * np.sqrt(T))

    if option == 'call':
        return (S*norm.cdf(d1, 0.0, 1.0) - K*np.exp(-r*T)*norm.cdf(d2, 0.0, 1.0))
    elif option == 'put':
        return (K*np.exp(-r*T)*norm.cdf(-d2, 0.0, 1.0) - S*norm.cdf(-d1, 0.0, 1.0))
    else:
        return 'Error for input'
    
    
def BS_option_withQ(S, K, T,t, r,q, sigma, option='call'):
    """
    
    Calculate Option Price with repo rate
    
    S: spot price
    K: strike price
    T,t: time to maturity
    r: risk-free interest rate
    q: repo rate 
    sigma: standard deviation of price of underlying asset
    """
    T = T-t
    
    d1 = (np.log(S/K) + (r -q + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = (np.log(S/K) + (r -q - 0.5*sigma**2)*T)/(sigma * np.sqrt(T))

    if option == 'call':
        return (S*np.exp(-q*T)*norm.cdf(d1, 0.0, 1.0) - K*np.exp(-r*T)*norm.cdf(d2, 0.0, 1.0))
    elif option == 'put':
        return (K*np.exp(-r*T)*norm.cdf(-d2, 0.0, 1.0) - S*np.exp(-q*T)*norm.cdf(-d1, 0.0, 1.0))
    else:
        return 'Error for input'
    
