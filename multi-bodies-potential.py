'''
	SIMULADOR DE N-CORPOS INTERAGENTES GRAVITACIONALMENTE: "FORMAÇÃO DE ESTRELAS"
	
	PROPOSTA: CALCULAR O POTENCIAL MÉDIO E EVOLUIR TEMPORALMENTE, RECALCULANDO O POTENCIAL A CADA CICLO

'''



import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random
import numpy as np


dt = 0.1
space_size = 500
n_particles = 100
mass_interval = 50
speed_interval = 30
G = 1
total_time = 1000
total_frames = int(total_time/dt)
global_time = 0

class Mass:
	def __init__(self, mass, x, y, vx, vy):
		global global_time
		self.m = mass
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.Fx = 0
		self.Fy = 0
		print("tempo: ", global_time, " ; Particula criada: ", "massa: ",self.m, "; (",self.x,",",self.y,")", " ; v: (", self.vx, ",", self.vy, ")")
	
	def move(self):
		self.vx += self.Fx * dt #/self.m
		self.vy += self.Fy * dt #/self.m
		self.x += self.vx*dt
		self.y += self.vy*dt
		self.Fx = 0
		self.Fy = 0

	def force(self, phi):
		bateu = False
		'''if R < self.m/5:	# ADICIONAR VERIFICAÇÃO DE COLISÃO
			self.colision(P, q)
			bateu = True
		if R > 0 and not bateu:
			self.Fx = G*self.m * P.m * (self.x - P.x)/R**2
			self.Fy = G*self.m * P.m * (self.y - P.y)/R**2
		'''
		self.Fx = phi/self.x
		self.Fy = phi/self.y

	def show(self):
		ax.plot(self.x, self.y, 'ob', markersize=self.m/5)

	def colision(self, P, q):
		global particulas
		for i, obj in enumerate(particulas):
			if obj == P:
				particulas.pop(i)
			elif obj == q:
				particulas.pop(i)
		particulas.append(Mass((self.m + P.m)/2, self.x, self.y, (self.vx*self.m+P.vx*P.m)/(self.m + P.m), (self.vy*self.m+P.vy*P.m)/(self.m + P.m)))	# m/2 pelo bug

	def verify_out_of_limits(self):
		if np.sqrt(self.y**2) >= space_size:
			self.vy = -self.vy
		elif np.sqrt(self.x**2) >= space_size:
			self.vx = -self.vx

def campo_medio(particulas):
	phi = 0
	M = 0
	for p in particulas:
		M += p.m
		R = np.sqrt((p.x)**2 + (p.y)**2)
		phi_p = G*p.m/R
		phi += phi_p
	phi = phi/M
	return phi


def animate(U):
	global particulas, global_time
	ax.clear()
	ax.set_xlim([-space_size-10, space_size+10])
	ax.set_ylim([-space_size-10, space_size+10])
	global_time = round(U*dt, 2)
	ax.set_title("number of particles: {} ; time: {}".format(len(particulas), global_time))
	
	phi = campo_medio(particulas)
	
	for p in particulas:
		p.force(phi)
		p.verify_out_of_limits()
		p.move()
		p.show()

fig, ax = plt.subplots()

particulas = []
for i in range(n_particles):
	particulas.append(Mass(random.uniform(0,mass_interval), random.uniform(-space_size, space_size), random.uniform(-space_size, space_size), random.uniform(-speed_interval, speed_interval), random.uniform(-speed_interval, speed_interval)))

ani = animation.FuncAnimation(fig, animate, total_frames, interval = 1, repeat= True)
plt.show()
