'''
Created on Mar 26, 2020

@author: Thoma
'''
from Graph import Graph
import numpy as np 

g = Graph()
arr = np.arange(3)
g.add_edge('A','B',2,arr)
g.add_edge('A','C',5,arr)
g.add_edge('A','D',7,arr)
g.add_edge('B','D',9,arr)
g.add_edge('B','E',1,arr)
g.add_edge('C','D',2,arr)
g.add_edge('C','H',7,arr)
g.add_edge('D','E',10,arr)
g.add_edge('D','G',5,arr)
g.add_edge('E','G',4,arr)
g.add_edge('E','F',2,arr)
g.add_edge('F','G',4,arr)
g.add_edge('F','H',6,arr)
g.add_edge('G','H',8,arr)
'''
print(g.getNeighbor('A'))

print(g.getNeighbor('B'))

print(g.getTime('C', 'D'))
'''

#Start the path finding

smallestNode = 'A'

C = np.max([i for i in g.getAllTime()])
n = len(g.getAllNeighbors())

startNode = 'A'

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
                before[u] = newDist
                bucket[ path[u] ].append(u)
                
                
print(path)

print(before)
  

