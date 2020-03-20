from Classes.World import World

from Classes.Graph import Graph

from networkx.classes import graph



graphObj = Graph()

myWorld = World()



'''

for i in range(len(myWorld.Edges)):

    graphObj.add_node(myWorld.Edges[i][0]) #add vertices

'''



for j in range(len(myWorld.Edges)):   

    graphObj.add_edge(myWorld.Edges[j][0], myWorld.Edges[j][1],myWorld.Edges[j][2], myWorld.Edges[j][3]) #graphObj.add_edge(myWorld.Edges[i][0], myWorld.Edges[i][1],myWorld.Edges[i][2]) for when we want to add actual time
    #need to change the graphing method so that if there is a list of size 2 then stright line
    #else, if list is not 2 then keep iterating a new stright line to represent curvature

print(myWorld.Edges)

print('work?')
print(graphObj.getLine(136, 141))
print(graphObj.isLinStraight(136, 141))
vtx = myWorld.Verticies



myWorld.changeToViz(vtx)



for k in range(len(myWorld.Edges)):

        #print(k, graphObj.getNeighbor(k))

        myWorld.drawGraph(k,graphObj.getNeighbor(k))

        

myWorld.appearances()



myWorld.runSimulation(10)




