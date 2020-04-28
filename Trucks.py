'''
Created on Apr 22, 2020

@author: Thoma
'''

class Trucks(object):
    def __init__(self,id,startNode,capacity,pos):
        x = float(pos[0])
        y=float(pos[1])
        self.truck = {'Path':[startNode,0,[x,y]],'Time':[0,0],'Order':[id,'null'],'Use':[False,capacity]}
        
        '''
        {'Path':[currentNode,EndNode,location(x,y)],'Time':[TimeonPath,TimeLeftOnPath],'Order':[Truck ID,OrderNmber],'Use':[T/F if truck is in use,capacity]}
        currentNode = startNode
        truckID = id
        capacity = capacity
        [x,y] = pos
        '''
        
    def getPosition(self): 
        return self.truck['Path'][0]
    
    def setNewPosition(self,pos):
        self.truck['Path'][0] = pos
        
    def getEndPosition(self):    
        return self.truck['Path'][1]
    
    def setEndPosition(self,pos):    
        self.truck['Path'][1] = pos
        
    def getPosition_x_Coordinates(self):
        return self.truck['Path'][2][0]
    
    def getPosition_y_Coordinates(self):
        return self.truck['Path'][2][1]
    
    def setPosition_x_Coordinates(self,x):
        self.truck['Path'][2][0] = x
    
    def setPosition_y_Coordinates(self, y):
        self.truck['Path'][2][1] = y
        
    def isTruckInUse(self):
        return self.truck['Use'][0]
    
    def setTruckUsage(self,us):
        self.truck['Use'][0] = us

    
    def getTimeLeftOnPath(self):
        return self.truck['Time'][1]
    
    def setNewTimeLeft(self):
        self.truck['Time'][1] += 1 #took out float(1)
        
    def setTimeOfaNewPath(self,tim):
        self.truck['Time'][0] = float(tim)
        self.truck['Time'][1] = 1
        
    def getTimeOfAPath(self):
        return self.truck['Time'][0]
        
    def setNewOrderForTruck(self,num):
        self.truck['Order'][1] = num
        self.setTruckUsage(True)
        
    def getTruckCapacity(self):
        return self.truck['Use'][1]
    
    def getTruckID(self):
        return self.truck['Order'][0]
        