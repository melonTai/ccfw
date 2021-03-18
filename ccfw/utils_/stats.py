# -*- coding: utf-8 -*-
# author:melonTai
# description:util stats
import numpy as np
from decimal import getcontext, Decimal

def round_down(x):
    x = Decimal(x)
    return float(x)

def standarize(ndarray):
    return (ndarray - ndarray.mean())/ndarray.std(ddof = 0)

def calc_interval_mean(cut_off_down, cut_off_up, pdsx, pdsy):
    return [pdsy[(i <= pdsx) & (pdsx < i+1)].mean() for i in range(cut_off_down, cut_off_up)]

def plot_interval_mean(ax, cut_off_down, cut_off_up, pdsx, pdsy, color = 'orange'):
    y_mean_list = calc_interval_mean(cut_off_down, cut_off_up, pdsx, pdsy)
    for i in range(cut_off_down, cut_off_up):
        x_list = [i, i+1]
        y_mean = y_mean_list[i + cut_off_down]
        ax.plot(x_list, [y_mean]*len(x_list), color = color)

def mylog10(ndarray):
    min_data,*_ = ndarray.min()
    offset = -min_data*2 if min_data < 0 else 0
    return np.log10(ndarray + offset)
