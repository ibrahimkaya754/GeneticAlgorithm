# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:25:06 2017

@author: SADMcan
"""
import math

def griewank(xx):
    d    = len(xx)
    sum  = 0
    prod = 1
    for ii in range(d):
        xi   = xx[ii]
        sum  = sum + xi**2/4000
        prod = prod * math.cos(xi/math.sqrt(ii+1))
    out = sum - prod + 1
    return out

def egg(xx):
    x1    = xx[0]
    x2    = xx[1]
    term1 = -(x2+47) * math.sin(math.sqrt(math.fabs(x2+x1/2+47)))
    term2 = -x1 * math.sin(math.sqrt(math.fabs(x1-(x2+47))))
    out   = term1 + term2
    return out

def bukin6(x):
    x1 = x[0]
    x2 = x[1]    
    term1 = 100 * math.sqrt((abs(x2-0.01*x1**2)))
    term2 = 0.01 * abs(x1+10)    
    out = term1 + term2
    return out

def drop(xx):
    x1 = xx[0]
    x2 = xx[1]
    frac1 = 1+math.cos(12*math.sqrt(x1**2 + x2**2))
    frac2 = 0.5*(x1**2 + x2**2) + 2
    out = -frac1/frac2
    return out

def test01(xx):
    x1 = xx[0]
    x2 = xx[1]
    out = x1**2 - 3*x2
    return out

def ackley(xx):
    d    = len(xx)
    c    = math.pi * 2
    b    = 0.20
    a    = 20
    
    sum1 = 0
    sum2 = 0
    
    for ii in range(d):
        xi   = xx[ii]
        sum1 = sum1 + xi**2
        sum2 = sum2 + math.cos(c*xi)
    
    term1 = -a * math.exp(-b*math.sqrt(sum1/d))
    term2 = -math.exp(sum2/d)
    
    y = term1 + term2 + a + math.exp(1)
    
    return y