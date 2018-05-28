"""
Institution : DTU
Course      : Master Thesis Project
Date        : 20-Jan-2018
Author      : Jaime Liew - S141777
Email       : Jaimeliew1@gmail.com
Description : Demonstration if individual pitch control. This script
contains the controller code which is interfaced in realtime with a
HAWC2 simulation using the HAWC2Interface Module.
demand to each blade.
"""

from HAWC2_TCP import HAWC2Interface
import numpy as np


class IPC(HAWC2Interface):
    # A class which executes your custom python function.
    def __init__(self, modeldir, K, b, a):
        HAWC2Interface.__init__(self, modeldir)

        self.N = len(b) # order of filter
        self.K = K # Proportional gain of filter
        self.b = b # Numerator coefficients of filter
        self.a = a # Denominator coefficients of coefficients
        #note. len(b) == len(a) == N

        # placeholders for storing the past N inputs and outputs.
        # Assumes 3 blades
        self.x_ = np.zeros([3, self.N])
        self.y_ = np.zeros([3, self.N])



    def update(self, array1):
        theta       = array1[1:4] # Power pitch demand
        x           = array1[4:7] # tip deflection [m]

        x           = x - np.mean(x)   # Center about the mean

        # shift index of past states by 1. eg: [1,2,3,4] -> [4,1,2,3]
        N = self.N
        self.x_[:, 1:N] = self.x_[:, 0:N-1]
        self.y_[:, 1:N] = self.y_[:, 0:N-1]
        self.x_[:, 0]     = x
        self.y_[:, 0]     = [0, 0, 0]

        #apply filter to x_ and y_ to find newest y_
        for i in [0,1,2]:       # For each blade...
            for j in range(N):  # for each past input and output value...
                                # apply filter coefficients.
                self.y_[i,0] += self.b[j] * self.x_[i, j] - self.a[j] * self.y_[i, j]

        #Calculate control feedback action
        theta_ = -self.K*self.y_[:,0]

        # Superimpose IPC control action (theta_) over power pitch
        # demand (theta)
        out = list(theta + theta_)

        return out



if __name__ == '__main__':
    # IPC filter coefficients
    K = -1
    b = [0.04139865635722332, -0.24724984420650856, 0.6153247291080708,
        -0.8167730078549886, 0.6098892568550152, -0.24290112363655772,
        0.04031133337781191]
    a = [1.0, -5.918976177119697, 14.597287405477822, -19.19933888234148,
         14.204054827782327, -5.6043617399861, 0.9213345662369582]

    simTime, sampleTime = 100, 0.01
    N_iters = int(simTime/sampleTime)

    # Run HAWC2 with Python interface.
    HAWC2 = IPC('DTU10MW_Turbine/', K, b, a)
    HAWC2.run('htc/IPCExample.htc', N_iters)

