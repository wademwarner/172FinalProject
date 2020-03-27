'''

Created on Mar 19, 2020



@author: Wade

'''



'''

Created on Mar 6, 2020

@author: Thoma

'''


import numpy







class Graph(object):

    def __init__(self):

        self.dict = {} #To store the graphs nodes tht are connect with one and another

        self.distance = {} #to store the distance between nodes

        self.edge = {} #store the curvature of the edge 
        
        self.line = {} #store the curvature of each line

        '''

        if graphDict == None:

            graphDict = {}

        self.dict = graphDict

        '''

    

    

    def get_node_list(self): #return the vertices

        return list(self.dict.keys())

        

    def get_edge_list(self): #return a list of the nodes

        return self.genEdges()

    

    def genEdges(self):

        edge = []

        for vert in self.dict:

            for neib in self.dict[vert]:

                edge.append({vert,neib})

        return edge

    

    def add_node(self, v):

        if v not in self.dict:

            self.dict[v] = []

    def del_node(self, v):

        self.dict[v] = None

        

    def add_edge(self, v, w, time, lineCurve):  #use v as the from node and w as the to node then add the time between them as well

        #time = 1 #used only for the first part of the project

        if v not in self.dict:

            self.dict[v] = []

        if w not in self.dict:

            self.dict[w] = []   

        if (v,w) not in self.distance:

            self.dict[v].append(w)

            #self.dict[w].append(v)         Removed to make this to make the path test element easier 

            self.distance[(v,w)] = time


    def getAllNeighbors(self):
        return self.dict.keys()    
 

    
    def getAllTime(self):
        return self.distance.values()

    
    def getNeighbor(self,v):



        if v not in self.dict:



            return None



        else:



            return self.dict[v]



    



    def getNeighborSize(self,v):



        if v not in self.dict:



            return None



        else:



            return len(self.dict[v])



    def getLine(self,v,w):

        try:

            return self.line[(v,w)]

        except KeyError:

            return 152

    

    def isLinStraight(self,v,w):

        if len(self.line[(v,w)]) == 2:

            return True

        else:

            return False



    def getTime(self,v,w):



        return self.distance[(v,w)]



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



        self.dict[v][w] = None



        self.dict[w][v] = None



        if v < w:



            



            self.distance[(v,w)] = None



        else:



            self.distance[(w,v)] = None



        



        



    def __str__(self):



        vert = 'vertices: '



        for i in self.dict:



            vert += str(i) + ' '



        vert += '\nedges'



        for j in self.genEdges():



            vert += str(j) + ' '



        return vert

    def find_path(self):
        smallestNode = 'A'

        C = np.max([i for i in g.getAllTime()])
        n = len(g.getAllNeighbors())
        
        startNode = 'A'
        
        endNode = 'H'
        path = {}
        
        bucket = [ [] for j in range(C*n + 1)]
        
        for t in g.getAllNeighbors():
            if t == startNode:
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
            
            for u in g.getNeighbor(smallestNode):
                
                if u not in permanentNode:
                    newDist = path[smallestNode] + g.getTime(smallestNode, u)
                    
                    if newDist < path[u]:
                        bucket[ path[u] ].remove(u)
                        path[u] = newDist
                        before[u] = smallestNode
                        bucket[ path[u] ].append(u)
                        
                        
        print(path)
        
        print(before)   #want to return path and before, path
        
        #find the shortest path 
        
        done = True
        shortestPath = {}
        shortestPath[endNode] = [before[endNode],path[endNode]]
        endNode = before[endNode]
        while done:
            if path[endNode] == 0:
                done = False
                shortestPath[endNode] = [endNode,0]
            else:
                shortestPath[endNode] = [before[endNode],path[endNode]]
                endNode = before[endNode]
            
         
        print(shortestPath)





    #world give the truck locations

