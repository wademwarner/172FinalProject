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
        self.order_rev = {}
        self.order_cost = {}
        self.order_profit = {}
    
    def getETC(self, order, time,weight): #GET EXPECTED TRANSPORTATION COST, 
        
        '''pseudocode structure
        
        for all trips in total trip
            
            ETC += (self.trans_cost+self.weight_mx*weight)*time_trip
        self.order_cost{order} = ETC
        return ETC
        
        '''
    def getEHC (self,order,time,weight): #THIS MIGHT NOT BE NECESSARY, BECAUSE IF WE IMPLEMENT A DEVOTED TRUCK FOR THE ENTIRE TRIP, THERE SHOULD BE NO HOLDING COST
        
        '''BUT, pseudocode if neededmodule
        
        for all line stops in tripcolor
            
            if time > time_needed
                EHC = (time - time_needed)*weight*self.holding_cost
        
        self.order_cost{order} += EHC
        return EHC
        
        '''
    def getRev (self,order,time): #Gets what we earn per car as made
        '''pseudocode
        
        pass a complete order through here
        
        extra = time - 60
        discount_magnitude = np.ceil(extra) * self.discount
        car_af_discount = self.car_value - discount_magnitude
        
        self.order_rev{order} = car_af_discount
        return car_af_discount
        
        '''
    def getProfit (self,order):
        
        return self.order_rev{order} - self.order_cost{order}
        
        
        
        
        
                