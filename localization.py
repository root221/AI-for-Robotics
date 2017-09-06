p=[0.2, 0.2, 0.2, 0.2, 0.2]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
motions = [1,1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    q = []
    for i in range(5):
        if world[i] == Z:
            q.append(p[i] * pHit)
        else:
            q.append(p[i] * pMiss)
    s = sum(q)
    q = [x/s for x in q]
    
    return q

#for measurement in measurements:
#    p = sense(p,measurement)

# p is the input distribution
# U is the number of grid cells that the robot is moving to the right or to the left
# return the new distribution Q after the move
def move(p,U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q

#p = move(p,1)
#p = move(p,1)
#for i in range(1000):
#    p = move(p,1)

# compute the posterior distribution if the robot first senses red
#p = sense(p,'red')
#p = move(p,1)
#p = sense(p,'green')
#p = move(p,1)

for k in range(len(measurements)):
    print(k)
    p = sense(p,measurements[k])
    p = move(p,motions[k])
    
print(p)
