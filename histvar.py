# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:10:51 2023

@author: sametz
"""
import pandas as pd
import numpy as np 

def create_pnl_vec(file_path, portvals):

    daily_df = pd.read_csv(file_path)
    for j,col in enumerate(list(daily_df)):
        daily_df[col+'shift'] = (np.exp(np.log(daily_df[col] / daily_df[col].shift(-1)))-1).fillna(0)
        daily_df[col+'pnlvec'] = daily_df[col+'shift'] * portvals[j]
        
    tot_pnl_vec = daily_df[[x for x in list(daily_df) if x.endswith('pnlvec')]].sum(axis=1)
    return tot_pnl_vec

def estimate_VAR_1_99(pnl_vec, coef1=0.0, coef2=0.4, coef3=0.6):
    return coef1*pnl_vec.nsmallest(3).iloc[0] + coef2*pnl_vec.nsmallest(3).iloc[1] + coef3*pnl_vec.nsmallest(3).iloc[2]

def main():
    
    portvals = [153084.81, 95891.51]
    input_file_path = 'ccyprices.csv'
    pnlvec = create_pnl_vec(input_file_path, portvals)
    hist_VAR = estimate_VAR_1_99(pnlvec)
    print("1-day historical VAR of the FX portfolio with 99% confidence is estimated as:", hist_VAR)

if __name__ == "__main__":
    main()
