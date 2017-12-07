#!/usr/bin/python
from deap import creator, base, tools
import random
import os
import datetime
import numpy
import subprocess
import os.path

IND_SIZE = 9
INT_MIN = 1
INT_MAX = 42
POP_SIZE = 25
GEN_NUM = 25
P_CROSS = 0.25
P_MUT = 0.4
ELITE_NUM = 3

def evaluateBot(individual):
	individual = list(map(abs, individual))
	attack = int((individual[0] * 20)/42)
	divisor = int((individual[1] * 10)/42)
	leave = int((individual[2] * 8)/42)
	runGameCommand = 'java main.RunGame 0 0 0 "java frontLineBot.BotStarter" "java frontLineBot.BotVars %s %s %s %s %s %s %s %s %s" 2>err.txt 1>out.txt' % (str(attack), str(divisor), str(leave), str(individual[3]), str(individual[4]), str(individual[5]), str(individual[6]), str(individual[7]), str(individual[8])) 
#	print(os.getcwd())
#	print(runGameCommand)
	os.system(runGameCommand)

	result = subprocess.run(['grep', 'fitness2', 'out.txt'], stdout=subprocess.PIPE)
	fitnessFound = result.stdout.decode("utf-8")

	if fitnessFound == '':
		fitness = (300,)
	else:
		fitness = (int(fitnessFound.split()[1]),)
#	print(fitness)
	return fitness

def selElitistAndRoulette(individuals, k, num_elitist):
    return tools.selBest(individuals, int(num_elitist)) + tools.selRoulette(individuals, int(k-num_elitist), fit_attr='fitness')
    
creator.create("BotFitness", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.BotFitness)

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, INT_MIN, INT_MAX)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=IND_SIZE)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
pop = toolbox.population(n=POP_SIZE)


toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=10, sigma=7, indpb=0.2)
toolbox.register("selBestElite", tools.selBest, k=ELITE_NUM)
toolbox.register("selBestSingle", tools.selBest, k=1)
toolbox.register("selRouletteElite", tools.selRoulette)
toolbox.register("select", selElitistAndRoulette, num_elitist=ELITE_NUM)
toolbox.register("evaluate", evaluateBot)

stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

print("calculating initial population fitness")
invalid_ind = [ind for ind in pop if not ind.fitness.valid]
fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
for ind, fit in zip(invalid_ind, fitnesses):
	ind.fitness.values = fit

##ind1 = toolbox.individual()
##ind1.fitness.values = evaluate(ind1)
#print(ind1.fitness.valid)
#print(ind1.fitness)

##mutant = toolbox.clone(ind1)
##ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)
##del mutant.fitness.values

##child1, child2 = [toolbox.clone(ind) for ind in (ind1, ind2)]
##tools.cxBlend(child1, child2, 0.5)
##del child1.fitness.values
##del child2.fitness.values

for gen in range(GEN_NUM):
	start = datetime.datetime.now()
	print("generation: " + str(gen))
	offspring = toolbox.selRouletteElite(pop, len(pop))
	offspring = list(map(toolbox.clone, offspring))
	
	best = toolbox.selBestElite(pop)
	best = list(map(toolbox.clone, best))

	for child1, child2 in zip(offspring[::2], offspring[1::2]):
		if random.random() < P_CROSS:
			toolbox.mate(child1, child2)
			del child1.fitness.values
			del child2.fitness.values

	for mutant in offspring:
		if random.random() < P_MUT:
			toolbox.mutate(mutant)
			del mutant.fitness.values

	offspring = best + offspring
	invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
	fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
	for ind, fit in zip(invalid_ind, fitnesses):
		ind.fitness.values = fit


	bestInd = toolbox.selBestSingle(offspring)
	pop[:] = offspring
	record = stats.compile(pop)
	print(record)

	fits = [ind.fitness.values[0] for ind in pop]
	length = len(pop)
	mean = sum(fits) / length
	sum2 = sum(x*x for x in fits)
	std = abs(sum2 / length - mean**2)**0.5
	
	end = datetime.datetime.now()
	delta = end-start

	print(delta)
	csvRow = "%s, %s, %s, %s, %s, %s, %s\n" % (str(gen), str(min(fits)), str(max(fits)), str(mean), str(std), str(delta), str(bestInd))
	with open("GenStats6.csv", "a") as file:
		file.write(csvRow)
	with open("GenReports6.txt", "a") as file:
		file.write(str(record) + "\n")

















