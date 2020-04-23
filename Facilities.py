'''
Created on Apr 22, 2020

@author: Wade
'''
from __builtin__ import False

class Facilities (object):
    
    def __init__ (self):
        self.warehouses = {}
        self.lines = {}
        
        '''warehouse vertices'''
        self.A = []
        self.B = []
        self.C = []
        self.D = []
        self.E = []
        self.F = []
        self.G = []
        self.H = []
        
        '''line vertices'''
        self.L1 = []
        self.L2 = []
        self.L3 = []
        self.L4 = []
    
    def defineWarehouses (self, Warehouses): #define warehouses and formats them into "bin"-like dictionaries that can be found easily
        print(Warehouses)
        for wh in Warehouses:
            wh = str(wh)
            wh_build = wh[10]
            #print(line_build)
            '''creates dictionary of lists of warehouse vertices for each warehouse type (which is the key)'''
            if (wh_build) == "A":
                self.A.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.A 
            elif (wh_build) == "B":
                self.B.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.B 
            elif (wh_build) == "C":
                self.C.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.C       
            elif (wh_build) == "D":
                self.D.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.D  
            elif (wh_build) == "E":
                self.E.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.E      
            elif (wh_build) == "F":
                self.F.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.F       
            elif (wh_build) == "G":
                self.G.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.G            
            elif (wh_build) == "H":
                self.H.append(self.getNumber(wh,True))
                self.warehouses[wh_build] = self.H        
        print(self.warehouses)            

    def defineLines (self, Lines): #define warehouses and formats them into "bin"-like dictionaries that can be found easily
        #print(Lines)
        for line in Lines:
            line = str(line)
            line_build = line[10]+line[11]
            #print(line_build)

            #creates dictionary of lists of line vertices for each line type (which is the key)

            if (line_build) == "L1":
                self.L1.append(self.getNumber(line,False))
                self.lines[line_build] = self.L1 #[27]
            elif (line_build) == "L2":
                self.L2.append(self.getNumber(line,False))
                self.lines[line_build] = self.L2 #[27]
            elif (line_build) == "L3":
                self.L3.append(self.getNumber(line, False))
                self.lines[line_build] = self.L3 #[27]         
            elif (line_build) == "L4":
                self.L4.append(self.getNumber(line, False))
                self.lines[line_build] = self.L4 #[27]
        print(self.lines)
                
    def getNumber (self, test_num, is_wh): #for varying 2/3 index numbers, figures if a number is 1,2,3 digits and cuts off based on comma placement
        if is_wh == False:    
            i = 27
            num = ""
            while test_num[i] != ",":
                num += test_num[i]
                i += 1
        else:
            i = 26
            num = ""
            while test_num[i] != "}":
                num += test_num[i]
                i += 1
                
        return int(num)
                
                   
            
            