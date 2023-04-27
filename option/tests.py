# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:32:34 2023

@author: sametz
"""

import unittest
from BSMOption import BSMOption
import numpy as np

class TestBSMOption(unittest.TestCase):
    """
    Test cases for BSM Option model 
    Excel spreadsheet counpterpart is used as reference for input parameters and expected outputs
    """
    def setUp(self):
        self.S = 19
        self.K = 17
        self.days_to_expiry = 168
        self.riskfree_rate = 0.005
        self.vol = 0.3
    
    def test_classObject(self):
        optmodel = BSMOption(self.S, self.K, self.days_to_expiry, self.riskfree_rate, self.vol)
        self.assertIsInstance(optmodel, BSMOption)
        
    def test_init_parameters(self):
        optmodel = BSMOption(self.S, self.K, self.days_to_expiry, self.riskfree_rate, self.vol)
        self.assertEqual(optmodel.K, self.K)
        self.assertEqual(optmodel.vol, self.vol)
        self.assertEqual(optmodel.r,self.riskfree_rate)
        self.assertEqual(optmodel.S, self.S)
        
    def test_modify_parameters(self):
        optmodel = BSMOption(self.S, self.K, self.days_to_expiry, self.riskfree_rate, self.vol)
        optmodel.K = 20
        optmodel.vol = 0.5
        self.assertEqual(optmodel.K, 20)
        self.assertEqual(optmodel.vol, 0.5)
        
    def test_invalid_price(self):
        optmodel = BSMOption(19, 0, self.days_to_expiry, self.riskfree_rate, self.vol)
        with self.assertRaises(ValueError):
            optmodel.calculate_call_price()
            
        optmodel = BSMOption(0, 19, self.days_to_expiry, self.riskfree_rate, self.vol)
        with self.assertRaises(ValueError):
            optmodel.calculate_call_price()
        
        optmodel = BSMOption(19, 0, self.days_to_expiry, self.riskfree_rate, self.vol)
        with self.assertRaises(ValueError):
            optmodel.calculate_put_price()
            
        optmodel = BSMOption(0, 19, self.days_to_expiry, self.riskfree_rate, self.vol)
        with self.assertRaises(ValueError):
            optmodel.calculate_put_price()
            
    def test_invalid_maturity(self):
        optmodel = BSMOption(19, 19, 0, self.riskfree_rate, self.vol)
        with self.assertRaises(ValueError):
            optmodel.calculate_call_price()
        with self.assertRaises(ValueError):
            optmodel.calculate_put_price()
         
    def test_ITM_callprice(self):
        #Excel spreadsheet reference is used for input parameters and expected price
        optmodel = BSMOption(19, 17, self.days_to_expiry, self.riskfree_rate, self.vol)
        expected_price = 2.70
        price = np.round(optmodel.calculate_call_price(),2)
        self.assertAlmostEqual(expected_price, price)
        
    def test_ITM_putprice(self):
        #Excel spreadsheet reference is used for input parameters and expected price
        optmodel = BSMOption(19, 20, self.days_to_expiry, self.riskfree_rate, self.vol)
        expected_price = 2.10
        price = np.round(optmodel.calculate_put_price(),2)
        self.assertAlmostEqual(expected_price, price)
        
    def test_ATM_callprice(self):
        #Excel spreadsheet reference is used for input parameters and expected price
        optmodel = BSMOption(19, 19,self.days_to_expiry, self.riskfree_rate, self.vol)
        expected_price = 1.56
        price = np.round(optmodel.calculate_call_price(),2)
        self.assertAlmostEqual(expected_price, price)
        
    def test_ATM_putprice(self):
        #Excel spreadsheet reference is used for input parameters and expected price
        optmodel = BSMOption(19, 19, self.days_to_expiry, self.riskfree_rate, self.vol)
        expected_price = 1.52
        price = np.round(optmodel.calculate_put_price(),2)
        self.assertAlmostEqual(expected_price, price)
        
    def test_OTM_callprice(self):
        #Excel spreadsheet reference is used for input parameters and expected price
        optmodel = BSMOption(19, 20, self.days_to_expiry, self.riskfree_rate, self.vol)
        expected_price = 1.15
        price = np.round(optmodel.calculate_call_price(),2)
        self.assertAlmostEqual(expected_price, price)
        
    def test_OTM_putprice(self):
        #Excel spreadsheet reference is used for input parameters and expected price
        optmodel = BSMOption(19, 17, self.days_to_expiry, self.riskfree_rate, self.vol)
        expected_price = 0.66
        price = np.round(optmodel.calculate_put_price(),2)
        self.assertAlmostEqual(expected_price, price)
        
    def test_callput_parity(self):
        """
        C+PV(x)=P+S
        The relationship between call and put prices are as above so they need to be equal when strike = forward price
        """
        fwd_price = np.exp(0.005*168/365)*19
        optmodel = BSMOption(19, fwd_price, 168, self.riskfree_rate, self.vol)
        
        call = optmodel.calculate_call_price()
        put = optmodel.calculate_put_price()
        self.assertAlmostEqual(call, put)

    def test_maturityimpactITM(self):
        #The price of the ITM call option should be monotone increasing as days to expiry increases
        maturities = [168,175,182,189]
        for i in range(len(maturities)-1):
           optmodel1 = BSMOption(19, 17, maturities[i], self.riskfree_rate, self.vol)
           optmodel2 = BSMOption(19, 17, maturities[i+1], self.riskfree_rate, self.vol)
           price1 = optmodel1.calculate_call_price()
           price2 = optmodel2.calculate_call_price()
           self.assertGreater(price2, price1)
           
    def test_maturityimpactOTM(self):
        #The price of the OTM call option should be monotone increasing as days to expiry increases
        maturities = [168,175,182,189]
        for i in range(len(maturities)-1):
           optmodel1 = BSMOption(19, 22, maturities[i], self.riskfree_rate, self.vol)
           optmodel2 = BSMOption(19, 22, maturities[i+1], self.riskfree_rate, self.vol)
           price1 = optmodel1.calculate_call_price()
           price2 = optmodel2.calculate_call_price()
           self.assertGreater(price2, price1)
           
    def test_volatilityimpact(self):
        #The price of any option should be monotone increasing as volatility increases regardless of the side of the contract
        vols = [0.2,0.3,0.4]
        for i in range(len(vols)-1):
           optmodel1 = BSMOption(19, 17, self.days_to_expiry, self.riskfree_rate, vols[i])
           optmodel2 = BSMOption(19, 17, self.days_to_expiry, self.riskfree_rate, vols[i+1])
           price1 = optmodel1.calculate_call_price()
           price2 = optmodel2.calculate_call_price()
           self.assertGreater(price2, price1)
           price1 = optmodel1.calculate_put_price()
           price2 = optmodel2.calculate_put_price()
           self.assertGreater(price2, price1)
                      
    def test_positiveCallDelta(self):
        #Call options should have positive delta regardless of the moneyness
        for strike in [15,19,20]:
            optmodel = BSMOption(19, strike, self.days_to_expiry, self.riskfree_rate, self.vol)
            delta = optmodel.calculate_call_delta()
            self.assertGreater(delta, 0)
            
    def test_negativePutDelta(self):
        #Put options should have negative delta regardless of the moneyness
        for strike in [15,19,20]:
            optmodel = BSMOption(19, strike, self.days_to_expiry, self.riskfree_rate, self.vol)
            delta = optmodel.calculate_put_delta()
            self.assertLess(delta, 0)
            
    def test_callDelta_deepITM(self):
        #deep ITM option should have delta of 1
            optmodel = BSMOption(20, 1, self.days_to_expiry, self.riskfree_rate, self.vol)
            delta = optmodel.calculate_call_delta()
            self.assertAlmostEqual(delta, 1)
        
    def test_callDelta_deepOTM(self):
        #deep OTM option should have delta of 0
            optmodel = BSMOption(1, 20, self.days_to_expiry, self.riskfree_rate, self.vol)
            delta = optmodel.calculate_call_delta()
            self.assertAlmostEqual(delta, 0)
            
    def test_zero_riskfreerate(self):
        #ATM call and put prices should be equal if RF rate is zero 
        optmodel = BSMOption(19, 19, 30, 0, 0.3)
        
        call = optmodel.calculate_call_price()
        put = optmodel.calculate_put_price()
        self.assertAlmostEqual(call, put)

            
if __name__ == '__main__':
    unittest.main()