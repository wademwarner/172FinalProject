'''
Created on Mar 6, 2020

@author: Thoma
'''




class Graph(object):
    def __init__(self):
        self.dict = {} #To store the graphs nodes tht are connect with one and another
        self.distance = {} #to store the distance between nodes
        self.edge = {} #store the curvature of the edge 
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
        
    def add_edge(self, v, w, time):  #use v as the from node and w as the to node then add the time between them as well
        time = 1 #used only for the first part of the project
        if v not in self.dict:
            self.dict[v] = []
        if w not in self.dict:
            self.dict[w] = []   
        if v > w:
            v, w = w, v
        if (v,w) not in self.distance:
            self.dict[v].append(w)
            self.dict[w].append(v)
            self.distance[(v,w)] = time
        
    def getNeighbor(self,v):
        if v not in self.dict:
            return None
        else:
            return self.dict[v]
    
    
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

    #world give the truck locations
    

