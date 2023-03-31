import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random

dt = 0.01

class Mass:
	def __init__(self, mass, x, y, vx, vy):
		self.m = mass
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		print("Particula criada: ", "massa: ",self.m, "; (",self.x,",",self.y,")", " ; v: (", self.vx, ",", self.vy, ")")
	
	def move(self):
		self.vx += self.Fx / self.m * dt
		self.vy += self.Fy / self.m * dt
		self.x += self.vx*dt
		self.y += self.vy*dt
		self.Fx = 0
		self.Fy = 0

	def force(self, P):
		R = ((self.x - P.x)**2 + (self.y - P.y)**2)**(3/2)
		self.Fx = self.m * P.m * (self.x - P.x)/R
		self.Fy = self.m * P.m * (self.y - P.y)/R
		
	def show(self):
		ax.plot(self.x, self.y, 'ob', markersize=3)
	
def animate(U):
	global particulas
	ax.clear()
	ax.set_xlim([-50, 50])
	ax.set_ylim([-50, 50])
	
	for p in particulas:
		for q in particulas:
			if p != q:
				p.force(q)
	for p in particulas:
		p.move()
		p.show()

fig, ax = plt.subplots()

particulas = []

particulas = []
for i in range(100):
	particulas.append(Mass(random.uniform(0,10), random.uniform(-50, 50), random.uniform(-50, 50), random.uniform(-5, 5), random.uniform(-5, 5)))

ani = animation.FuncAnimation(fig, animate, 100, interval = 1, repeat= True)
plt.show()
