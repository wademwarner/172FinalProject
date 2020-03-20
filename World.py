from  Classes.AbstractWorld import AbstractWorld
from Classes.Graph import Graph

import pygame
pygame.font.init() 

class World(AbstractWorld):
	
	graphViz = Graph()
	
	def __init__(self):
		AbstractWorld.__init__(self)
		
		self.height = 600
		self.width = 800
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.black = (0,0,0)
		self.blue = (0,0,255)
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


	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):

		'''
		This will give you a list of ALL cars which are in the system
		'''
		trucks = self.getInitialTruckLocations()
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t)) 

		'''
		We will run a simulation where "t" is the time index
		'''
		for t in xrange(initialTime,finalTime):	
			print "\n\n Time: %02d:%02d"%(t/60, t%60)
			# each minute we can get a few new orders
			newOrders = self.getNewOrdersForGivenTime(t)
			print "New orders:"  
			for c in newOrders:
				print c
			
			text = self.font.render("Time: %02d:%02d"%(t/60, t%60), True, (255, 0, 0), (255, 255, 255))
			textrect = text.get_rect()
			textrect.centerx = 100
			textrect.centery = 30
			self.screen.fill((255, 255, 255))
			self.screen.blit(text, textrect)
 
			
			'''
			You should plot the vetricies, edges and cars and customers
			Each time, cars will move and you should visualize it 
			accordingly
			'''
     
			pygame.display.update()	
			for event in pygame.event.get():
				pass   
			self.clock.tick(fps)
  
  	'''WMW'''
	def changeToViz(self,verts): #takes x and y in vertices and imports as vert to be graphed
			
		for i in verts:
			self.vID.append(i)
		print self.vID
		for i in range(len(self.vID)):
			self.vID[i][1] = int(self.vID[i][1]*self.width)
			
		for i in range(len(self.vID)):
			self.vID[i][2] = int(self.vID[i][2]*self.width)
			
		for i in self.vID:
			self.vtxPosit[i[0]] = (i[1],i[2])
			
		

	def appearances(self): #put vertices on display
		for vertex in self.vtxPosit: #every vertex
			pygame.draw.rect(self.screen, self.blue,(self.vtxPosit[vertex][0]-2,self.vtxPosit[vertex][1]-2,4,4))	
		for edge in self.neighborPosit:
			pygame.draw.aaline(self.screen,self.blue,edge[0],edge[1],4)
			
		pygame.display.update()
		pygame.time.delay(5000)
		#get neighbors of vertices and draw a line
			
		
	
		
	def drawGraph(self,node,node_neighbors):
			
		if node_neighbors != None:		
			vertPoint = self.vtxPosit[node]
	
			for i in node_neighbors:
				#print(node, "->", i)
				#print("######")
				vertNeighbor = self.vtxPosit[i] #[node_neighbors[i]
				self.neighborPosit.append((vertPoint, vertNeighbor)) #might need to be fixed for later updates, this just lists all edge points for visualization
				#self.lineList.append(lineCreate)


		
		