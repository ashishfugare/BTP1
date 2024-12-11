import itertools
import time
import tracemalloc

# Global counter to track nodes explored
nodes_explored = 0

# Function to check if the solution is valid
def is_valid_solution(assignment, equation):
    # Remove non-alphabet characters from the equation (i.e., +, =, space)
    equation = ''.join(filter(str.isalpha, equation))  # Only keep alphabetic characters

    lhs, rhs = equation.split("=")
    
    # Calculate the lhs and rhs values based on the assignment
    lhs_value = sum(assignment[c] * 10**i for i, c in enumerate(reversed(lhs)))
    rhs_value = sum(assignment[c] * 10**i for i, c in enumerate(reversed(rhs)))
    
    return lhs_value == rhs_value

# Function to solve the cryptarithmetic problem using a greedy approach
def solve_cryptarithmetic_greedy(equation):
    global nodes_explored
    
    # Remove non-alphabet characters from the equation
    equation = ''.join(filter(str.isalpha, equation))  # Only keep alphabetic characters
    
    # Extract unique characters in the equation, excluding operators
    unique_chars = list(set(equation))
    
    # Sort characters based on their positional significance (greedy choice)
    sorted_chars = sorted(unique_chars, key=lambda x: equation.rfind(x), reverse=True)
    
    # Start assigning digits from 9 downwards, trying to match significance
    for perm in range(10 ** len(sorted_chars)):
        nodes_explored += 1  # Increment for each node (permutation) explored
        
        # Map digits to characters according to sorted significance
        digits = list(map(int, str(perm).zfill(len(sorted_chars))))
        
        # Skip invalid assignments where two characters have the same digit
        if len(set(digits)) != len(digits):
            continue
        
        # Assign characters to digits
        assignment = dict(zip(sorted_chars, digits))
        
        # Check if this assignment satisfies the equation
        if is_valid_solution(assignment, equation):
            return assignment
    
    return None

# Define the cryptarithmetic problem
equation = "SEND + MORE = MONEY"

# Start memory and time tracking
tracemalloc.start()
start_time = time.time()

# Solve the problem using the greedy method
solution = solve_cryptarithmetic_greedy(equation)

# Stop time and memory tracking
end_time = time.time()
current_memory, peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Print results
if solution:
    print("Solution found:", solution)
else:
    print("No solution found.")

# Output performance metrics
print(f"\nExecution Time: {end_time - start_time:.4f} seconds")
print(f"Peak Memory Usage: {peak_memory / 10**6:.4f} MB")
print(f"Nodes Explored: {nodes_explored}")
