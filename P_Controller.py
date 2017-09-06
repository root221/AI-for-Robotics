# -----------
# User Instructions
#
# Implement a P controller by running 100 iterations
# of robot motion. The desired trajectory for the 
# robot is the x-axis. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau * crosstrack_error
#
# Note that tau is called "param" in the function
# below.
#
# Your code should print output that looks like
# the output shown in the video. That is, at each step:
# print myrobot, steering
#
# Only modify code at the bottom!
# ------------
 
import random
import numpy as np
import matplotlib.pyplot as plt
from math import *
#import proportional

# ------------------------------------------------
# 
# this is the Robot class
#

class robot(object):
    def __init__(self, length=20.0):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        """
        Sets a robot coordinate.
        """
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        """
        Sets the noise parameters.
        """
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        """
        Sets the systematical steering drift parameter
        """
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        """
        steering = front wheel steering angle, limited by max_steering_angle
        distance = total distance driven, most be non-negative
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # make a new copy
        res = robot()
        res.length = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            res.x = self.x + distance2 * np.cos(self.orientation)
            res.y = self.y + distance2 * np.sin(self.orientation)
            res.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * np.pi)
            res.x = cx + (np.sin(res.orientation) * radius)
            res.y = cy - (np.cos(res.orientation) * radius)

        return res

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)

############## ADD / MODIFY CODE BELOW ####################
# ------------------------------------------------------------------------
#
# run - does a single control run

def run(params):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0 # motion distance is equalt to speed (we assume time = 1)
    N = 100 
    myrobot.set_steering_drift(10.0 / 180 * pi)
    err = 0.0

    crosstrack_error = myrobot.y
    int_crosstrack_err = 0
    for i in range(N * 2):
        diff_crosstrack_error = myrobot.y - crosstrack_error  
        crosstrack_error = myrobot.y
        int_crosstrack_err += myrobot.y
        steer = -params[0] * crosstrack_error - params[1] * diff_crosstrack_error - params[2] * int_crosstrack_err
        myrobot = myrobot.move(steer,1)

        if i >= N:
            err += (crosstrack_error ** 2)

    return err / float(N)



def twiddle(tol=0.001):
    t = 0
    p = [0,0,0]
    dp = [1,1,1]
    best_err = run(p)
    
    while sum(dp) > tol:
        for i in range(len(p)):
                p[i] += dp[i]
                err = run(p)
                if best_err > err:
                    best_err = err
                    dp[i] *= 1.1

                else:
                    p[i] -= dp[i] * 2.0
                    err = run(p)
                    if best_err > err:
                        best_err = err
                        dp[i] *= 1.1

                    else:
                        p[i] += dp[i]
                        dp[i] *= 0.9
        t += 1
        print(t,p,best_err)
    return p


params = twiddle()



