from Classes.World import World

from Classes.Graph import Graph


myWorld = World()
graphObj = Graph()

for i in range(len(myWorld.Edges)):
    graphObj.add_node(myWorld.Edges[i][0])
    graphObj.add_edge(myWorld.Edges[i][0], myWorld.Edges[i][1])
    #graphObj.setTime(myWorld.Edges[i][0], myWorld.Edges[i][1], myWorld.Edges[i][2])  need to change to get the time working
    #graphObj.addLine(myWorld.Edges[i][0], myWorld.Edges[i][1], myWorld.Edges[i][3])  need to change all get the line working
print(graphObj.__str__())
#print(graphObj.getTime(0, 10))
#print(graphObj.getLine(0,10))


print myWorld.Edges 

print myWorld.Verticies

#initalize a grpah object
#add all the stuff
#try and print it all


myWorld.runSimulation(10)




