import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Mass:
	def __init__(self, mass, x, y, vx, vy):
		self.m = mass
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

	
	def force(self, Fx, Fy, dt):
		self.vx += Fx / self.m * dt
		self.vy += Fy / self.m * dt
		self.x += self.vx*dt
		self.y += self.vy*dt
	
	def force2(self, P):
		R = ((self.x - P.x)**2 + (self.y - P.y)**2)**(3/2)
		
		Fx = self.m * P.m * (self.x - P.x)/R
		Fy = self.m * P.m * (self.y - P.y)/R
		
		self.force(-Fx, -Fy, 0.001)
		P.force(Fx, Fy, 0.001)
		
	def show(self):
		ax.plot(self.x, self.y, 'or', markersize=2)
	
	
def animate(U):
	#ax.clear()
	ax.set_xlim([-20, 30])
	ax.set_ylim([-20, 20])
	
	M1.force2(M2)
	if U%10 == 0:
		M1.show()
		M2.show()

fig, ax = plt.subplots()

M1 = Mass(1000000, 0, 0, 0, 0)
M2 = Mass(500, 25, 0, -0, -120)

ani = animation.FuncAnimation(fig, animate, 100, interval = 1, repeat= True)

plt.show()
	
	

