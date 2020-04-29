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
		
		
		
		self.facilObj = Facilities()
		
		self.orderInfo = {}   #'Current Position', 'End Position','Truck Used', 'Finished' old stuff here
		
		self.order_sequence = {}
		
		self.ProdSet = True
		
		self.ProductionInfo = {}
		
		self.truckObj = {} #dictionary to hold all the truck objects 
		
		
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):


		Warehouses = self.getLocationOfWarehouses()
		self.facilObj.defineWarehouses(Warehouses)
		
		'''
		print(self.Warehouses)
		This is how the warehouses are stored in self.Warehouses
		{'A': [37, 0], 'C': [5, 91], 'B': [208, 98], 'E': [140, 200], 'D': [20, 33], 'G': [68, 16], 'F': [165, 147], 'H': [111, 172]}
		
		'''
		
		

		ProductionLines = self.getProductionLines()
		print(ProductionLines)
		
		self.facilObj.defineLines(ProductionLines)
		
		'''
		print(self.ProductionLines) -Currently we are not looking at capacity for these, only bring what is needed for each step
		{'L4': [89, 84, 168, 153, 26], 'L2': [82, 10, 174, 186, 185], 'L3': [1, 15, 3, 13, 32], 'L1': [119, 141, 181, 46, 25]}
		
		Bellow is a nested for loop to add the capacity and usage condition to all the production site with their node as the key 
		This is needed for determining if an order can be procesed and if material is needed for that specific order also 
		'''
		
		
		if self.ProdSet:
			self.ProdSet = False
			for i in self.facilObj.lines.keys():
				for j in range(len(self.facilObj.lines[i])):
					self.ProductionInfo[self.facilObj.lines[i][j]] = {'Capacity Max':100, 'Capacity Held':0, 'In Use': False}
					
			print(self.ProductionInfo)
		
		
		
		

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
				self.createOrderDict(c,c.productionProcess,c.finalLocation)
				'''
				need to call a method here to create an order dict 
				
				{'processingTime': 7, 'processinLine': 'L2', 'materialNeeded[tons]': 7, 'resourceNeeded': 'D'}, {'processingTime': 6, 'processinLine': 'L1', 'materialNeeded[tons]': 9, 'resourceNeeded': 'B'}
				
				'''
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
			
			
			for i in self.orderInfo.keys(): #maybe make everything in this for loop into a method 
				
				stepL = len(self.order_sequence[i])
				step = self.orderInfo[i]['Order Step']
				
				if self.orderInfo[i]['Order TIS'] == 0: #iterates through when the order if first created
					if self.ProductionInfo[self.orderInfo[i]['Current Node']]['Capacity Held'] >= self.order_sequence[i][stepL-step]['Material']:
						#start the order production
						self.orderInfo[i]['Order Process'] = 2
						
					else: #finding the warehouse closest ot the production site
						resLocation = self.findClosestWarehouse(self.orderInfo[i]['Current Node'], self.order_sequence[i][stepL-step]['Resource']) 
						self.orderInfo[i]['Order Process'] = 1
						self.findTruckForOrder(i,resLocation,self.order_sequence[i][stepL-step]['Material'],1)
						
						
						'''
						have truck get material 
						
						Assign this truck to be the orders truck in orderInfo['Truck Used']
						'''
				elif self.orderInfo[i]['Order Process'] == 0:
					pass
					#order is waiting for a truck still at the first location
					
				elif self.orderInfo[i]['Order Process'] == 1:
					pass
					#order is waiting for material
					
				elif self.orderInfo[i]['Order Process'] == 2:
					pass
					#order is being produced
					
				else:
					pass
					#order is going to the next order location 
				
				
				
				
				
				self.orderInfo[i]['Order TIS'] += 1
				
				
			
	
				
			'''	
			ProductionInfo = {'Capacity Max':100, 'Capacity Held':0, 'In Use': False}
			
			order_sequence = [{(ordL-i):{'Process Time': ,'Material':,'Resource':,'Production Line': 0}}]
			
			orderInfo =	{'Current Node':,'End Node':,'Truck Used':None,'Delivery Location','Finished':False,'Order Step':1,'Order TIS':0,'Order Process':0}
						
							0-order was created and nothing has happened 
							1-order is waiting for material at a production site
							2-order is being produced
							3-order is moving to the next location 
							
     		'''
			pygame.display.update()	
			for event in pygame.event.get():
				pass   
			self.clock.tick(fps)




	def createOrderDict(self,orderNum,orderProcess,endNode): #a method to create two dictionaries to be used for the order process 
		
		ordL = len(orderProcess)
		print(ordL)
		#create the order dictionary
		for i in range(ordL):
				
			if (ordL-i)!= ordL:
				self.order_sequence[orderNum].append({(ordL-i) : {'Process Time': orderProcess[ordL-i-1]['processingTime'],
											'Material': orderProcess[ordL-i-1]['materialNeeded[tons]'],
											'Resource': orderProcess[ordL-i-1]['resourceNeeded'],
											'Production Line': 0}})
				
				self.order_sequence[orderNum][i][ordL-i]['Production Line'] = self.findOrderPath(orderNum, 
																							orderProcess[ordL-i-1]['processinLine'], 
																							self.order_sequence[orderNum][i-1][ordL-i + 1]['Production Line'])
				
				
			else: #first iteration through the forloop 
				self.order_sequence[orderNum] = [{(ordL-i):{'Process Time': orderProcess[ordL-i-1]['processingTime'],
											'Material': orderProcess[ordL-i-1]['materialNeeded[tons]'],
											'Resource': orderProcess[ordL-i-1]['resourceNeeded'],
											'Production Line': 0}}]
	
				self.order_sequence[orderNum][i][ordL-i]['Production Line'] = self.findOrderPath(orderNum, 
																							orderProcess[ordL-i-1]['processinLine'], 
																							endNode)
		
		print('the order sequence is')
		print self.order_sequence[orderNum]
		
		'''
		[{3: {'Material': 3, 'Resource': 'E', 'Production Line': 13, 'Process Time': 6}}, 
		{2: {'Material': 9, 'Resource': 'G', 'Production Line': 84, 'Process Time': 5}}, 
		{1: {'Material': 9, 'Resource': 'B', 'Production Line': 46, 'Process Time': 5}}]
		
		'''
		
		self.orderInfo[orderNum] = {'Current Node':self.order_sequence[orderNum][ordL-1][1]['Production Line'],
								'End Node':endNode, #maybe change this to the 2nd step location
								'Truck Used':None, 
								'Delivery Location':self.order_sequence[orderNum][ordL-2][1]['Production Line'], #
								'Finished':False,
								'Order Step':1, 
								'Order TIS':0,
								'Order Process':0}
							'''
							0-order was created andnothing has happened 
							1-order is waiting for material at a production site
							2-order is being produced
							3-order is moving to the next location 
							
							'''
		
		
		

		print('the order info is ')
		print self.orderInfo[orderNum]
			
		
			
		
	'''
	Need to figure out the exact nodes of produciton facilities the order will go to from the findOrderPath method
	Then add everything into a dicitonary with all that 
	Store each step as a different sub key of the dictionary, step1, step2,...., stepN
	{'processingTime': 7, 'processinLine': 'location of the node of this produciton line', 'materialNeeded[tons]': 7, 'resourceNeeded': 'D'}
	'''
	#self.order_sequence = {'Process Time':,'Production Line':,'Material and Resource':,}
	#self.orderInfo = {'Current Node':,'End Node':,'Truck Used':, 'Delivery Location'L, 'Finished:False,'Order Step':, 'Order TIS':0}


	
	
	def findOrderPath(self,orderNumber, ProdSite, endNode): #a dictionary to find the shortest optimal production locations based on the final location 
		#This method takes in the following, order Number, Name of the type of production site and  
		#the node of the production site or end location order goes to next 
		#The for loop is finding the shortest distance between two nodes and comparing them to find the shortest path for the order to work
		#Add hungarian method in here if possible 
		smallestDist = 1000
		distHold = 0
		optimalLocation = 0
		
		for i in range(len(self.facilObj.lines[ProdSite])):
			distHold = self.graphViz.find_pathLength(self.facilObj.lines[ProdSite][i],endNode) 
			if distHold < smallestDist:
				smallestDist = distHold
				optimalLocation = self.facilObj.lines[ProdSite][i]
				
		return optimalLocation
	
	def findClosestWarehouse(self,prodLoc, materialType): #finding the warehouse closest to the production site being used 
		smallestDist = 1000
		distHold = 0
		optimalLocation = 0
		
		for i in range(len(self.facilObj.warehouses[materialType])):
			distHold = self.graphViz.find_pathLength(self.facilObj.warehouses[materialType][i],prodLoc) 
			if distHold < smallestDist:
				smallestDist = distHold
				optimalLocation = self.facilObj.warehouses[materialType][i]
				
		return optimalLocation
	
	
	'''
	{'L4': [89, 84, 168, 153, 26], 'L2': [82, 10, 174, 186, 185], 'L3': [1, 15, 3, 13, 32], 'L1': [119, 141, 181, 46, 25]}
	{'A': [37, 0], 'C': [5, 91], 'B': [208, 98], 'E': [140, 200], 'D': [20, 33], 'G': [68, 16], 'F': [165, 147], 'H': [111, 172]}
	'''

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
				'''
				change this for when the truck reaches its end node for delviery and record profit/loss here
				Have a similar statement for the trucks bringing stuff to a warehouse so that trucks can be released for new tasks 
				'''
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
		
		#this needs to be changed for part 2
		
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
		
	def findTruckForOrder(self,orderNumber,resourseLocation,materialNeeded,Task):
		'''
		Task = 1 if the truck is staying with the order the whole time
		Task = 2 if the truck is just delviering material 
		
		'''
		
		truckNum = -1
		'''
		this gets a new truck for any order so it can be moved
		'''
		#change for part two or remove 
		
		for i in self.truckObj.keys():
			#Checking to see if trucks are avaliable and they have enough capacity for the material that is needed
			if self.truckObj[i].isTruckInUse() == False and self.truckObj.getTruckCapacity() >= materialNeeded:
				self.truckObj[i].setTruckUsage(True)
				truckNum = i
				break
		
		
		if truckNum != -1: #this is true if a new truck was found for the 
			self.truckObj[truckNum].setNewOrderForTruck(orderNumber)
			if Task == 1:
				self.setNewTruckForOrder(truckNum,resourseLocation)
				
			else:
				self.set
			return truckNum
		else:
			
			return None
			
	
	
	
	def setNewTruckForOrder(self,truckNumber,resourseLocation): #Will move a truck to the warehouse loaction 
		
		#change this for part 2
		
		self.truckObj[truckNumber].setEndPosition(resourseLocation)

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
