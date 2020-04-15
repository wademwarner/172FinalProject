from Classes.World import World


from Classes.Graph import Graph

from networkx.classes import graph



graphObj = Graph()

myWorld = World(graphObj)



for j in range(len(myWorld.Edges)):   

    graphObj.add_edge(myWorld.Edges[j][0], myWorld.Edges[j][1],myWorld.Edges[j][2], myWorld.Edges[j][3],myWorld.Edges[j][4]) #graphObj.add_edge(myWorld.Edges[i][0], myWorld.Edges[i][1],myWorld.Edges[i][2]) for when we want to add actual time
    #if myWorld.Edges[j][2] > 2:
     #   print(myWorld.Edges[j][2])
      #  print(myWorld.Edges[j][3])
#set the floyd welch matrix up
graphObj.setFloyd()
print('floyd Finish')

#print(myWorld.Edges)

#print('work?')

#print(graphObj.getLine(7, 149))

#print(graphObj.isLinStraight(136, 141))

'''

trying to see if there is a realtionship between time and length of an
'''

print(graphObj.getNeighbor(101))

vtx = myWorld.Verticies

myWorld.changeToViz(vtx)    #draws the vertex's

print('locatin of trucks')
trucks = myWorld.getInitialTruckLocations() 

print(trucks[3])

for k in range(len(myWorld.Edges)):

        
        myWorld.drawGraph(k,graphObj.getNeighbor(k))

#myWorld.appearances()


myWorld.runSimulation(1) 




