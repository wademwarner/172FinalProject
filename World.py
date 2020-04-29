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

		self.red = (255,0,0)		#color of order when it is waiting to be produced 

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
		
		self.extraTruck = {}
		
		
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
					self.ProductionInfo[self.facilObj.lines[i][j]] = {'Capacity Max':100, 'Capacity Held':0, 'In Use': None}
					
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
				
				
				if self.orderInfo[i]['Finished']:
					print(i)
					print(self.orderInfo[i]['Order TIS'])
					
					del self.orderInfo[i]
					continue 
					'''
					The order has been delviered to its final location 
					Record the Profit/loss of the order  
					'''
				
				print(i)
				print(self.orderInfo[i])
				print(stepL-step)
				print(step)
				print(stepL)
				print(self.orderInfo[i]['Current Node'])
				print(self.order_sequence[i])
					
				currentProdLine = self.order_sequence[i][stepL-step][step]['Production Line']
				
				if self.orderInfo[i]['Order TIS'] == 0: #iterates through when the order if first created
					if self.ProductionInfo[currentProdLine]['Capacity Held'] >= self.order_sequence[i][stepL-step][step]['Material']:
						#start the order production
						self.orderInfo[i]['Order Process'] = 2
						
						if self.ProductionInfo[currentProdLine]['In Use'] == None:
							self.ProductionInfo[currentProdLine]['In Use'] = i
							
						self.getOrderTruck(i)
						
					else: #finding the warehouse closest ot the production site
						resLocation = self.findClosestWarehouse(self.orderInfo[i]['Current Node'], self.order_sequence[i][stepL-step][step]['Resource']) 
						self.orderInfo[i]['Order Process'] = 1
						
						if self.ProductionInfo[currentProdLine]['In Use'] == None:
							self.ProductionInfo[currentProdLine]['In Use'] = i
							
						self.findTruckForOrder(i,resLocation,self.order_sequence[i][stepL-step][step]['Material'],1)
						
						
				
					'''
					0-order was created and nothing has happened 
					1-order is waiting for material at a production site
					2-order is being produced
					3-order is moving to the next location 
					'''			
						
				elif self.orderInfo[i]['Order Process'] == 0:
					if self.ProductionInfo[currentProdLine]['Capacity Held'] >= self.order_sequence[i][stepL-step][step]['Material']:
						#start the order production
						self.orderInfo[i]['Order Process'] = 2
						self.getOrderTruck(i)
						
					else: #finding the warehouse closest to the production site
						resLocation = self.findClosestWarehouse(self.orderInfo[i]['Current Node'], self.order_sequence[i][stepL-step][step]['Resource']) 
						self.orderInfo[i]['Order Process'] = 1
						self.findTruckForOrder(i,resLocation,self.order_sequence[i][stepL-step][step]['Material'],1)
					
				elif self.orderInfo[i]['Order Process'] == 1:
					'''
					Animate the order location
					move the truck to the order location as red
					'''
					pygame.draw.rect(self.screen, self.red,(self.vtxPosit[self.orderInfo[i]['Current Node']][0]-2,
															self.vtxPosit[self.orderInfo[i]['Current Node']][1]-2,5,5))
					
					self.moveTruck(i,self.orderInfo[i]['Truck Used'],self.truckObj[self.orderInfo[i]['Truck Used']].getPosition(),
								self.truckObj[self.orderInfo[i]['Truck Used']].getEndPosition(),1)
					#order is waiting for material
					
					
				elif self.orderInfo[i]['Order Process'] == 2:
					'''
					animate the order as being produced as green
					incrament the process time down by one 
					
					Adda new method to see if material is needed or call it when we set orderStage to 2
					'''
					if (step +1) < (stepL-1):
						if self.ProductionInfo[self.order_sequence[i][stepL-step-1][step+1]['Production Line']]['Material Held'] < self.order_sequence[i][stepL-step-1][step+1]['Material']:
							'''
							send truck to get material 
							'''
							if i not in self.extraTruck.keys():
								resLocation = self.findClosestWarehouse(self.order_sequence[i][stepL-step-1][step+1]['Production Line'], 
																	self.order_sequence[i][stepL-step-1][step+1]['Resource']) 
								self.findTruckForOrder(i,resLocation,self.order_sequence[i][stepL-step-1][step+1]['Material'],2)
							self.moveExtraTruck(self.truckObj[self.extraTruck[i]].getPosition(),self.truckObj[self.extraTruck[i]].getEndPosition(),self.extraTruck[i],i)
				
					
					
					if self.ProductionInfo[currentProdLine]['In Use'] == i: #seeing if the productin line is being used by this order
						pygame.draw.rect(self.screen, self.green,(self.vtxPosit[self.orderInfo[i]['Current Node']][0]-2,
																self.vtxPosit[self.orderInfo[i]['Current Node']][1]-2,4,4))
						self.order_sequence[i][stepL-step][step]['Process Time'] -= 1
						
						
						
					elif self.ProductionInfo[currentProdLine]['In Use'] == None: #if the productin line is open, have this order use it
						self.ProductionInfo[currentProdLine]['In Use'] = i
						pygame.draw.rect(self.screen, self.green,(self.vtxPosit[self.orderInfo[i]['Current Node']][0]-2,
																self.vtxPosit[self.orderInfo[i]['Current Node']][1]-2,4,4))
						self.order_sequence[i][stepL-step][step]['Process Time'] -= 1
					
					
					
					if self.order_sequence[i][stepL-step][step]['Process Time'] == 0: #check to see if the order was completed or not
						#the order is done being produced here 
						self.ProductionInfo[currentProdLine]['In Use'] = None
						
						self.orderInfo[i]['Order Step'] += 1
						step += 1
						if step >= (stepL-1):
							self.truckObj[self.orderInfo[i]['Truck Used']].setEndPosition(self.orderInfo[i]['End Node'])
							self.orderInfo[i]['Order Process'] = 4
						else:
							self.truckObj[self.orderInfo[i]['Truck Used']].setEndPosition(self.order_sequence[i][stepL-step][step]['Production Line'])
							self.orderInfo[i]['Order Process'] = 3 
						#the order is done being produced at this line nd needs to move to the next production line or delivery location
						
						
						
					
					#order is being produced
					
				else:
					if step >= (stepL-1):
						self.orderInfo[i]['Order Process'] = 4
						self.moveTruck(i,self.orderInfo[i]['Truck Used'],self.orderInfo[i]['Current Node'],
									self.orderInfo[i]['End Node'],4)
					else:
						self.orderInfo[i]['Order Process'] = 3
						self.moveTruck(i,self.orderInfo[i]['Truck Used'],self.orderInfo[i]['Current Node'],
									self.order_sequence[i][stepL-step][step]['Production Line'],3)
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
							4-order if going to delivery location 
							
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
								'Truck Used':None, #
								'Finished':False,
								'Order Step':1, 
								'Order TIS':0,
								'Order Process':0}		
								#'Delivery Location':self.order_sequence[orderNum][ordL-2][2]['Production Line'], 
		
		
		

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

	def moveTruck(self,orderNumber,TruckNum,indexNode,end,orderStage):  #problems here likely means problems in the graph class path finding algorithm

		nextNode = self.graphViz.getNextNode(indexNode,end) #figure out the next node the truck is traveling to
	
		stepSize = float((self.graphViz.getLineLength(indexNode,nextNode)-1)/self.truckObj[TruckNum].getTimeOfAPath())

		#add in an ending condition here eventually 
		'''
		orderStage == 1 - move the truck to the order location after picking up material at a warehouse
			Need to say material is at production line
			
		orderStage == 2 - See if the truck needs to be moved to the next order 
			Maybe not animate in here yet, have a method to call this 
			
		orderStage == 3 - move the order to the next production site 
		
		orderStage == 4 - move the order to the end location 
		'''
		
		#self.moveTruckToOrderDest(orderNumber, indexNode, TruckNum)
				
		if orderStage == 1:
			
			if self.graphViz.isLineStraight(indexNode,nextNode): #animation for if the line is straight

			
				self.moveTruckStright(indexNode,nextNode,TruckNum)
		
			else: #moving the truck along a curved line
				
				self.moveTruckCurved(stepSize,indexNode,nextNode,TruckNum)
		
		
		
		else:
			if self.graphViz.isLineStraight(indexNode,nextNode): #animation for if the line is straight
	
				self.moveTruckStright(indexNode,nextNode,TruckNum)
				pygame.draw.rect(self.screen, self.blue,(self.truckObj[TruckNum].getPosition_x_Coordinates()-2,
													self.truckObj[TruckNum].getPosition_y_Coordinates()-2,4,4))
			
			else: #moving the truck along a curved line
				
				self.moveTruckCurved(stepSize,indexNode,nextNode,TruckNum)
				pygame.draw.rect(self.screen, self.blue,(self.truckObj[TruckNum].getPosition_x_Coordinates()-2,
													self.truckObj[TruckNum].getPosition_y_Coordinates()-2,4,4))
			
		if self.truckObj[TruckNum].getTimeLeftOnPath() > self.truckObj[TruckNum].getTimeOfAPath(): #reset the next node if it done on path between vertex's
			
			stepL = len(self.order_sequence[orderNumber])
			step = self.orderInfo[orderNumber]['Order Step']
			
			currentProdLine = self.order_sequence[orderNumber][stepL-step][step]['Production Line']
				
				
			
			
			
			if orderStage == 1:
				'''
				fix this 
				'''
				
				
				if nextNode == self.truckObj[TruckNum].getEndPosition():
					if self.orderInfo[orderNumber]['Current Node'] == nextNode: 
						
						self.orderInfo[orderNumber]['Order Process'] = 2
						print('we are producing stuff now')
						
						if self.ProductionInfo[currentProdLine]['In Use'] == None:
							self.ProductionInfo[currentProdLine]['In Use'] = orderNumber
						
							
						
						materialLeft = self.truckObj[TruckNum].getTruckCapacity() - self.order_sequence[orderNumber][stepL-step][step]['Material']
						self.ProductionInfo[currentProdLine]['Capacity Held'] += materialLeft
						
						
						
					else:	#moving the truck from the warehouse to the production site 
						self.truckObj[TruckNum].setEndPosition(self.orderInfo[orderNumber]['Current Node'])
						print('the truck is giong to the order with material')
		
					
			elif orderStage == 3: #updating the nodes of the truk if it is moving to a new production facility
				if nextNode == self.order_sequence[orderNumber][stepL-step][step]['Production Line']: #checks to see if the order is at the end location
					'''
					order is at the next production site 
					'''
					if self.ProductionInfo[currentProdLine]['Capacity Held'] >= self.order_sequence[orderNumber][stepL-step][step]['Material']: 
					#checks to see if material needed is there and if the production facility is able to produce cars
					
						self.orderInfo[orderNumber]['Order Process'] = 2 
						#order now being produced
						
						
						
						if self.ProductionInfo[currentProdLine]['In Use'] == None:
							self.ProductionInfo[currentProdLine]['In Use'] = orderNumber
						
						materialLeft = self.truckObj[TruckNum].getTruckCapacity() - self.order_sequence[orderNumber][stepL-step][step]['Material']
						self.ProductionInfo[currentProdLine]['Capacity Held'] += materialLeft
						
						
						#something to see if more material is needed at the next stage ###
						
						self.orderInfo[orderNumber]['Current Node'] = self.order_sequence[orderNumber][stepL-step][step]['Production Line'] 
						#set the order location to the new production line
						self.truckObj[TruckNum].setEndPosition(self.orderInfo[orderNumber]['Current Node'])
					else:
						self.orderInfo[orderNumber]['Order Process'] = 1
				else:
					self.orderInfo[orderNumber]['Current Node'] = nextNode

					
			elif orderStage == 4:
				if nextNode == self.orderInfo[orderNumber]['End Node']: #the order is at its end location 
					self.orderInfo[orderNumber]['Finished'] = True
					self.orderInfo[orderNumber]['Truck Used'] = None
					self.truckObj[TruckNum].setTruckUsage(False)
				else:
					self.orderInfo[orderNumber]['Current Node'] = nextNode
					
			if self.orderInfo[orderNumber]['Truck Used'] != None: #if the order is still in productin, set new positions for the order and truck	
				self.truckObj[TruckNum].setNewPosition(nextNode)
						
					
				self.truckObj[TruckNum].setPosition_x_Coordinates(float(self.vtxPosit[nextNode][0]))
				self.truckObj[TruckNum].setPosition_y_Coordinates(float(self.vtxPosit[nextNode][1]))
				
				self.truckObj[TruckNum].setTimeOfaNewPath(float(self.graphViz.getTime(self.truckObj[TruckNum].getPosition(),
																	self.graphViz.getNextNode(self.truckObj[TruckNum].getPosition(),self.truckObj[TruckNum].getEndPosition()))))	
						
		

			'''
			ProductionInfo = {'Capacity Max':100, 'Capacity Held':0, 'In Use': Order Number}
			
			order_sequence = [{(ordL-i):{'Process Time': ,'Material':,'Resource':,'Production Line': 0}}]
			
			orderInfo =	{'Current Node':,'End Node':,'Truck Used':None,'Delivery Location','Finished':False,'Order Step':1,'Order TIS':0,'Order Process':0}
			'''
	
	def moveExtraTruck(self,indexNode,end,TruckNum,orderNum):#animating and mving the truck transporting material to production sites
		nextNode = self.graphViz.getNextNode(indexNode,end) #figure out the next node the truck is traveling to
	
		stepSize = float((self.graphViz.getLineLength(indexNode,nextNode)-1)/self.truckObj[TruckNum].getTimeOfAPath())
		#animating the movement
		stepL = len(self.order_sequence[orderNum])
		step = self.orderInfo[orderNum]['Order Step']
		
		if self.graphViz.isLineStraight(indexNode,nextNode): #animation for if the line is straight
	
			self.moveTruckStright(indexNode,nextNode,TruckNum)
		
		else: #moving the truck along a curved line
				
			self.moveTruckCurved(stepSize,indexNode,nextNode,TruckNum)
			
		#see if truck is at a new node
		if self.truckObj[TruckNum].getTimeLeftOnPath() > self.truckObj[TruckNum].getTimeOfAPath():
			
			if nextNode == self.order_sequence[orderNum][stepL-step][step]['Production Line']: #material at production site
				currentProdLine = self.order_sequence[orderNum][stepL-step-1][step+1]['Production Line']
				
				if self.ProductionInfo[currentProdLine]['Capacity Held'] >= self.order_sequence[orderNum][stepL-step][step]['Material']: 
				#checks to see if material needed is there and if the production facility is able to produce cars
				
					
					
					if self.ProductionInfo[currentProdLine]['In Use'] == None:
						self.ProductionInfo[currentProdLine]['In Use'] = orderNum
					
					materialLeft = self.truckObj[TruckNum].getTruckCapacity() - self.order_sequence[orderNum][stepL-step-1][step+1]['Material']
					self.ProductionInfo[currentProdLine]['Capacity Held'] += materialLeft
					
					truckID = self.extraTruck[orderNum]
					del self.extraTruck[orderNum]
					self.truckObj[truckID].setTruckUsage(False)
					
			
			elif nextNode == self.truckObj[orderNum].getEndPosition(): #material is at the warehouse
				
				self.truckObj[orderNum].setEndPosition(currentProdLine)
			
			self.truckObj[TruckNum].setNewPosition(nextNode)
						
					
			self.truckObj[TruckNum].setPosition_x_Coordinates(float(self.vtxPosit[nextNode][0]))
			self.truckObj[TruckNum].setPosition_y_Coordinates(float(self.vtxPosit[nextNode][1]))
			
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
		
		#blits the truck to thr correct position on the screen
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
		
	
	def getOrderTruck(self,orderNumber):
		'''
		This method gets a new truck for an order if the first production site already had material at it
		'''
		truckNum = -1

		for i in self.truckObj.keys():
			#Checking to see if trucks are avaliable and they have enough capacity for the material that is needed
			if self.truckObj[i].isTruckInUse() == False:
				self.truckObj[i].setTruckUsage(True)
				truckNum = i
				self.orderInfo[orderNumber]['Truck Used'] = truckNum
				break
		
		
		if truckNum != -1: #this is true if a new truck was found for the 
			self.truckObj[truckNum].setNewOrderForTruck(orderNumber)
			self.setNewTruckForOrder(truckNum,self.orderInfo[orderNumber]['Current Node'])
			
		else:
			pass
	
	def findTruckForOrder(self,orderNumber,resourseLocation,materialNeeded,Task):
		'''
		This gets a new truck for any order so the material is moved from the warehouse to the production site
		Task = 1 if the truck is staying with the order the whole time
		Task = 2 if the truck is just delviering material 
		
		'''

		truckNum = -1
		
		for i in self.truckObj.keys():
			#Checking to see if trucks are avaliable and they have enough capacity for the material that is needed
			if self.truckObj[i].isTruckInUse() == False and self.truckObj[i].getTruckCapacity() >= materialNeeded:
				self.truckObj[i].setTruckUsage(True)
				truckNum = i
				break
		
		
		if truckNum != -1: #this is true if a new truck was found for the 
			self.truckObj[truckNum].setNewOrderForTruck(orderNumber)
			if Task == 1:
				self.setNewTruckForOrder(truckNum,resourseLocation)
				self.orderInfo[orderNumber]['Truck Used'] = truckNum
			else:	#assigning a truck moving to delvier stuff without the order 
				self.extraTruck[orderNumber] = truckNum
				self.setNewTruckForOrder(truckNum,resourseLocation)
			
		else:
			if Task == 1:
				self.orderInfo[orderNumber]['Truck Used'] = None
			
	
	
	
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
			pygame.draw.rect(self.screen, self.pple,(self.vtxPosit[vertex][0]-2,self.vtxPosit[vertex][1]-2,4,4)) #if you want nodes to be a different color
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
