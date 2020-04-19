from  Classes.AbstractWorld import AbstractWorld

from Classes.Graph import Graph

from Classes.Vehicle import Vehicle

from Classes.AbstractVehicle import AbstractVehicle

from Classes.Trucks import Trucks


import pygame

import re

import random as ran

from __builtin__ import True



#from main import graphObj

pygame.font.init() 



class World(AbstractWorld,AbstractVehicle, Graph, Trucks):

	

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
		
		self.orders = {}  	#a dictionary to store the orders with elements as (current node,end node,Truck Used, Finished/Not(a boolean)
	
		#truck = pygame.image.load('C:\Users\Thoma\Desktop\truck.jpg')
		truck = pygame.image.load('C:\Users\Thoma\Desktop\smallTruck.jpg') #upload an image of a truck
		self.truck = pygame.transform.scale(truck,(20,20))		#Scale the image
		
		
		self.truckObj = {} #dictionary to hold all the truck objects 
		
		

	def runSimulation(self, fps=10, initialTime=5*60, finalTime=23*60): #fps was 1 before

		'''
		This will give you a list of ALL cars which are in the system
		'''
		aux = []
		trucks = self.getInitialTruckLocations()
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t))
			
			self.truckObj[i] = Trucks(i,t.currentPossition[1],t.capacity,self.vtxPosit[t.currentPossition[1]])
			#{'Path':[currentNode,EndNode,location(x,y)],'Time':[TimeonPath,TimeLeftOnPath],'Order':[Truck ID,OrderNmber],'Use':[T/F if truck is in use,capacity]}



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
				#self.orders[c].append(0)
				self.orders[c].append(-1)								#0=truck being used for the order FALSE is for fnished or not with order
				self.findTruckForOrder(c)
				self.orders[c].append(False)
				#the order dictionary has (current node, end node, Truck Used, Finished/Not(a boolean T/F)
	
				
				
				
				
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
			self.appearances()              #used so that the vertices are shown on the screen
			
			for i in self.orders.keys():	
				if self.orders[i][2] != -1: #if an order deosnt have a truck its truck number is -1, likely change this in part 2
					if self.orders[i][0] == self.truckObj[self.orders[i][2]].getEndPosition():	

						self.moveTruck(i,self.orders[i][2],self.truckObj[self.orders[i][2]].getPosition(),self.truckObj[self.orders[i][2]].getEndPosition())
							#moveTruck(self,orderNumber,TruckNum,indexNode,end) so it has moveTruck(order NUmber,Truck Number, truck position, truck end position)
												
					else:
						print('Truck going with order')
						self.moveTruck(i,self.orders[i][2],self.truckObj[self.orders[i][2]].getPosition(),self.orders[i][1])	#Animate the movement of each truck
						#moveTruck(self,orderNumber,TruckNum,indexNode,end) so it has moveTruck(order NUmber,Truck Number, truck position, order end position)
				else:
					self.findTruckForOrder(i) #seeing if a truck has been freed up form last go around
     
			pygame.display.update()	
			for event in pygame.event.get():
				pass   
			self.clock.tick(fps)




	def moveTruck(self,orderNumber,TruckNum,indexNode,end):  #problems here likely means problems in the graph class path finding algorithm

		print(orderNumber)
		nextNode = self.graphViz.getNextNode(indexNode,end) #figure out the next node the truck is traveling to
		print(self.graphViz.getLineLength(indexNode,nextNode)-1)
		print(self.truckObj[TruckNum].getTimeOfAPath())
		stepSize = float((self.graphViz.getLineLength(indexNode,nextNode)-1)/self.truckObj[TruckNum].getTimeOfAPath())
		#add in an ending condition here eventually 
		'''
		Sees if the truck index and path is done so either the truck made it the end position or if it needs a new end position
		Then if the path is stright it executes the animation and if its curve then executes the animation
		'''
		if indexNode == end:
			if self.orders[orderNumber][0] == self.orders[orderNumber][0]: #the truck reached the order end spot
				print('we done with the animation now!!!!!!')
				self.truckObj[TruckNum].setTruckUsage(False)
				del self.orders[orderNumber]
				#pygame.time.delay(10000) this adds a 10 seconds delay when the truck delivers the order to its end position
				#part 2 add in something here add something in for the profit count update
				
				
				
				
			else:#the truck reached the order position now it needs to go to the order end position
				self.truckObj[self.orders[orderNumber][2]].setEndPosition(self.orders[orderNumber][1]) 
				#sets a new end position of the truck to be the same as the orders end node
				
				
				print('new truck position for the going to order')
				
				self.truckObj[TruckNum].setPosition_x_Coordinates(float(self.vtxPosit[indexNode][0]))
				self.truckObj[TruckNum].setPosition_y_Coordinates(float(self.vtxPosit[indexNode][1]))
				#set the new x and y coordinates of the truck

				#add the new time for the next Edge and a new time on path of 1, 
				self.truckObj[TruckNum].setTimeOfaNewPath(float(self.graphViz.getTime(self.truckObj[TruckNum].getPosition(),
																	self.graphViz.getNextNode(self.truckObj[TruckNum].getPosition(),self.truckObj[TruckNum].getEndPosition()))))
				
			
			
			
		elif self.graphViz.isLineStraight(indexNode,nextNode): #animation for if the line is straight
	
			
			
			
			x1 = float(self.vtxPosit[indexNode][0]) #the x position of a a line start
			y1 = float(self.vtxPosit[indexNode][1]) #the y positin of aline start
			x2=  float(self.vtxPosit[nextNode][0])  #the x position of a lines end
			y2 = float(self.vtxPosit[nextNode][1]) #the y position of a lines end
			
			self.truckObj[TruckNum].setPosition_x_Coordinates(x1+float(self.truckObj[TruckNum].getTimeLeftOnPath()/self.truckObj[TruckNum].getTimeOfAPath()*(x2 -x1)))		
			self.truckObj[TruckNum].setPosition_y_Coordinates(y1+float(self.truckObj[TruckNum].getTimeLeftOnPath()/self.truckObj[TruckNum].getTimeOfAPath()*(y2 -y1)))
			'''
			sets the x and y position of the of the truck after movement
			where x,y = (stepLeft/stepSize)*(x2-x1)
			'''
			
			self.truckObj[TruckNum].setNewTimeLeft() #adjust the steps of the order
			
			#blits the truck to thr correct position on the screem
			self.screen.blit(self.truck,(self.truckObj[TruckNum].getPosition_x_Coordinates()-10,self.truckObj[TruckNum].getPosition_y_Coordinates()-10))
			print('truck moved on the striaht')
		
		else: #moving the truck along a curved line
			
			stepLength = int(stepSize*self.truckObj[TruckNum].getTimeLeftOnPath())#get the number of line lengths to go for the the line
			stepDec = float(stepSize*self.truckObj[TruckNum].getTimeLeftOnPath()) - stepLength #+ 1		#this gives the decimal of how far along the line the points will be
			print('step dist and decimal ')
			print(stepLength)
			print(stepDec)
			
			list_curV = self.graphViz.getLine(indexNode,nextNode) #list of points to give the graph its "curV" (V -> vertex)
			lineStart = list_curV[stepLength - 1]
			lineEnd = list_curV[stepLength]
			xDiff = float((lineStart[0] - lineEnd[0])*stepDec)	#getting the amount of the line that should be traveled i the x direction
			yDiff = float((lineStart[1] - lineEnd[1])*stepDec)	#getting the amount of the line that should be traveled i the x direction
		
			self.truckObj[TruckNum].setPosition_x_Coordinates(self.width*(xDiff + lineStart[0]))		#sets the truck positions to its new coordinates in the x direction
			self.truckObj[TruckNum].setPosition_y_Coordinates(self.height*(yDiff + lineStart[1]))		#sets the truck positions to its new coordinates in the y direction
			self.truckObj[TruckNum].setNewTimeLeft() #incraments the truck time on the path by one
			
			self.screen.blit(self.truck,(self.truckObj[TruckNum].getPosition_x_Coordinates()-10,self.truckObj[TruckNum].getPosition_y_Coordinates()-10))
			print('truck moved on the curve')
			
			
		if self.truckObj[TruckNum].getTimeLeftOnPath() > self.truckObj[TruckNum].getTimeOfAPath(): #resest the next node if it done on path between vertex's
			
			if self.orders[orderNumber][0] == self.truckObj[self.orders[orderNumber][2]].getEndPosition(): #updating the trucks positions when its traveling to the order

				self.truckObj[TruckNum].setNewPosition(nextNode)

				print('new truck position befor the order')
				
			else:			#the truck moving with the order to the orders end position
				self.orders[orderNumber][0] = nextNode
				self.truckObj[TruckNum].setNewPosition(nextNode)
				print('Trukc going to a new position with the order')
			#all below here needs to be adjusted for when the truck reaches a new node
			self.truckObj[TruckNum].setPosition_x_Coordinates(float(self.vtxPosit[nextNode][0]))
			self.truckObj[TruckNum].setPosition_y_Coordinates(float(self.vtxPosit[nextNode][1]))
			
			self.truckObj[TruckNum].setTimeOfaNewPath(float(self.graphViz.getTime(self.truckObj[TruckNum].getPosition(),
																self.graphViz.getNextNode(self.truckObj[TruckNum].getPosition(),self.truckObj[TruckNum].getEndPosition()))))

	
		
	def findTruckForOrder(self,orderNumber):
		
		truckNum = -1
		'''
		this gets a new truck for any order so it can be moved
		'''
		
		for i in self.truckObj.keys():
			#add something to do with capacity here in part 2
			if self.truckObj[i].isTruckInUse() == False:
				self.truckObj[i].setTruckUsage(True)
				self.orders[orderNumber][2]=i
				truckNum = i
				break
		print('truck object key and then orders key')
		
		if truckNum != -1: #this is true if a new truck was found for the 
			self.truckObj[truckNum].setNewOrderForTruck(orderNumber)
			self.setNewTruckForOrder(orderNumber, truckNum)
		else:
			self.orders[orderNumber].append(None)
			
	
	
	
	
	def setNewTruckForOrder(self,orderNumber,truckNumber): #this sets the truck up to move to the order postion
		#This needs to changed based upon if a truck is going to an order, warehouse or production site in part 2
		
		
		self.truckObj[truckNumber].setEndPosition(self.orders[orderNumber][0])

		self.truckObj[truckNumber].setTimeOfaNewPath(float(self.graphViz.getTime(self.truckObj[truckNumber].getPosition(),
																self.graphViz.getNextNode(self.truckObj[truckNumber].getPosition(),self.truckObj[truckNumber].getEndPosition()))))
	

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
