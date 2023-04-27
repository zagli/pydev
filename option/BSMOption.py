# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 13:31:59 2023

@author: sametz
"""

import numpy as np
import datetime as dt
from scipy.stats import norm 

class BSMOption():
    """ 
    This class implements Black&Scholes model for vanilla option pricing
    
    Assumptions of the model: 
    - Option is European and hence can only be exercised at maturity date.
    - Underlying stock does not pay divident during option's lifetime.  
    - The risk-free rate and volatility of the underlying asset are known and constant. 
    - The returns of the underlying asset are normally distributed.
    - Markets are random and hence cannot be predicted
    """

    def __init__(self, spot_price:float, strike_price:float, days_to_maturity:int, rf_rate:float, sigma:float):
        """
        spot_price: current stock or other underlying spot price
        strike_price: strike price of the contract
        days_to_maturity: number of days until the expiration
        risk_free_rate: current risk free rate  
        sigma: annualized standard deviation of asset's log returns
        """
        
        self.S = spot_price
        self.K = strike_price
        self.r = rf_rate
        self.vol = sigma
        self.time_to_expiry = days_to_maturity/365
        
    def _calcd1(self):
        return (np.log(self.S / self.K) + (self.r + self.vol**2 / 2.0) * self.time_to_expiry) / (self.vol * np.sqrt(self.time_to_expiry))

    def _calcd2(self):
        return self._calcd1()- self.vol * np.sqrt(self.time_to_expiry)
        
    def calculate_call_price(self):
        #calculates call price of a vanilla european option contract
        if self.S <= 0:
            raise ValueError("Spot price must be positive")
        if self.K <= 0:
            raise ValueError("Strike must be positive")
        if self.time_to_expiry <= 0:
            raise ValueError("Days to maturity arg must be positive")
        d1 = (np.log(self.S/self.K) + (self.r + (self.vol ** 2) / 2.0)*self.time_to_expiry)/(self.vol*np.sqrt(self.time_to_expiry))
        d2 = d1 - self.vol*np.sqrt(self.time_to_expiry)
        d1 = self._calcd1()
        d2 = self._calcd2()
        return self.S*norm.cdf(d1) - self.K*np.exp(-self.r*self.time_to_expiry)*norm.cdf(d2)

    def calculate_put_price(self):
        #calculates put price of a vanilla european option contract
        if self.S <= 0:
            raise ValueError("Spot price must be positive")
        if self.K <= 0:
            raise ValueError("Strike must be positive")
        if self.time_to_expiry <= 0:
            raise ValueError("Days to maturity arg must be positive")
        d1 = (np.log(self.S/self.K) + (self.r + (self.vol ** 2) / 2.0)*self.time_to_expiry)/(self.vol*np.sqrt(self.time_to_expiry))
        d2 = d1 - self.vol*np.sqrt(self.time_to_expiry)
        d1 = self._calcd1()
        d2 = self._calcd2()
        return self.K*np.exp(-self.r*self.time_to_expiry)*norm.cdf(-d2) - self.S*norm.cdf(-d1)
    
    def calculate_call_delta(self):
        #calculates call delta of a vanilla european option contract
        return norm.cdf(self._calcd1())
    
    def calculate_put_delta(self):
        return -norm.cdf(-self._calcd1()) 
    

def main():
    # Gather the inputs from the user
    spot_price = float(input("Spot price: ").replace("$",""))
    strike_price = float(input("Strike: ").replace("$",""))
    rf_rate = float(input("Risk-free rate as percentage:").replace("%","")) / float('100')
    vol = float(input("Vol: ").replace("%","")) / float('100')
    time_to_expiry = int(input("Time to expiration (in days): "))

    optmodel = BSMOption(spot_price, strike_price, time_to_expiry, rf_rate ,vol)
    # Calculate the value of a call and put option based on the inputs
    call_price = optmodel.calculate_call_price()
    put_price = optmodel.calculate_put_price()
    
    print("Call Price:{0}".format(call_price))
    print("Put Price:{0}".format(put_price))


if __name__ == "__main__":
    main()


