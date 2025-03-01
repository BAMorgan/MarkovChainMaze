import numpy as np
from numpy.linalg import eig

class Markov:
    def __init__(self, maze):
        self.maze = maze
        self.rows = maze.rows
        self.cols = maze.cols
        self.size = self.rows * self.cols
        self.transition_matrix = np.zeros((self.size, self.size))

    def get_index(self, x, y):
        return (x - 1) * self.cols + (y - 1)

    def get_position(self, index):
        return index // self.cols + 1, index % self.cols + 1

    def build_matrix(self):
        for x in range(1, self.rows + 1):
            for y in range(1, self.cols + 1):
                current_index = self.get_index(x, y)
                possible_moves = []

                # check possible moves
                if self.maze.maze_map[(x, y)]['N'] == 1 and x > 1:
                    possible_moves.append(self.get_index(x - 1, y))
                if self.maze.maze_map[(x, y)]['S'] == 1 and x < self.rows:
                    possible_moves.append(self.get_index(x + 1, y))
                if self.maze.maze_map[(x, y)]['E'] == 1 and y < self.cols:
                    possible_moves.append(self.get_index(x, y + 1))
                if self.maze.maze_map[(x, y)]['W'] == 1 and y > 1:
                    possible_moves.append(self.get_index(x, y - 1))

                if not possible_moves:
                    self.transition_matrix[current_index, current_index] = 1
                else:
                    prob = 1.0 / len(possible_moves)
                    for move in possible_moves:
                        self.transition_matrix[current_index, move] = prob

        return self.transition_matrix

    def get_steady_state(self):
        eigenvalues, eigenvectors = eig(self.transition_matrix.T)

        # eigenvector corresponding to eigenvalue 1
        steady_state_vector = eigenvectors[:, np.isclose(eigenvalues, 1)]

        # normalize
        steady_state_distribution = steady_state_vector[:, 0].real
        steady_state_distribution /= steady_state_distribution.sum()

        # steady-state transition matrix
        steady_state_transition_matrix = np.tile(steady_state_distribution, (self.size, 1))

        return  steady_state_transition_matrix

    def find_goal_and_most_likely_position(self, start_position, goal_position, n_steps):
        current_state = np.zeros((self.size,))
        current_state[self.get_index(*start_position)] = 1.0
        goal_index = self.get_index(*goal_position)
        goal_reached_at_step = None
        most_likely_position = start_position
        most_likely_probability = 1.0 / self.size
        goal_transition_matrix = []
        transition_matrices = []

        for step in range(1, n_steps + 1):
            current_state = np.dot(current_state, self.transition_matrix)

            # transition matrix every 10 steps
            if step % 10 == 0:
                transition_matrices.append((step, current_state.copy()))

            # check if the agent reached the goal
            if goal_reached_at_step is None and current_state[goal_index] > 0:
                goal_reached_at_step = step
                goal_transition_matrix = current_state.copy()

            # update most likely position after current step
            most_likely_state = np.argmax(current_state)
            most_likely_position = (int(most_likely_state // self.cols + 1), int(most_likely_state % self.cols + 1))
            most_likely_probability = current_state[most_likely_state]

        return goal_reached_at_step, most_likely_position, most_likely_probability, goal_transition_matrix, transition_matrices

    def find_most_likely_paths(self, start_position, goal_position, n_steps):
        current_state = np.zeros((self.size,))
        current_state[self.get_index(*start_position)] = 1.0
        goal_index = self.get_index(*goal_position)

        paths = {i: [] for i in range(self.size)}
        paths[self.get_index(*start_position)] = [(start_position, 1.0)]

        most_likely_paths = []

        for step in range(1, n_steps + 1):
            next_state = np.dot(current_state, self.transition_matrix)
            new_paths = {i: [] for i in range(self.size)}

            # go over all positions in the maze
            for num in range(self.size):
                if current_state[num] > 0:
                    for next_num in range(self.size):
                        prob = current_state[num] * self.transition_matrix[num, next_num]
                        if prob > 0:
                            new_path = paths[num] + [(self.get_position(next_num), prob)]
                            if not new_paths[next_num] or new_paths[next_num][-1][1] < prob:
                                new_paths[next_num] = new_path

            current_state = next_state
            paths = new_paths

            # store most likely path to the goal if reached
            if current_state[goal_index] > 0:
                most_likely_paths.append(paths[goal_index])

        return most_likely_paths

    def format_paths_with_cumulative_probability(self,paths):
        formatted_paths = []
        for path in paths:
            positions = [step[0] for step in path]
            cumulative_probability = np.prod([step[1] for step in path])

            formatted_paths.append((positions, cumulative_probability))
        return formatted_paths