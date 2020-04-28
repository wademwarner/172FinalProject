from  Classes.AbstractWorld import AbstractWorld

from Classes.Graph import Graph

from Classes.Vehicle import Vehicle

from Classes.AbstractVehicle import AbstractVehicle

from Classes.Trucks import Trucks

from Classes.Facilities import Facilities 

import pygame

import re

import random as ran

from __builtin__ import True



#from main import graphObj

pygame.font.init() 



class World(AbstractWorld,AbstractVehicle, Graph, Trucks, Facilities):

	

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
		
		self.Warehouses = {}
		
		self.ProductionLines = {}
		
		self.facility = Facilities()
		
		self.orderInfo = {}   #'Current Position', 'End Position','Truck Used', 'Finished' old stuff here
		
		self.order_sequence = {}
		
		
		
		self.truckObj = {} #dictionary to hold all the truck objects 
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):



		Warehouses = self.getLocationOfWarehouses()
		print (Warehouses)
		#print('how warehouses are in facilities ')
		self.Warehouses = self.facility.defineWarehouses(Warehouses)
		
		'''
		print(self.Warehouses)
		This is how the warehouses are stored in self.Warehouses
		{'A': [37, 0], 'C': [5, 91], 'B': [208, 98], 'E': [140, 200], 'D': [20, 33], 'G': [68, 16], 'F': [165, 147], 'H': [111, 172]}
		'''

		ProductionLines = self.getProductionLines()
		self.defineLines
		print (ProductionLines)
		
		self.ProductionLines = self.facility.defineLines(ProductionLines)
		
		'''
		print(self.ProductionLines) -Currently we are not looking at capacity for these, only bring what is needed for each step
		{'L4': [89, 84, 168, 153, 26], 'L2': [82, 10, 174, 186, 185], 'L3': [1, 15, 3, 13, 32], 'L1': [119, 141, 181, 46, 25]}
		
		'''
		

		'''
		This will give you a list of ALL cars which are in the system
		'''
		trucks = self.getInitialTruckLocations()
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t)) 
			
			self.truckObj[i] = Trucks(i,t.currentPossition[1],t.capacity,self.vtxPosit[t.currentPossition[1]])
 

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
				print c.productionProcess
				print c.finalLocation
				
				#create a new order with its starting and end position as random
				#liss = list(self.getRandVerts())
			
				#self.orderInfo[c] = {'Current Position':liss[0], 'End Position':liss[1],'Truck Used':None, 'Finished':False}
				#self.findTruckForOrder(c)

				#print(self.orderInfo[c])
	
				
				
				
				
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
			self.appearances()              #used so that the vertices are shown on the screen
				
			for i in self.orderInfo.keys(): #maybe make evrything in this for loop into a method 
				
				if self.orderInfo[i]['Truck Used'] != None and self.orderInfo[i]['Finished'] == False:
					
					if self.orderInfo[i]['Current Position'] == self.truckObj[self.orderInfo[i]['Truck Used']].getEndPosition():
						
						#moving the truck when the it is on its way to the order!
						
						self.moveTruck(i,self.orderInfo[i]['Truck Used'],self.truckObj[self.orderInfo[i]['Truck Used']].getPosition(),
									self.truckObj[self.orderInfo[i]['Truck Used']].getEndPosition())
							
												
					else:
						print('Truck going with order')
							#Animate the movement of each truck
						self.moveTruck(i,self.orderInfo[i]['Truck Used'],self.truckObj[self.orderInfo[i]['Truck Used']].getPosition(),
									self.orderInfo[i]['End Position'])
				else:
					self.findTruckForOrder(i) #seeing if a truck has been freed up form last go around
     
			pygame.display.update()	
			for event in pygame.event.get():
				pass   
			self.clock.tick(fps)




	def moveTruck(self,orderNumber,TruckNum,indexNode,end):  #problems here likely means problems in the graph class path finding algorithm

		
		nextNode = self.graphViz.getNextNode(indexNode,end) #figure out the next node the truck is traveling to
	
		stepSize = float((self.graphViz.getLineLength(indexNode,nextNode)-1)/self.truckObj[TruckNum].getTimeOfAPath())
		#add in an ending condition here eventually 
		'''
		Sees if the truck index and path is done so either the truck made it the end position or if it needs a new end position
		Then if the path is stright it executes the animation and if its curve then executes the animation
		'''
		if indexNode == end:
			
			if self.orderInfo[orderNumber]['Current Position'] == self.orderInfo[orderNumber]['End Position']: 
				#Deleting the order and freeing up the truck once the order has been fulfilled
				print('we done with the animation now!!!!!!')
				self.truckObj[TruckNum].setTruckUsage(False)
				
				#del self.orderInfo[orderNumber]
				self.orderInfo[orderNumber]['Finished'] = True
				self.orderInfo[orderNumber]['Truck Used'] = None
				#part 2 add in something here add something in for the profit count update
				
				
				
				
			else:#the truck reached the order position now it needs to go to the order end position
				
				self.moveTruckToOrderDest(orderNumber, indexNode, TruckNum)
				
			
			
			
		elif self.graphViz.isLineStraight(indexNode,nextNode): #animation for if the line is straight
	
			
			self.moveTruckStright(indexNode,nextNode,TruckNum)
		
		else: #moving the truck along a curved line
			
			self.moveTruckCurved(stepSize,indexNode,nextNode,TruckNum)
			
			
		if self.truckObj[TruckNum].getTimeLeftOnPath() > self.truckObj[TruckNum].getTimeOfAPath(): #resest the next node if it done on path between vertex's
			
			#updating the trucks positions when its traveling to the order
			
			'''
			Likely will need to change this logic once the warehouses are added to this part 
			
			'''
			if self.orderInfo[orderNumber]['Current Position'] == self.truckObj[self.orderInfo[orderNumber]['Truck Used']].getEndPosition(): 
				#updating the trucks positions when its traveling to the order

				self.truckObj[TruckNum].setNewPosition(nextNode)
				self.truckObj[TruckNum].setEndPosition(self.orderInfo[orderNumber]['End Position']) #Added in with new additions, remove if fucked

				print('new truck position befor the order')
				
			else:			#the truck moving with the order to the orders end position
				
				self.orderInfo[orderNumber]['Current Position'] = nextNode
				self.truckObj[TruckNum].setNewPosition(nextNode)
				print('Trukc going to a new position with the order')
			#all below here needs to be adjusted for when the truck reaches a new node
			self.truckObj[TruckNum].setPosition_x_Coordinates(float(self.vtxPosit[nextNode][0]))
			self.truckObj[TruckNum].setPosition_y_Coordinates(float(self.vtxPosit[nextNode][1]))
			
			self.truckObj[TruckNum].setTimeOfaNewPath(float(self.graphViz.getTime(self.truckObj[TruckNum].getPosition(),
																self.graphViz.getNextNode(self.truckObj[TruckNum].getPosition(),self.truckObj[TruckNum].getEndPosition()))))

	
		
	def moveTruckToOrderDest(self,orderNumber,indexNode,TruckNum):
		
		self.truckObj[self.orderInfo[orderNumber]['Truck Used']].setEndPosition(self.orderInfo[orderNumber]['End Position']) 
			
		#sets a new end position of the truck to be the same as the orders end node
		
		
		print('new truck position for the going to order')
		
		self.truckObj[TruckNum].setPosition_x_Coordinates(float(self.vtxPosit[indexNode][0]))
		self.truckObj[TruckNum].setPosition_y_Coordinates(float(self.vtxPosit[indexNode][1]))
		#set the new x and y coordinates of the truck

		#add the new time for the next Edge and a new time on path of 1, 
		self.truckObj[TruckNum].setTimeOfaNewPath(float(self.graphViz.getTime(self.truckObj[TruckNum].getPosition(),
															self.graphViz.getNextNode(self.truckObj[TruckNum].getPosition(),self.truckObj[TruckNum].getEndPosition()))))
		
	
	def moveTruckStright(self,indexNode,nextNode,TruckNum):
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
		#print('truck moved on the striaht')
		
		
	def moveTruckCurved(self,stepSize,indexNode,nextNode,TruckNum):
		stepLength = int(stepSize*self.truckObj[TruckNum].getTimeLeftOnPath())#get the number of line lengths to go for the the line
		stepDec = float(stepSize*self.truckObj[TruckNum].getTimeLeftOnPath()) - stepLength #+ 1		#this gives the decimal of how far along the line the points will be
		#print('step dist and decimal ')
		#print(stepLength)
		#print(stepDec)
		
		list_curV = self.graphViz.getLine(indexNode,nextNode) #list of points to give the graph its "curV" (V -> vertex)
		lineStart = list_curV[stepLength - 1]
		lineEnd = list_curV[stepLength]
		xDiff = float((lineStart[0] - lineEnd[0])*stepDec)	#getting the amount of the line that should be traveled i the x direction
		yDiff = float((lineStart[1] - lineEnd[1])*stepDec)	#getting the amount of the line that should be traveled i the x direction
	
		self.truckObj[TruckNum].setPosition_x_Coordinates(self.width*(xDiff + lineStart[0]))		#sets the truck positions to its new coordinates in the x direction
		self.truckObj[TruckNum].setPosition_y_Coordinates(self.height*(yDiff + lineStart[1]))		#sets the truck positions to its new coordinates in the y direction
		self.truckObj[TruckNum].setNewTimeLeft() #incraments the truck time on the path by one
		
		self.screen.blit(self.truck,(self.truckObj[TruckNum].getPosition_x_Coordinates()-10,self.truckObj[TruckNum].getPosition_y_Coordinates()-10))
		#print('truck moved on the curve')
		
	def findTruckForOrder(self,orderNumber):
		
		truckNum = -1
		'''
		this gets a new truck for any order so it can be moved
		'''
		
		for i in self.truckObj.keys():
			#add something to do with capacity here in part 2
			if self.truckObj[i].isTruckInUse() == False:
				self.truckObj[i].setTruckUsage(True)
				#self.orders[orderNumber][2]=i
				self.orderInfo[orderNumber]['Truck Used'] = i
				truckNum = i
				break
		print('truck object key and then orders key')
		
		if truckNum != -1: #this is true if a new truck was found for the 
			self.truckObj[truckNum].setNewOrderForTruck(orderNumber)
			self.setNewTruckForOrder(orderNumber, truckNum)
			#return truckNum
		else:
			self.orderInfo[orderNumber]['Truck Used'] = None
			
			
	
	
	
	
	def setNewTruckForOrder(self,orderNumber,truckNumber): #this sets the truck up to move to the order postion
		#This needs to changed based upon if a truck is going to an order, warehouse or production site in part 2
		
		
		self.truckObj[truckNumber].setEndPosition(self.orderInfo[orderNumber]['Current Position'])

		self.truckObj[truckNumber].setTimeOfaNewPath(float(self.graphViz.getTime(self.truckObj[truckNumber].getPosition(),
																self.graphViz.getNextNode(self.truckObj[truckNumber].getPosition(),self.truckObj[truckNumber].getEndPosition()))))
		#return truckNumber

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
