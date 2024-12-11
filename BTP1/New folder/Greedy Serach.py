import itertools
import time
import tracemalloc

# Global counter to track nodes explored
nodes_explored = 0

# Function to check if the solution is valid
def is_valid_solution(assignment, equation):
    lhs, rhs = equation.split("=")
    lhs_value = sum(assignment[c] * 10**i for i, c in enumerate(reversed(lhs)))
    rhs_value = sum(assignment[c] * 10**i for i, c in enumerate(reversed(rhs)))
    return lhs_value == rhs_value

# Function to solve the cryptarithmetic problem using greedy search
def solve_cryptarithmetic(equation):
    global nodes_explored  # Use global counter
    unique_chars = set(equation) - {'+', '=', ' '}
    chars_list = list(unique_chars)
    
    # Iterate over all permutations of possible digits for unique characters
    for perm in itertools.permutations(range(10), len(chars_list)):
        nodes_explored += 1  # Increment for each node (permutation) explored
        assignment = dict(zip(chars_list, perm))
        
        if is_valid_solution(assignment, equation):
            return assignment
    return None

# Define the cryptarithmetic problem
equation = "SEND + MORE = MONEY"

# Start memory and time tracking
tracemalloc.start()
start_time = time.time()

# Solve the problem
solution = solve_cryptarithmetic(equation)

# Stop time and memory tracking
end_time = time.time()
current_memory, peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Print results
if solution:
    print("Solution found:", solution)
else:
    print("No solution found.")

# Output time, memory, and nodes explored
print(f"\nExecution Time: {end_time - start_time:.4f} seconds")
print(f"Peak Memory Usage: {peak_memory / 10**6:.4f} MB")
print(f"Nodes Explored: {nodes_explored}")
