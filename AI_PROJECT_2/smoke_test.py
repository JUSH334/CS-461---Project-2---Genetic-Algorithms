import statistics
from main import random_schedule
from fitness import schedule_fitness


def smoke_test(num_schedules: int = 1000):
    """
    Generate random schedules, compute fitness,
    and print min, average, max fitness, plus
    worst/best assignments and a fitness histogram.
    """
    scored = []  # list of (score, schedule)
    for _ in range(num_schedules):
        sched = random_schedule()
        score = schedule_fitness(sched)
        scored.append((score, sched))

    # Extract scores
    scores = [score for score, _ in scored]
    min_score = min(scores)
    max_score = max(scores)
    avg_score = statistics.mean(scores)

    # Print summary
    print(f"Minimum fitness: {min_score:.2f}")
    print(f"Average fitness: {avg_score:.2f}")
    print(f"Maximum fitness: {max_score:.2f}\n")

    # Worst schedule
    worst_sched = next(sched for score, sched in scored if score == min_score)
    print("Worst schedule assignments:")
    for assign in worst_sched:
        print(f"  {assign.activity.code} | {assign.room.name} @ {assign.time_slot.label} | {assign.facilitator.name}")
    print()

    # Best schedule
    best_sched = next(sched for score, sched in scored if score == max_score)
    print("Best schedule assignments:")
    for assign in best_sched:
        print(f"  {assign.activity.code} | {assign.room.name} @ {assign.time_slot.label} | {assign.facilitator.name}")
    print()

if __name__ == "__main__":
    smoke_test(1000)
