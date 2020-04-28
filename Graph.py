'''
Created on Apr 22, 2020

@author: Thoma
'''

import numpy as np 







class Graph(object):

    def __init__(self):

        self.dict = {} #To store the graphs nodes that are connect with one and another

        self.distance = {} #to store the distance between nodes, i this case it is used as time

        self.edge = {} #store the tiem it take to travel on each edge 
        
        self.line = {} #store the curvature of each line
        
        self.nextMatrix = {}  #store the shortest distance between points
        
        self.floydMatrix = {} #store the shortest ditance between points


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


    def getAllNeighbors(self):    #returns all the neighbors for all the nodes
        return self.dict.keys()    

    
    def getAllTime(self):
        dist = []
        for i in self.distance.keys():
            dist.append(self.distance[i])
        return dist #returns all the times of the edges

    
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
            return None
        
        else:
            return self.line[(v,w)]        #return the curvature of an edge



    def isLineStraight(self,v,w):  #asking if the line is straight

        return len(self.line[(v,w)]) == 2
                  #return False if the line is curved, True if line isnt curved
                  
    def getLineLength(self,v,w):
        if (v,w) not in self.line.keys():    #return None is an edge doesnt exisit
            return None
        
        else:
            return len(self.line[(v,w)])      #return the curvature of an edge




    def getTime(self,v,w):                  #return the time to travel along an edge

        if (v,w) not in self.distance.keys():
            return None                     #return None is the edge doesnt exisit
        else:
            return self.distance[(v,w)]     #return the time to travel on an edge if it exisits






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


                       #An ordered shortest path is returned here 


    def getFloydShortest(self,i,j): #returns the shortest ditance between two nodes
        return self.floydMatrix[i,j]
    
    def getNextNode(self,i,j):  #returns the next node to be used in the world class for finding a path
        return self.nextMatrix[i,j]
    
    def setFloyd(self): #a method to set run the floyd welch algorithm to find the shortesrt distance between points
        n = len(self.getAllNeighbors())
        self.floydMatrix = np.ones([n,n])*np.inf
        
        map = {}
        
        V = sorted(self.getAllNeighbors())
        
        for i,v in enumerate(V):
            map[v] = i
            
        print(map) #delete this later after implemented
        
        self.nextMatrix = {}
        
        for i in V:
            for j in V:
                self.nextMatrix[i,j] = '?'
        
        for e in self.getAllNeighbors():
            for t in self.getNeighbor(e):
                self.floydMatrix [map[e],map[t]] = self.getTime(e, t)  #Adjustment to make this work for the graph class
                self.nextMatrix[e,t] = t
        
        
        for k in V:
            for i in V:
                for j in V:
                    if self.floydMatrix [map[i],map[k]] + self.floydMatrix [map[k],map[j]] < self.floydMatrix [map[i],map[j]]:
                        self.floydMatrix [map[i],map[j]] = self.floydMatrix [map[i],map[k]] + self.floydMatrix [map[k],map[j]]
                        self.nextMatrix[i,j] = self.nextMatrix[i,k]
                        
    def find_pathLength(self, start, end):                        

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
                        
                        
        return path[end]
