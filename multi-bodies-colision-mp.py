'''
	SIMULADOR DE N-CORPOS INTERAGENTES GRAVITACIONALMENTE: "FORMAÇÃO DE ESTRELAS"
	
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random
import numpy as np
import multiprocessing as mp
import tqdm as tqdm

print("Number of cpu : ", mp.cpu_count())

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
		#print("tempo: ", global_time, " ; Particula criada: ", "massa: ",self.m, "; (",self.x,",",self.y,")", " ; v: (", self.vx, ",", self.vy, ")")
	
	def move(self):
		self.vx += self.Fx / self.m * dt
		self.vy += self.Fy / self.m * dt
		self.x += self.vx*dt
		self.y += self.vy*dt
		self.Fx = 0
		self.Fy = 0

	def force(self, P, q):
		R = (np.sqrt((q.x - P.x)**2 + (q.y - P.y)**2))
		bateu = False
		if R < self.m/5:
			self.colision(P, q)
			bateu = True
		if R > 0 and not bateu:
			self.Fx = G*self.m * P.m * (self.x - P.x)/R**2
			self.Fy = G*self.m * P.m * (self.y - P.y)/R**2
		
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


def calcular_forcas():
	global particulas
	q = particulas[isss]
	for p in particulas:
		if q != p:
			p.force(p, q)


def animate(U):
	global particulas, global_time
	ax.clear()
	ax.set_xlim([-space_size-10, space_size+10])
	ax.set_ylim([-space_size-10, space_size+10])
	global_time = round(U*dt, 2)
	ax.set_title("number of particles: {} ; time: {}".format(len(particulas), global_time))
	
	processes = []
	for iss in range(len(particulas)):
		global isss
		isss = iss
		processes.append(mp.Process(target=calcular_forcas))
	
	for process in processes:
		process.start()
	for process in processes:
		process.join()

	for p in particulas:
		p.verify_out_of_limits()
		p.move()
		p.show()

if __name__ == '__main__':
	fig, ax = plt.subplots()
	particulas = []
	print("Gerando partículas:")
	for i in tqdm.trange(n_particles):
		particulas.append(Mass(random.uniform(0,mass_interval), random.uniform(-space_size, space_size), random.uniform(-space_size, space_size), random.uniform(-speed_interval, speed_interval), random.uniform(-speed_interval, speed_interval)))
	print("Todas as partículas foram geradas")

	ani = animation.FuncAnimation(fig, animate, total_frames, interval = 1, repeat= True)
	plt.show()
