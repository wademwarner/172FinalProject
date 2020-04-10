'''

Created on Mar 19, 2020



@author: Wade

'''



'''

Created on Mar 6, 2020

@author: Thoma

'''


import numpy as np 







class Graph(object):

    def __init__(self):

        self.dict = {} #To store the graphs nodes that are connect with one and another

        self.distance = {} #to store the distance between nodes, i this case it is used as time

        self.edge = {} #store the tiem it take to travel on each edge 
        
        self.line = {} #store the curvature of each line


    def get_node_list(self): #return the vertices

        return list(self.dict.keys())

    def get_edge_list(self): #return a list of the nodes

        return self.genEdges()

    def genEdges(self): # a method to return all the edges as a list 

        edge = []

        for vert in self.dict:

            for neib in self.dict[vert]:

                edge.append({vert,neib})

        return edge

    def add_node(self, v):   #method to add a new node (vertex) to the graph

        if v not in self.dict:

            self.dict[v] = []

    def del_node(self, v):  #Delete a node (certex)

        self.dict[v] = None

        

    def add_edge(self, v, w, time, lineCurve,neighbors):  #use v as the from node and w as the to node then add the time between them as well

        #time = 1 #used only for the first part of the project
        
        '''
        NEED TO CHANGE THIS TO WORK FOR THE SECOND PART OF THE PROJECT ITSELF 
        '''
        if v not in self.dict:

            self.dict[v] = []

        if w not in self.dict:

            self.dict[w] = []   

        if neighbors == 'B':
            self.dict[v].append(w)

            self.dict[w].append(v)         #Removed to make this to make the path test element easier 

            self.distance[(v,w)] = time #assign a time to each edge 
            self.distance[(w,v)] = time
            
            if (v,w) not in self.line.keys():
                self.line[(v,w)] = lineCurve #assigns the curvature of the line to an edge
                
            if (w,v) not in self.line.keys():   
                self.line[(w,v)] = np.flip(lineCurve,0)
                
                
        elif neighbors == 'OneWayA':
            self.dict[v].append(w)

            #self.dict[w].append(v)         #Removed to make sure the path finding algorithm still works

            self.distance[(v,w)] = time #assign a time to each edge 
            if (v,w) not in self.line.keys():
                self.line[(v,w)] = lineCurve #assigns the curvature of the line to an edge
                
        else:
            #self.dict[v].append(w)        #Removed to make sure the path finding algorithm still works

            self.dict[w].append(v)         

            self.distance[(w,v)] = time     #assign a time to each edge 
            
            if (w,v) not in self.line.keys():           #assigns the curvature of the line to an edge
                self.line[(w,v)] = np.flip(lineCurve,0)
            
            
        '''
        For part two 
        the if statement above needs to be changed to accomidate different road paths, this will dictate the  self.distance[(v,w)] = time as is above or just one or the other
        Also change for the lineCurve part
        '''

    def getAllNeighbors(self):    #returns all the neihbors for all the nodes
        return self.dict.keys()    
 

    
    def getAllTime(self):
        return self.distance.values() #returns all the times of the edges

    
    def getNeighbor(self,v): #reuturns the neighbors of node v and returns None if a node doesnt exisit

        if v not in self.dict.keys():

            return None

        else:
            return self.dict[v]


    def getNeighborSize(self,v):

        if v not in self.dict:          #returns none if node v isnt in the graph

            return None

        else:

            return len(self.dict[v])   #reuturns an integer of the number of neighbors node v has


    def getLine(self,v,w):
        
        if (v,w) not in self.line.keys():    #return None is an edge doesnt exisit
            return 6
        
        else:
            return self.line[(v,w)]        #return the curvature of an edge

        '''
        try:

            return self.line[(v,w)]

        except KeyError:

            return 152
            code wade did that i am not sure if it is right 
        '''
    

    def isLinStraight(self,v,w):  #asking if the line is straight

        if len(self.line[(v,w)]) == 2:

            return True                    #return True if the line is straight

        else:

            return False                   #return False if the line is curved



    def getTime(self,v,w):                  #return the time to travel along an edge

        if (v,w) not in self.distance.keys():
            return None                     #return None is the edge doesnt exisit
        else:
            return self.distance[(v,w)]     #return the time to travel on an edge if it exisits



    '''

    likely will add this to the add_edge class then adjust it in the future for the getLine function 

    def addLine(self,v,w,tupxY): #used to store the curve of the line 

        self.dict[v][(v,w)].append(tupxY)

        #self.dict[w][v].append(tupxY)

        

    def getLine(self,v,w):

        return self.dict[v][(v,w)][1]

        work off tackc code more

    '''



    def del_edge(self, v, w):
        '''
        THIS NEEDS TO EITHER BE TAKEN OUT OR CHANGES WHEN WE ADD DIRECTION TO THIS JOHN
        '''

        self.dict[v][w] = None

        self.dict[w][v] = None

        if v < w:

            self.distance[(v,w)] = None

        else:

            self.distance[(w,v)] = None




    def __str__(self):     #Prints all the edges and vertices in the graph


        vert = 'vertices: '

        for i in self.dict:

            vert += str(i) + ' '

        vert += '\nedges'

        for j in self.genEdges():

            vert += str(j) + ' '

        return vert

    def find_path(self, start, end):   #a path finding algorithm                       
        '''
        LIKELY CHANGE THIS SHIT UP TO MAKE IT A LOT MORE EFFICIENT 
        ALSO COMMENT OUT AFTER THE CHANGES ARE MADE TO IT. NEED TO FINISH PART 1 BEFORE THIS CAN HAPPEN
        TRY TO GET THIS TO BE LESS THAN 30 LINES OF CODE TOTAL
        '''
        print(start)
        print(end)
        #g = self   replace self with g if explosion occurs
        smallestNode = start

        C = np.max([i for i in self.getAllTime()])
        n = len(self.getAllNeighbors())
        
        
        path = {}
        
        bucket = [ [] for j in range(C*n + 1)]
        
        for t in self.getAllNeighbors():
            if t == start:
                path[t] = 0
            else:
                path[t] = n*C 
                
            bucket[ path[t] ].append(t)

        permanentNode = {}
        
        before = {}
        
        bucketIndex = 0
        while len(permanentNode) < n:
            
            if len(bucket[bucketIndex]) > 0:
                smallestNode = bucket[bucketIndex].pop()
                
            else:
                bucketIndex += 1
                continue
            
            permanentNode[smallestNode] = True
            
            for u in self.getNeighbor(smallestNode):                               #a for loop to find the shortest path and retirh in as path
                
                if u not in permanentNode:
                    newDist = path[smallestNode] + self.getTime(smallestNode, u)
                    
                    if newDist < path[u]:
                        bucket[ path[u] ].remove(u)
                        path[u] = newDist
                        before[u] = smallestNode
                        bucket[ path[u] ].append(u)
                        
                        
        #print(path)     #MAY not need to print this
        
        #print(before)   #want to return path and before, path    Also do we need to print????
        
        #find the shortest path 
        '''
        This returning a dictonary of wehre the key is the first Node and all other nodes other than the end node
        then the next node it suppose to go to along with the cummulative distance
        '''
        
        done = True
        shortestPath = {}
        shortestPath[before[end]] = [end,path[end]]
        if start == before[end]:
            pass
        else:
            end = before[end] 
            while done:
            
                before[end]
                shortestPath[before[end]] = [end,path[end]]
                if before[end] == start:
                    done = False
                else:
                    end = before[end]
                
         
        return shortestPath                         #An ordered shortest path is returned here 



