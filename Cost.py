'''
Created on Apr 28, 2020

@author: Wade
'''
import numpy as np

class Cost (object):
    
    def __init__(self):
        self.car_value = 1500000
        self.discount = 100000
        self.trans_cost = 50
        self.weight_mx = 5 #weight multiplier 5 * weight of materials
        self.holding_cost = 5
        self.HC_Order = {}
        self.order_rev = {}
        self.h_cost = 0
        self.t_cost = {}
        self.order_profit = {}
        
        self.totalRev = 0
        self.totalCost = 0

    
    def getETC(self, order, weight): #GET EXPECTED TRANSPORTATION COST, 

        ETC = (self.trans_cost+self.weight_mx*weight)
        self.t_cost[order] += ETC
        
    def getEHC (self,order,weight,lines): #lines has the lines and the current hold rate for each one at time 
        #TOTAL ACCUMULATOR - TOTAL OVER THE ENTIRE SIMULATION
        EHC = 0        
        for line in lines: #WE WANT ALL MATERIALS AT ALL LINES
            
            EHC += lines[line]*5 #lines[LINE]
                                 #SHOULD return a tonnage which the line is holding 
                                 #and multiply by $5 for holding
        
        self.order_cost += EHC
        #this ultimately gives us a total holding cost, not HC/t
        
        
    def getRev (self,order,time): #Gets what we earn per car as made
               
        extra = time - 60
        discount_magnitude = np.ceil(extra/30) * self.discount
        car_af_discount = self.car_value - discount_magnitude
        
        self.order_rev[order] = car_af_discount

    def getTProfit (self):
        totalRev = 0
        totalCost = 0
        for order in self.order_rev:
            totalRev += self.order_rev[order]
        totalCost += self.h_cost
        for order in self.t_cost:
            totalCost += self.t_cost[order]
        totalProfit = totalRev-totalCost
        
        return totalProfit
        
    def printProfit (self):
        
        PRev = "Total revenues for the day = $" + self.totalRev
        PCost = "Total costs for the day = $" + self.totalCost
        PProfit = "Total profit for the day = $" + self.getTProfit()
        
        print PRev
        print PCost
        print PProfit
        
        
        
        
                