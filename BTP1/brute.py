import time
from itertools import permutations

def brute_force_solve(equation: str):
    letters = list(set(filter(str.isalpha, equation)))
    digits = '0123456789'
    node_count = 0  # Initialize node count
    for perm in permutations(digits, len(letters)):
        node_count += 1
        table = str.maketrans(''.join(letters), ''.join(perm))
        try:
            if eval(equation.translate(table)):
                return {letters[i]: int(perm[i]) for i in range(len(letters))}, node_count
        except:
            continue
    return None, node_count

if __name__ == "__main__":
    equation = "TWELVE + THREE == FIFTEEN"
    
    print(f"Testing Equation: {equation}")

    # Brute-Force Approach
    print("\nBrute-Force Approach")
    start_time = time.time()
    solution, brute_force_nodes = brute_force_solve(equation)
    end_time = time.time()
    brute_force_time = end_time - start_time

    if solution:
        print("Solution:", solution)
    else:
        print("No solution found!")
    
    print(f"Time taken: {brute_force_time:.4f} seconds")
    print(f"Nodes explored: {brute_force_nodes}")

    ##"DONALD + GERALD == ROBERT"
    ##"BASE + BALL == GAMES"
    ##"CROSS + ROADS == DANGER"
    ##TWELVE + THREE == FIFTEEN ##No solution as 11 Aplahbets ,Pigeonhole
    ##"SEND + MORE == MONEY",
