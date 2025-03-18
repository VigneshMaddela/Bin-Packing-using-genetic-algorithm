import random
import numpy as np

NUM_ITEMS = 15
BIN_CAPACITY = 50
POP_SIZE = 30
MUTATION_RATE = 0.2
NUM_GENERATIONS = 200

item_sizes = [random.randint(5, 20) for _ in range(NUM_ITEMS)]
MAX_BINS = NUM_ITEMS  

def create_population():
    return [random.choices(range(MAX_BINS), k=NUM_ITEMS) for _ in range(POP_SIZE)]

def evaluate(chromosome):
    bins = {}
    for idx, bin_id in enumerate(chromosome):
        bins[bin_id] = bins.get(bin_id, 0) + item_sizes[idx]
    
    penalty = sum(max(0, bins[b] - BIN_CAPACITY) for b in bins)
    return -len(bins) - penalty * 100  

def tournament_selection(population, scores):
    group = random.sample(list(zip(population, scores)), 5)
    return max(group, key=lambda x: x[1])[0]

def one_point_crossover(parent1, parent2):
    cut = random.randint(1, NUM_ITEMS - 1)
    return parent1[:cut] + parent2[cut:], parent2[:cut] + parent1[cut:]

def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        index = random.randint(0, NUM_ITEMS - 1)
        chromosome[index] = random.randint(0, MAX_BINS - 1)
    return chromosome

def genetic_algorithm():
    population = create_population()
    
    for _ in range(NUM_GENERATIONS):
        scores = [evaluate(ind) for ind in population]
        next_generation = []

        for _ in range(POP_SIZE // 2):
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)
            child1, child2 = one_point_crossover(parent1, parent2)
            next_generation.extend([mutate(child1), mutate(child2)])

        population = next_generation
    
    optimal_solution = max(population, key=evaluate)
    return optimal_solution, -evaluate(optimal_solution)

solution, bins_used = genetic_algorithm()
print(f"Optimized Packing: {solution}")
print(f"Bins Utilized: {bins_used}")
