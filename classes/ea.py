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

	result = subprocess.run(['grep', 'fitness2', 'out.txt'], stdout=subprocess.PIPE)
	fitnessFound = result.stdout.decode("utf-8")

	if fitnessFound == '':
		fitness = (300,)
	else:
		fitness = (int(fitnessFound.split()[1]),)
	print(fitness)
	return fitness


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
