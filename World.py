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
		self.pple = (255,0,255)
		self.clock = pygame.time.Clock()
		self.font  = pygame.font.SysFont('Comic Sans MS', 30)
		'''wmw'''
		self.x_graphic = []
		self.y_graphic = []
		self.vID = []
		self.vtxPosit = {}
		self.neighborRelDict ={} #dictionary for the direct neighbor key for vertex
		self.neighborPositDict = {} 
		self.rectList = []
		self.neighborPosit = []
		self.prevNode = []
		self.line_CURV = []
		self.line_graph = []
		self.line_list = {}
		self.graphViz = x
		
		self.orders = {}
		self.bestPath = []
		self.bestPathConvCart = {}
		self.order_check ={}
		self.order_len = []
		self.len_ord_path = {}
		self.check_order_stat = {}
		self.endOfOrder = {}
		
		self.trucks = {}
		self.truck_on_order = {}
		self.trs = {} #truck run status (0 if open, 1 if headed to pickup, 2 if capacitated
		self.truckPathList = {}
		self.trd = {} #truck remaining distance to demand vertex
		self.vtxHasTruck = {} #if a truck has reached key vertex
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):

		'''
		This will give you a list of ALL cars which are in the system
		'''
		trucks = self.getInitialTruckLocations()
		print(trucks[0])
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t))
			findNum = re.findall(r'\d+', str(t)) #helps get the starting vertex for trucks
			listNum = list(map(int,findNum))
			self.trucks[i] = listNum[1]
			self.trs[i] = 0
		#print(self.trucks)
		'''
		We will run a simulation where "t" is the time index
		'''
		oct =-1 #order count
		for t in xrange(initialTime,finalTime):	
			print "\n\n Time: %02d:%02d"%(t/60, t%60)
			# each minute we can get a few new orders
			newOrders = self.getNewOrdersForGivenTime(t) #list of new orders
			print "New orders:" 
			for c in newOrders:
				if len(newOrders) > 0:
					oct += 1
					print c
					self.orders[oct]=self.getRandVerts()
					print("Shipment from -> to: ", self.orders[oct][0],self.orders[oct][1])
					self.bestPath=self.graphViz.find_path(self.orders[oct][0],self.orders[oct][1])
					self.endOfOrder[oct] = self.orders[oct][1]
					self.bestPathConvCart[oct] = self.realVertexConv(self.bestPath)
					print("Best path travels on vertices: ",self.bestPathConvCart[oct])
					print("on nodes: ", self.bestPath)
					pygame.draw.rect(self.screen, (0,255,255),(self.bestPathConvCart[oct][0][0]-2,self.bestPathConvCart[oct][0][1]-2,7,7)) #signal teal that new order has been placed
					#self.order_check[c] = self.orders[c][1]
					self.len_ord_path[oct] = len(self.bestPath)
					self.order_len.append(self.len_ord_path[oct])
					self.check_order_stat[oct] = 1
					min = 10000
					min_truck = None
					min_path = None
					for i in range(0,len(self.trucks)):
						try:
							len_sp = len(self.graphViz.find_path(self.trucks[i],self.orders[oct][1]))
							print(self.trucks[i],self.orders[oct][0])
							print(len_sp)
						except KeyError:
							continue
						try:
							if len_sp <= min:
								min, min_truck, min_path = len_sp, i, self.graphViz.find_path(self.trucks[i],self.orders[oct][0])
						except KeyError:
							continue
					self.truckPathList[min_truck] = min_path
					self.trs[min_truck] = 1
					self.truck_on_order[oct] = self.trucks[min_truck]
					self.trd[min_truck] = min
					print("Truck Leaving: " ,min_truck, " on a path ", min_path, " for order # ", oct, " at a location of ", self.trucks[min_truck])
					pygame.draw.rect(self.screen, self.pple,(self.vtxPosit[self.trucks[min_truck]][0]-2,self.vtxPosit[self.trucks[min_truck]][1]-2,7,7)) #should draw truck when it is called on by its nearest calling vertex
				else:
					pass
			
			for truck in range(0,len(self.trs)):
				#print(self.trs)
				#print(self.trs[truck])
				try:
					if self.trs[truck] == 0:
						continue
					elif self.trs[truck] == 1:
						if self.trd[truck] == 0:
							self.trs[truck] == 2
							self.trucks[truck] = self.truckPathList[truck][len(self.truckPathList[truck])-1]
							print("Truck reached destination of: ", self.trucks[truck])
							continue
						self.trd[truck] -= 1
						self.trucks[truck] = -1 #in use, no native vertex at this point
						#print(self.truckPathList[truck][len(self.truckPathList[truck])-self.trd[truck]])
						#print(len(self.truckPathList[truck]),self.trd[truck])
						#print(self.truckPathList[truck])
						print(truck, len(self.truckPathList[truck]), self.trd[truck],len(self.truckPathList[truck])-self.trd[truck],self.truckPathList[truck])
						vertexTruckCurrent = self.truckPathList[truck][len(self.truckPathList[truck])-self.trd[truck]]
						print(vertexTruckCurrent)
						#print(vertexTruckCurrent)
						vtxTC_posit = self.vtxPosit[vertexTruckCurrent]
						print(vtxTC_posit[0],vtxTC_posit[1],"truck: ",truck)
						pygame.draw.rect(self.screen, self.green,(vtxTC_posit[0],vtxTC_posit[1],7,7)) #draw up to date truck location prior to pick-up
						#pygame.display.update()
					else:
						continue
				except KeyError:
					continue
			
			for truck in range(0,len(self.trd)):
				try:
					if self.trd[truck] == 0:
						self.vtxHasTruck[self.truckPathList[truck][len(self.truckPathList[truck])-1]] = True
						self.trs[truck] = 2
				
					else:
						continue
				except KeyError:
					continue
			
			print(oct)		
			try:
				if oct <= 0:
					pass
				else:
					for ord in range(0,len(self.check_order_stat)):
						#print(self.check_order_stat,"/",self.len_ord_path)
						if self.vtxHasTruck[self.orders[ord][1]] == False:
							continue
						if self.check_order_stat[ord] == self.len_ord_path[ord]-1:
							self.trucks[ord] = self.endOfOrder[ord]
							continue
						else:
							whereOnPath = self.check_order_stat[ord]
							#print(self.bestPathConvCart)
							#print(self.bestPathConvCart[0])
							print(ord, whereOnPath, 0)
							pygame.draw.rect(self.screen, self.red,(self.bestPathConvCart[ord][whereOnPath][0]-2,self.bestPathConvCart[ord][whereOnPath][1]-2,7,7))
							self.check_order_stat[ord] += 1
							print("Order # " + str(ord) + " being processed by truck # " + str(self.trucks[ord]) + " currently at " + str(self.bestPathConvCart[ord][whereOnPath][0]-2) , str(self.bestPathConvCart[ord][whereOnPath][1]-2))		
				
			except KeyError:
				pass
			
			pygame.display.update()
			#pygame.time.delay(2500)
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
			self.appearances()
 
			
			'''
			You should plot the vetricies, edges and cars and customers
			Each time, cars will move and you should visualize it 
			accordingly
			'''
     
			for event in pygame.event.get():
				pass   
			self.clock.tick(fps*100)
  
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
			pygame.draw.rect(self.screen, self.blue,(self.vtxPosit[vertex][0]-2,self.vtxPosit[vertex][1]-2,4,4))	
		for edge in self.line_list: #self.neighborPosit
			for i in range(0,len(self.line_list[edge])-2):
				pygame.draw.line(self.screen,self.blue,self.line_list[edge][i],self.line_list[edge][i+1],3)
							
		pygame.display.update()
		#get neighbors of vertices and draw a line
			
		
	
		
	def drawGraph(self,node,node_neighbors):
			
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
				if list_curV == 152:
					continue
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
			if a == b:
				self.getRandVerts()
			else:
				return self.vID[a][0],self.vID[b][0]
			
	def realVertexConv(self,list_vtx):
		newList = []
		for vtx in list_vtx:
			newList.append(self.vtxPosit[vtx])
		return newList