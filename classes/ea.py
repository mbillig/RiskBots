from deap import creator, base, tools
import random
import os
import subprocess
import os.path

def evaluate(individual):
    runGameCommand = 'java main.RunGame 0 0 0 "java bot.BotStarter" "java frontLineBot.BotVars %s %s %s %s %s %s %s %s %s" 2>err.txt 1>out.txt' % (str(individual[0]), str(individual[1]), str(individual[2]), str(individual[3]), str(individual[4]), str(individual[5]), str(individual[6]), str(individual[7]), str(individual[8])) 
    print(os.getcwd())
    print(runGameCommand)
    os.system(runGameCommand)
    os.system('findstr fitness2 out.txt 1>fitness.txt 2>fiterr.txt')
    print(os.path.isfile('fitness.txt'))
    with open("fitness.txt", "r") as fitFile:
        fitnessStr = fitFile.readlines()
    print(fitnessStr)
    fitnessFound = fitnessStr
    #print(found)
    if fitnessFound == '':
        fitness = (300,)
    else:
        fitness = (int(found.split()[1]),)
    print(fitness)
    os.system('cd ../')
    return fitness

print("testing")

creator.create("BotFitness", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.BotFitness)

IND_SIZE = 9
INT_MIN = 1
INT_MAX = 42
POP_SIZE = 25

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, INT_MIN, INT_MAX)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=IND_SIZE)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.population(n=POP_SIZE)

ind1 = toolbox.individual()
ind1.fitness.values = evaluate(ind1)
print(ind1.fitness.valid)
print(ind1.fitness)
