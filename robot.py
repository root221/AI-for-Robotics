from math import *
import random

landmarks = [[20.0,20.0],
			 [80.0,80.0],
			 [20.0,80.0],
			 [80.0,20.0]]

world_size = 100.0

class robot:
	
	def __init__(self):
		self.x = random.random() * world_size
		self.y = random.random() * world_size
		self.orientation = random.random() * 2 * pi
		self.forward_noise = 0.0
		self.turn_noise = 0.0
		self.sense_noise = 0.0

	def set(self,new_x,new_y,new_orientation):
		if new_x < 0 or new_x >= world_size:
			raise ValueError,'X coordinate out of bound'
		if new_y < 0 or new_y >= world_size:
			raise ValueError,'Y coordinate out of bound'
		if new_orientation < 0 or new_orientation >= 2 * pi:
			raise ValueError,'orientation must be in [0,2pi]'
		self.x = float(new_x)
		self.y = float(new_y)
		self.orientation = float(new_orientation)

	def set_noise(self,new_f_noise,new_t_noise,new_s_noise):
		self.forward_noise = float(new_f_noise)
		self.turn_noise = float(new_t_noise)
		self.sense_noise = float(new_s_noise)

	def move(self,turn,forward):
		if forward < 0:
			raise ValueError,'Robot cant move backwards'
		# turn and add randomness to the turning command
		orientation = self.orientation + float(turn) + random.gauss(0.0,self.turn_noise)
		orientation %= (2 * pi)

		# move and add randomness to the motion command
		dist = forward + random.gauss(0.0,self.forward_noise)
		x = self.x + cos(orientation) * dist
		y = self.y + sin(orientation) * dist
		x %= world_size
		y %= world_size
		res = robot()
		res.set(x,y,orientation)
		res.set_noise(self.forward_noise,self.turn_noise,self.sense_noise)
		return res


	def sense(self):
		Z = []
		for i in range(len(landmarks)):
			dist = sqrt((self.x - landmarks[i][0])**2 + (self.y - landmarks[i][1]) ** 2)
			# random.gauss(mu,sigma)
			dist += random.gauss(0.0,self.sense_noise)
			Z.append(dist)
		return Z
	#def __repr__(self):
	#	return repr(self.x)




	def measurement_prob(self,measurement):
		prob = 1.0
		for i in range(len(landmarks)):
			dist = sqrt((self.x - landmarks[i][0])**2 + (self.y - landmarks[i][1]) ** 2)
			prob *= self.Gaussian(dist,self.sense_noise,measurement[i])
		return prob

	def Gaussian(self,mu,sigma,x):
		# calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
		return (1/sqrt(2*pi*sigma**2)) * exp((-0.5)* ((x-mu)**2 / sigma**2))



	def __repr__(self):
		return '[x=%s y=%s orientation=%s]' % (str(self.x),str(self.y),str(self.orientation))

def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))




myrobot = robot()
myrobot = myrobot.move(0.1,5.0)
Z = myrobot.sense()


T = 10
N = 1000
p = []

for i in range(N):
	x = robot()
	x.set_noise(0.05,0.05,5.0)
	p.append(x)

for t in range(T):
	myrobot = myrobot.move(0.1, 5.0)
	p2 = []
	for partical in p:
		p2.append(partical.move(0.1,5.0))
	p = p2

	w = []
	for partical in p:
		w.append(partical.measurement_prob(Z))


	p3 = []
	# normalize 
	s = sum(w)
	alpha = [x/s for x in w]

	for i in range(N):
		index = 0
		s = 0
		beta = random.random()
		while s < beta:
			s = s + alpha[index]
			index = index + 1

		p3.append(p[index-1])
				
	p = p3
	if t == 9:
		print myrobot
		for i in p:
			print(i)
		#print eval(myrobot,p)