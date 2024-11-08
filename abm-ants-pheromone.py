import pycxsimulator
from matplotlib import pyplot as plt
import numpy as np

width = 50
height = 50
populationSize = 3000

evaporationRate = 0.02
diffusionCoefficient = 0.8
hillClimbingProb = 0.95

def initialize():
    global time, agents, envir, nextenvir

    time = 0
    
    agents = []
    for i in range(populationSize):
        newAgent = [np.random.randint(width), np.random.randint(height)]
        agents.append(newAgent)

    envir = np.zeros([height, width])
    for y in range(height):
        for x in range(width):
            envir[y, x] = np.random.random()

    nextenvir = np.zeros([height, width])

def observe():
    plt.cla()
    plt.imshow(envir, cmap = plt.cm.YlOrRd, vmin = 0, vmax = 3)
    plt.axis('image')
    x = [ag[0] for ag in agents]
    y = [ag[1] for ag in agents]
    plt.scatter(x, y, cmap = plt.cm.bone, alpha = 0.2)
    plt.title('t = ' + str(time))

def clip(a, amin, amax):
    if a < amin: return amin
    elif a > amax: return amax
    else: return a

def update():
    global time, agents, envir, nextenvir

    time += 1

    # diffusion and evaporation of phenomones
    for x in range(width):
        for y in range(height):
            localAv = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    localAv += envir[(y+dy) % height, (x+dx) % width]
            localAv /= 9.0
            nextenvir[y, x] = envir[y, x] + (localAv - envir[y, x]) * diffusionCoefficient
            nextenvir[y, x] *= (1.0 - evaporationRate)

    envir, nextenvir = nextenvir, envir

    for ag in agents:

        if np.random.random() < hillClimbingProb:
            # simulate hill-climbing motion
            maxph = 0
            maxdx = 0
            maxdy = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    tempx = (ag[0]+dx) % width
                    tempy = (ag[1]+dy) % height
                    if maxph < envir[tempy, tempx]:
                        maxph = envir[tempy, tempx]
                        maxdx = dx
                        maxdy = dy
            ag[0] += maxdx
            ag[1] += maxdy
        else:
            ag[0] += np.random.randint(-1, 2)
            ag[1] += np.random.randint(-1, 2)

        ag[0] = clip(ag[0], 0, width - 1)
        ag[1] = clip(ag[1], 0, height - 1)

        # production of pheromones
        envir[ag[1], ag[0]] += 0.01

pycxsimulator.GUI().start(func=[initialize, observe, update])

