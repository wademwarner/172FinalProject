from  Classes.AbstractWorld import AbstractWorld

from Classes.Graph import Graph

from Classes.Vehicle import Vehicle

from Classes.AbstractVehicle import AbstractVehicle



import pygame

import re

import random as ran

from __builtin__ import True



#from main import graphObj

pygame.font.init() 



class World(AbstractWorld,AbstractVehicle, Graph):

	

	def __init__(self,x):

		AbstractWorld.__init__(self)

		self.height = 600

		self.width = 800

		self.screen = pygame.display.set_mode((self.width, self.height))

		self.black = (0,0,0)

		self.blue = (0,0,255)

		self.red = (255,0,0)

		self.green =(0,255,0)

		self.pple = (255,0,255)        					#the color purple 

		self.clock = pygame.time.Clock()

		self.font  = pygame.font.SysFont('Comic Sans MS', 30)

		'''wmw additions, thin out after new changes are made'''

		self.vID = []					#a list of all the nodes 

		self.vtxPosit = {}				#dictionary of all the vertex (nodes) positinos 


		'''
		Remove all of these that are not used once the dispay is made 
		'''


		self.prevNode = []

		self.line_CURV = []

		self.line_graph = []

		self.line_list = {}

		self.graphViz = x
		
		self.orders = {}  	#a dictionary to store the orders with elements as (current node,end node,(x,y) position)
		
		self.orderPath = {}  #the shortest path a truck should follow to complete a specific order
		
		self.moveOrder = {} #a dictionary used to help the movement of orders
		
		self.orderStep = {} #track the steps of moving over a line as stepLenght, steps left
	
		#truck = pygame.image.load('C:\Users\Thoma\Desktop\truck.jpg')
		truck = pygame.image.load('C:\Users\Thoma\Desktop\smallTruck.jpg') #upload an image of a truck
		self.truck = pygame.transform.scale(truck,(20,20))		#Scale the image
	
		
		

	def runSimulation(self, fps=10, initialTime=5*60, finalTime=23*60): #fps was 1 before

		'''
		This will give you a list of ALL cars which are in the system
		'''
		trucks = self.getInitialTruckLocations()
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t)) 

		'''
		We will run a simulation where "t" is the time index
		'''
		for t in xrange(initialTime,finalTime):	                        #need soemthing in here to alwas draw the edges and allow for animations to occur
			print "\n\n Time: %02d:%02d"%(t/60, t%60)
			# each minute we can get a few new orders
			newOrders = self.getNewOrdersForGivenTime(t)
			print "New orders:"  
			for c in newOrders:                   #use c to animate the moving of the trucks based on the animation procedure 
				print c
				
				self.orders[c] = list(self.getRandVerts())									#create a new order with its starting position as random
				self.orders[c].append([float(self.vtxPosit[self.orders[c][0]][0]),float(self.vtxPosit[self.orders[c][0]][1])])  #sets the x,y coordinate of the 
				self.moveOrder[c] = [self.vtxPosit[self.orders[c][0]][0],self.vtxPosit[self.orders[c][0]][1],self.vtxPosit[self.orders[c][1]][0],
									self.vtxPosit[self.orders[c][1]][1]] #add in the x1,y1,x2,y2 poisiton 
				ty = float(self.graphViz.getTime(self.orders[c][0],self.graphViz.getNextNode(self.orders[c][0],self.orders[c][1])))
				self.orderStep[c] = [ty,ty]
				#self.orderPath[c] = self.graphViz.find_path(self.orders[c][0],self.orders[c][1])#get the shortest path and store it
				
				
				
				
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
			self.appearances()              #used so that the vertices are shown on the screen
			
			for i in self.orders.keys():													#a For loop to animate each truck moving
				self.moveTruck(i,self.orders[i][0],self.orders[i][1])#,self.orderPath[i]) add path back in	#Animate the movement of each truck
				print('I ran once!')
	
     
			pygame.display.update()	
			for event in pygame.event.get():
				pass   
			self.clock.tick(fps)




	def moveTruck(self,orderNum,indexNode,end):  #problems here likely means problems in the graph class path finding algorithm
		
		nextNode = self.graphViz.getNextNode(indexNode,end)
		
		if indexNode == end:
			self.screen.blit(self.truck,(self.orders[orderNum][2][0],self.orders[orderNum][2][1]))
			#pygame.draw.rect(self.screen, self.green,(self.vtxPosit[indexNode][0]-2,self.vtxPosit[indexNode][1]-2,12,12))    #using  rectangle instead of truck image
			del self.orders[orderNum] 
			del self.moveOrder[orderNum]
			del self.orderStep[orderNum]
			#del self.orderPath[orderNum] 

		
		
		else: #moving on the path incramentally 
			print(orderNum)
			print(self.orders[orderNum][2])
			print(self.moveOrder[orderNum][0])
			print(self.moveOrder[orderNum][1])
			print(self.moveOrder[orderNum][2])
			print(self.moveOrder[orderNum][3])
			print('the step is')
			print(self.orderStep[orderNum][0])
			print('the number of stes left is')
			print(self.orderStep[orderNum][1])
			
			
		 
			x1 = float(self.moveOrder[orderNum][0] )
			y1 = float(self.moveOrder[orderNum][1])
			x2=  float(self.moveOrder[orderNum][2]) 
			y2 = float(self.moveOrder[orderNum][3])
			print('movement of x is')
			print(float((1/self.orderStep[orderNum][0])*(x2 -x1)))
			print('movement of y is')
			print(float((1/self.orderStep[orderNum][0])*(y2 -y1)))
			self.orders[orderNum][2][0] += float((1/self.orderStep[orderNum][0])*(x2 -x1))
			self.orders[orderNum][2][1] += float((1/self.orderStep[orderNum][0])*(y2 -y1))
			self.orderStep[orderNum][1] -= float(1) #adjust the steps of the order
			
			self.screen.blit(self.truck,(self.orders[orderNum][2][0],self.orders[orderNum][2][1]))
			
			if self.orderStep[orderNum][1] == 0:
				print('new thing to go over')
				self.moveOrder[orderNum][0] = self.orders[orderNum][2][0]
				self.moveOrder[orderNum][1] = self.orders[orderNum][2][1]
				self.moveOrder[orderNum][2] = self.vtxPosit[self.graphViz.getNextNode(nextNode,end)][0]
				self.moveOrder[orderNum][3] = self.vtxPosit[self.graphViz.getNextNode(nextNode,end)][1]
				self.orderStep[orderNum][0] = float(self.graphViz.getTime(nextNode,self.graphViz.getNextNode(nextNode,end)))
				self.orderStep[orderNum][1] = self.orderStep[orderNum][0]
				
	
	        

		

  	'''WMW'''

	def changeToViz(self,verts): #takes x and y in vertices and imports as vert to be graphed
		
		
		for i in verts:

			self.vID.append(i)

		for i in range(len(self.vID)):

			self.vID[i][1] = int(self.vID[i][1]*self.width)

		for i in range(len(self.vID)):

			self.vID[i][2] = int(self.vID[i][2]*self.height)

		for i in self.vID:

			self.vtxPosit[i[0]] = (i[1],i[2])

			



	def appearances(self): #put vertices on display

		for vertex in self.vtxPosit: #every vertex

			#pygame.draw.rect(self.screen, self.blue,(self.vtxPosit[vertex][0]-2,self.vtxPosit[vertex][1]-2,4,4)) #The original code used	
			pygame.draw.rect(self.screen, self.pple,(self.vtxPosit[vertex][0]-2,self.vtxPosit[vertex][1]-2,7,7)) #if you want nodes to be a different color
		for edge in self.line_list: 

			for i in range(0,len(self.line_list[edge])-2):

				pygame.draw.line(self.screen,self.blue,self.line_list[edge][i],self.line_list[edge][i+1],3)

							

		pygame.display.update()

		#get neighbors of vertices and draw a line


	def drawGraph(self,node,node_neighbors):	#Draws the vertexes with their correct line curvature 

		if node_neighbors != None:		

			vertPoint = self.vtxPosit[node]

			self.prevNode = []

			for nn in node_neighbors: #nn -> neighbor node

				if nn in self.prevNode or node == nn:

					continue

				vertNeighbor = self.vtxPosit[nn]

				edge_init = (node,nn)

				#print(edge_init)

				self.line_CURV = []

				self.line_graph = []

				list_curV = self.graphViz.getLine(node,nn) #list of points to give the graph its "curV" (V -> vertex)
			
				for curv in list_curV:

					list_curV_CTVX = (curv[0]*self.width, curv[1]*self.height)

					self.line_CURV.append(list_curV_CTVX)



				#print(self.line_CURV)

				self.line_graph.append(vertPoint) #stores point of start vertex as first point to be lined

				for curv in self.line_CURV:

					self.line_graph.append(curv) #CHECK ME

				self.line_graph.append(vertNeighbor)

				self.line_list[edge_init] = self.line_graph

				self.prevNode.append(nn)



	def getRandVerts(self):

		num_verts = len(self.vID)

		sameNum = False

		while not sameNum:

			a = ran.randint(0,num_verts-1)

			b = ran.randint(0,num_verts-1)

			if a == b:   #if the random node is the same as the trucks initial position you need to get a new end node

				self.getRandVerts()

			else:

				return self.vID[a][0],self.vID[b][0]

			

	def realVertexConv(self,list_vtx):				#not sure what this does 

		newList = []

		for vtx in list_vtx:

			newList.append(self.vtxPosit[vtx])

		return newList
