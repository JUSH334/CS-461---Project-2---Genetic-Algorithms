import random
import math
import statistics
import matplotlib.pyplot as plt
from typing import List, Tuple

from models import Assignment
from data import rooms, times, facilitators, activities
from fitness import schedule_fitness

# Genetic Algorithm core parameters
POPULATION_SIZE = 500
INITIAL_MUTATION_RATE = 0.01
ELITE_SIZE = 5              # number of top schedules to carry over each generation
MAX_GENERATIONS = 1000
IMPROVEMENT_THRESHOLD = 0.01  # 1% improvement threshold for early stopping in evolve_once


def random_schedule() -> List[Assignment]:
    """Generate a schedule: exactly one assignment per activity."""
    return [
        Assignment(
            activity=act,
            room=random.choice(rooms),
            time_slot=random.choice(times),
            facilitator=random.choice(facilitators),
        )
        for act in activities
    ]


def select_parents(population: List[List[Assignment]], fitnesses: List[float]) -> Tuple[List[Assignment], List[Assignment]]:
    """
    Roulette-wheel selection via softmax-normalized fitness.
    """
    exps = [math.exp(f) for f in fitnesses]
    total = sum(exps)
    probs = [e / total for e in exps]
    return random.choices(population, weights=probs, k=2)


def crossover(parent1: List[Assignment], parent2: List[Assignment]) -> List[Assignment]:
    """One-point crossover on the assignment list."""
    point = random.randrange(1, len(parent1))
    return parent1[:point] + parent2[point:]


def mutate(schedule: List[Assignment], rate: float):
    """Mutate room/time_slot/facilitator for each assignment with probability rate."""
    for i, assign in enumerate(schedule):
        if random.random() < rate:
            field = random.choice(['room', 'time_slot', 'facilitator'])
            if field == 'room':
                schedule[i] = Assignment(assign.activity,
                                         random.choice(rooms),
                                         assign.time_slot,
                                         assign.facilitator)
            elif field == 'time_slot':
                schedule[i] = Assignment(assign.activity,
                                         assign.room,
                                         random.choice(times),
                                         assign.facilitator)
            else:
                schedule[i] = Assignment(assign.activity,
                                         assign.room,
                                         assign.time_slot,
                                         random.choice(facilitators))


def evolve_once(mutation_rate: float) -> Tuple[List[Assignment], float, List[Tuple[float, float]]]:
    """
    Run the GA for up to MAX_GENERATIONS using the given mutation_rate.
    Returns the best schedule found, its fitness, and the generation fitness history.
    """
    # initialize
    population = [random_schedule() for _ in range(POPULATION_SIZE)]
    fitness_history: List[Tuple[float, float]] = []  # list of (avg, best)

    fitnesses = [schedule_fitness(s) for s in population]
    fitness_history.append((statistics.mean(fitnesses), max(fitnesses)))

    for gen in range(1, MAX_GENERATIONS + 1):
        # elitism
        sorted_pop = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
        new_pop = [sched for sched, fit in sorted_pop[:ELITE_SIZE]]

        # reproduction
        while len(new_pop) < POPULATION_SIZE:
            p1, p2 = select_parents(population, fitnesses)
            child = crossover(p1, p2)
            mutate(child, mutation_rate)
            new_pop.append(child)

        population = new_pop
        fitnesses = [schedule_fitness(s) for s in population]

        avg_fit = statistics.mean(fitnesses)
        best_fit = max(fitnesses)
        fitness_history.append((avg_fit, best_fit))

        # logging
        if gen == 1 or gen % 10 == 0:
            print(f"Gen {gen:3d} @ λ={mutation_rate:.4f}: Avg={avg_fit:.2f}, Best={best_fit:.2f}")

        # early stopping after 100 gens
        if gen >= 100:
            prev_avg = fitness_history[gen-100][0]
            if (avg_fit - prev_avg) / abs(prev_avg) < IMPROVEMENT_THRESHOLD:
                print(f"Stopping evolve_once at gen {gen}: <1% improvement")
                break

    # pick best
    best_index = fitnesses.index(max(fitnesses))
    best_schedule = population[best_index]
    best_fitness = fitness_history[-1][1]
    return best_schedule, best_fitness, fitness_history


def adaptive_evolve():
    """
    Adaptively halve the mutation rate as long as best fitness improves.
    """
    mutation_rate = INITIAL_MUTATION_RATE
    best_overall = -math.inf
    best_schedule: List[Assignment] = []
    last_history: List[Tuple[float, float]] = []

    while True:
        print(f"\n--- Running GA with mutation rate = {mutation_rate:.4f} ---")
        sched, fit, history = evolve_once(mutation_rate)
        if fit > best_overall:
            best_overall = fit
            best_schedule = sched
            last_history = history
            mutation_rate /= 2
        else:
            print(f"No improvement at λ={mutation_rate:.4f}; stopping adaptation.")
            break

    # final output
    print(f"\nAdaptive GA final best fitness: {best_overall:.2f}")
    print("Final schedule:")
    for a in best_schedule:
        print(f"  {a.activity.code} | {a.room.name} @ {a.time_slot.label} | {a.facilitator.name}")

    # plot convergence of last run
    gens = list(range(len(last_history)))
    avgs = [h[0] for h in last_history]
    bests = [h[1] for h in last_history]
    plt.figure()
    plt.plot(gens, avgs, label='Average')
    plt.plot(gens, bests, label='Best')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('GA Convergence (final run)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    adaptive_evolve()
