import time
from itertools import permutations
from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
from collections import deque

V = TypeVar('V')  # Variable type
D = TypeVar('D')  # Domain type

class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        pass

class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    '''
    def ac3(self) -> bool:
        queue = deque([(xi, xj) for xi in self.variables for xj in self.variables if xi != xj])

        while queue:
            xi, xj = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False  # Domain wiped out; failure
                for xk in self.variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True
    '''

    '''
    def revise(self, xi: V, xj: V) -> bool:
        revised = False
        for x in self.domains[xi][:]:  # Iterate over a copy of the domain
            if not any(
                constraint.satisfied({xi: x, xj: y})
                for constraint in self.constraints[xi]
                for y in self.domains[xj]
            ):
                self.domains[xi].remove(x)
                revised = True
        return revised
    '''

    def ac3(self) -> bool:
        queue = deque([(xi, xj) for xi in self.variables for xj in self.variables if xi != xj])
        print("Starting AC3...")
        while queue:
            xi, xj = queue.popleft()
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    print(f"Domain of {xi} wiped out.")
                    return False  # Domain wiped out; failure
                for xk in self.variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        print("AC3 completed.")
        return True

    def revise(self, xi: V, xj: V) -> bool:
        revised = False
        for x in self.domains[xi][:]:  # Iterate over a copy of the domain
            if not any(
                constraint.satisfied({xi: x, xj: y})
                for constraint in self.constraints[xi]
                for y in self.domains[xj]
            ):
                self.domains[xi].remove(x)
                revised = True
        if revised:
            print(f"Domain of {xi} revised.")
        return revised

  


    def backtracking_search(self, assignment: Dict[V, D] = {}, performance: Dict = None, use_ac3: bool = False) -> Optional[Dict[V, D]]:
        if performance is not None:
            performance["nodes_explored"] += 1

        if len(assignment) == len(self.variables):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.domains[variable]:
            local_assignment = assignment.copy()
            local_assignment[variable] = value
            if self.consistent(variable, local_assignment):
                original_domains = {var: self.domains[var][:] for var in self.variables}

                if use_ac3:
                    if not self.ac3():
                        continue
                
                if self.forward_checking(variable, value, local_assignment):
                    result = self.backtracking_search(local_assignment, performance, use_ac3)
                    if result is not None:
                        return result

                self.domains = original_domains

        return None

    def select_unassigned_variable(self, assignment: Dict[V, D]) -> V:
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def forward_checking(self, variable: V, value: D, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            for neighbor_var in constraint.variables:
                if neighbor_var not in assignment:
                    self.domains[neighbor_var] = [
                        v for v in self.domains[neighbor_var]
                        if constraint.satisfied({**assignment, neighbor_var: v})
                    ]
                    if not self.domains[neighbor_var]:
                        return False
        return True

class CryptoArithmeticConstraint(Constraint[str, int]):
    def __init__(self, equation: str, letters: List[str]) -> None:
        super().__init__(letters)
        self.equation = equation

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        if len(set(assignment.values())) < len(assignment):  # Check for duplicate digits
            return False

        if len(assignment) == len(self.variables):  # Check full assignment
            for key, value in assignment.items():
                if value == 0 and self.equation.index(key) == 0:  # Prevent leading zeroes
                    return False

            equation = self.equation
            for key, value in assignment.items():
                equation = equation.replace(key, str(value))

            try:
                return eval(equation)
            except:
                return False

        return True

def print_solution(equation: str, solution: Dict[str, int]) -> None:
    solved_equation = equation
    for variable, digit in solution.items():
        solved_equation = solved_equation.replace(variable, str(digit))
    print(f"Solved Equation: {solved_equation}")
'''
def brute_force_solve(equation: str):
    letters = list(set(filter(str.isalpha, equation)))
    digits = '0123456789'
    for perm in permutations(digits, len(letters)):
        table = str.maketrans(''.join(letters), ''.join(perm))
        try:
            if eval(equation.translate(table)):
                return {letters[i]: int(perm[i]) for i in range(len(letters))}
        except:
            continue
    return None
'''


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

    return None, node_count  # Corrected indentation



'''
def run_benchmark(equations):
    results = []

    for equation in equations:
        print(f"\nTesting Equation: {equation}")

        letters = list(set(filter(str.isalpha, equation)))

        # Brute-Force Approach
        print("\nBrute-Force Approach")
        start_time = time.time()
        solution = brute_force_solve(equation)
        end_time = time.time()
        brute_force_time = end_time - start_time

        if solution:
            print("Solution:", solution)
            print_solution(equation, solution)
        else:
            print("No solution found!")
        print(f"Time taken: {brute_force_time:.4f} seconds")

        # Vanilla CSP Implementation without Optimizations
        print("\nVanilla CSP Implementation")
        possible_digits = {letter: list(range(10)) for letter in letters}
        for letter in letters:
            if equation.index(letter) == 0:
                possible_digits[letter] = list(range(1, 10))

        csp = CSP(letters, possible_digits)
        csp.add_constraint(CryptoArithmeticConstraint(equation, letters))

        performance_vanilla = {"nodes_explored": 0}
        start_time = time.time()

        solution = csp.backtracking_search(performance=performance_vanilla)

        end_time = time.time()
        vanilla_time = end_time - start_time

        if solution is None:
            print("No solution found!")
        else:
            print("Solution:", solution)
            print_solution(equation, solution)
        print(f"Nodes explored: {performance_vanilla['nodes_explored']}")
        print(f"Time taken: {vanilla_time:.4f} seconds")

        # Optimized CSP Implementation
        print("\nOptimized CSP Implementation")
        csp = CSP(letters, possible_digits)
        csp.add_constraint(CryptoArithmeticConstraint(equation, letters))

        performance_optimized = {"nodes_explored": 0}
        start_time = time.time()

        solution = csp.backtracking_search(performance=performance_optimized, use_ac3=True)

        end_time = time.time()
        optimized_time = end_time - start_time

        if solution is None:
            print("No solution found!")
        else:
            print("Solution:", solution)
            print_solution(equation, solution)
        print(f"Nodes explored: {performance_optimized['nodes_explored']}")
        print(f"Time taken: {optimized_time:.4f} seconds")

        # Collecting Results
        results.append({
            "equation": equation,
            "brute_force_time": brute_force_time,
            "vanilla_time": vanilla_time,
            "optimized_time": optimized_time,
            "brute_force_nodes": "N/A",
            "vanilla_nodes": performance_vanilla["nodes_explored"],
            "optimized_nodes": performance_optimized["nodes_explored"]
        })

    return results
'''




def run_benchmark(equations):
    results = []

    for equation in equations:
        print(f"\nTesting Equation: {equation}")

        letters = list(set(filter(str.isalpha, equation)))

        # Brute-Force Approach
        print("\nBrute-Force Approach")
        start_time = time.time()
        solution, brute_force_nodes = brute_force_solve(equation)
        end_time = time.time()
        brute_force_time = end_time - start_time

        if solution:
            print("Solution:", solution)
            print_solution(equation, solution)
        else:
            print("No solution found!")
        print(f"Time taken: {brute_force_time:.4f} seconds")

        # Vanilla CSP Implementation without Optimizations
        print("\nVanilla CSP Implementation")
        possible_digits = {letter: list(range(10)) for letter in letters}
        for letter in letters:
            if equation.index(letter) == 0:
                possible_digits[letter] = list(range(1, 10))

        csp = CSP(letters, possible_digits)
        csp.add_constraint(CryptoArithmeticConstraint(equation, letters))

        performance_vanilla = {"nodes_explored": 0}
        start_time = time.time()

        solution = csp.backtracking_search(performance=performance_vanilla)

        end_time = time.time()
        vanilla_time = end_time - start_time

        if solution is None:
            print("No solution found!")
        else:
            print("Solution:", solution)
            print_solution(equation, solution)
        print(f"Nodes explored: {performance_vanilla['nodes_explored']}")
        print(f"Time taken: {vanilla_time:.4f} seconds")

        # Optimized CSP Implementation
        print("\nOptimized CSP Implementation")
        csp = CSP(letters, possible_digits)
        csp.add_constraint(CryptoArithmeticConstraint(equation, letters))

        performance_optimized = {"nodes_explored": 0}
        start_time = time.time()

        solution = csp.backtracking_search(performance=performance_optimized, use_ac3=True)

        end_time = time.time()
        optimized_time = end_time - start_time

        if solution is None:
            print("No solution found!")
        else:
            print("Solution:", solution)
            print_solution(equation, solution)
        print(f"Nodes explored: {performance_optimized['nodes_explored']}")
        print(f"Time taken: {optimized_time:.4f} seconds")

        # Collecting Results
        results.append({
            "equation": equation,
            "brute_force_time": brute_force_time,
            "vanilla_time": vanilla_time,
            "optimized_time": optimized_time,
            "brute_force_nodes": brute_force_nodes,
            "vanilla_nodes": performance_vanilla["nodes_explored"],
            "optimized_nodes": performance_optimized["nodes_explored"]
        })

    return results


if __name__ == "__main__":
    equations = [
        "SEND + MORE == MONEY",
        "BASE + BALL == GAMES",
        "TWELVE + THREE == FIFTEEN"
    ]

    results = run_benchmark(equations)

    print("\nBenchmark Results:")
    for result in results:
        print(f"\nEquation: {result['equation']}")
        print(f"Brute-Force Time: {result['brute_force_time']:.4f} seconds")
        print(f"Brute-Force Nodes Explored: {result['brute_force_nodes']}")
        print(f"Vanilla CSP Time: {result['vanilla_time']:.4f} seconds")
        print(f"Optimized CSP Time: {result['optimized_time']:.4f} seconds")
        print(f"Vanilla CSP Nodes Explored: {result['vanilla_nodes']}")
        print(f"Optimized CSP Nodes Explored: {result['optimized_nodes']}")
