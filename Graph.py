'''
Created on Mar 6, 2020

@author: Thoma
'''




class Graph():
    def _init_(self, graphDict = None):
        if graphDict == None:
            graphDict = {}
        self.dict = graphDict
    
    
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
        
    def add_edge(self, v, w):  #use v as the from node and w as the to node
        if v in self.dict:
            self.dict[v].append(w)
        else:
            self.dict[w].append(v)
          
    def setTime(self,v,w,time):
        self.dict[v][w].append(time)
        
    def getTime(self,v,w):
        return self.dict[v][w]
      
    def addLine(self,v,w,tupxY): #used to store the curve of the line 
        self.dict[v][w].append(tupxY)
        #self.dict[w][v].append(tupxY)
        
    def getLine(self,v,w):
        return self.dict[v][w]
    
    def del_edge(self, v, w):
        self.dict[v][w] = None
        self.[w][v] = None
        
    def __str__(self):
        vert = 'vertices: '
        for i in self.dict:
            vert += str(i) + ' '
        vert += '\nedges'
        for j in self.genEdges():
            vert += str(j) + ' '
        return vert

    #world give the truck locations
    

