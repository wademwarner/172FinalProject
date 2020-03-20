from Classes.World import World
from Classes.Graph import Graph
from Classes.visGraph import visGraph
from networkx.classes import graph

graphObj = Graph()
myWorld = World()

'''
for i in range(len(myWorld.Edges)):
    graphObj.add_node(myWorld.Edges[i][0]) #add vertices
'''

for j in range(len(myWorld.Edges)):   
    graphObj.add_edge(myWorld.Edges[j][0], myWorld.Edges[j][1],1) #graphObj.add_edge(myWorld.Edges[i][0], myWorld.Edges[i][1],myWorld.Edges[i][2]) for when we want to add actual time

vtx = myWorld.Verticies

myWorld.changeToViz(vtx)

for k in range(len(myWorld.Edges)):
        #print(k, graphObj.getNeighbor(k))
        myWorld.drawGraph(k,graphObj.getNeighbor(k))
        
myWorld.appearances()

myWorld.runSimulation(10)




