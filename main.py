from Classes.World import World

from Classes.Graph import Graph


myWorld = World()
graphObj = Graph()

for i in range(len(myWorld.Edges)):
    graphObj.add_node(myWorld.Edges[i][0]) 


for j in range(len(myWorld.Edges)):   
    graphObj.add_edge(myWorld.Edges[j][0], myWorld.Edges[j][1],1) #graphObj.add_edge(myWorld.Edges[i][0], myWorld.Edges[i][1],myWorld.Edges[i][2]) for when we want to add actual time
print(graphObj.__str__())
print(graphObj.getTime(0, 10))
for u in range(len(myWorld.Edges)):
    print(graphObj.getNeighbor(u))


print myWorld.Edges 

print myWorld.Verticies

#initalize a grpah object
#add all the stuff
#try and print it all


myWorld.runSimulation(10)




