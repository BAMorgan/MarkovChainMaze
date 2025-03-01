import pyamaze as maze
import random
import argparse
from Markov import Markov

def main(size, loopperc):
    start_position = (random.randint(1, size), random.randint(1, size))
    goal_position = (random.randint(1, size), random.randint(1, size))
    m = maze.maze(rows=size, cols=size)
    m.CreateMaze(goal_position[0], goal_position[1], loopPercent=loopperc)
    n_steps = 100

    markov = Markov(m)
    markov.build_matrix()

    # steady-state distribution transition matrix
    steady_state_transition_matrix = markov.get_steady_state()

    goal_step, likely_position, likely_position_probability, goal_transition_matrix, transition_matrices = markov.find_goal_and_most_likely_position(start_position, goal_position, n_steps)

    if goal_step:
        print(f"Agent reached the goal at step: {goal_step}")
        print(f"Transition Matrix at step: {goal_step}")
        print(goal_transition_matrix)

    else:
        print("Agent did not reach the goal within the given steps.")

    # Save or print transition matrices every 10 steps
    for step, matrix in transition_matrices:
        print(f"Transition Matrix after {step} steps:")
        print(matrix)

    print(f"Most likely position after {n_steps} steps: {likely_position}")
    print(f"Probability of being in this position: {likely_position_probability}")

    print("Steady-State Transition Matrix:")
    print(steady_state_transition_matrix)

    # most likely goal paths
    most_likely_paths = markov.find_most_likely_paths(start_position, goal_position, n_steps)
    formatted_paths = markov.format_paths_with_cumulative_probability(most_likely_paths)
    # sort by probabilitiy
    sorted_paths = sorted(formatted_paths, key=lambda x: x[1], reverse=True)

    # top 3 paths by probability
    top_3_paths = [path[0] for path in sorted_paths[:3]]

    a = maze.agent(m, start_position[0], start_position[1], shape='arrow', footprints=True, color=maze.COLOR.red)
    b = maze.agent(m, start_position[0], start_position[1], shape='arrow', footprints=True, color=maze.COLOR.blue)
    c = maze.agent(m, start_position[0], start_position[1], shape='arrow', footprints=True, color=maze.COLOR.yellow)

    m.tracePath({a:top_3_paths[0], b:top_3_paths[1], c:top_3_paths[2]})

    output_file = "readme.txt"
    with open(output_file, "a") as f:
        f.write(f"Size of maze: {size} by {size}    Loop percentage: {loopperc}\n" )
        if goal_step:
            f.write(f"Agent reached the goal at step: {goal_step}\n")
            f.write(f"\nTransition Matrix at step: {goal_step}\n")
            f.write(str(goal_transition_matrix) + "\n")

        for step, matrix in transition_matrices:
            f.write(f"\nTransition Matrix after {step} steps:\n")
            f.write(str(matrix) + "\n")

        f.write(f"\nMost likely position after {n_steps} steps: {likely_position}\n")
        f.write(f"Probability of being in this position: {likely_position_probability}\n")
        f.write(f"\nSteady State Transition Matrix: \n{steady_state_transition_matrix}\n")

    m.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify maze size and loop percentage.")
    parser.add_argument('size', type=int, help="Size of the maze ")
    parser.add_argument('loopperc', type=int, help="Loop percentage (0 or 50)")

    args = parser.parse_args()
    main(args.size, args.loopperc)