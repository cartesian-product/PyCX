import pycxsimulator
import numpy as np
from matplotlib import pyplot as plt

width = 50
height = 50
populationSize = 50

free = 0
carrying = 1

garbageProb = 0.8

def initialize():
    global time, agents, envir

    time = 0

    agents = []
    for i in range(populationSize):
        newAgent = [np.random.randint(width), np.random.randint(height), free]
        agents.append(newAgent)

    envir = np.zeros([height, width])
    for y in range(height):
        for x in range(width):
            if np.random.random() < garbageProb:
                state = 1
            else:
                state = 0
            envir[y, x] = state

def observe():
    plt.cla()
    plt.imshow(envir, cmap = plt.cm.YlOrRd, vmin = 0, vmax = 5)
    plt.axis('image')
    x = [ag[0] for ag in agents]
    y = [ag[1] for ag in agents]
    s = [ag[2] for ag in agents]
    plt.scatter(x, y, c = s, cmap = plt.cm.bwr)
    plt.title('t = ' + str(time))

def clip(a, amin, amax):
    if a < amin: return amin
    elif a > amax: return amax
    else: return a

def update():
    global time, agents, envir

    time += 1
    
    for ag in agents:

        # simulate random motion
        ag[0] += np.random.randint(-1, 2)
        ag[1] += np.random.randint(-1, 2)
        ag[0] = clip(ag[0], 0, width - 1)
        ag[1] = clip(ag[1], 0, height - 1)

        # simulate interaction between ants and environment
        if envir[ag[1], ag[0]] > 0:
            if ag[2] == free:
                envir[ag[1], ag[0]] -= 1
                ag[2] = carrying
            else:
                envir[ag[1], ag[0]] += 1
                ag[2] = free

pycxsimulator.GUI().start(func=[initialize, observe, update])
