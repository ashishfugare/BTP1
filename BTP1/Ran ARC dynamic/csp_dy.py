import time
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

    def ac3(self, queue: Optional[deque] = None) -> bool:
        # If no queue is provided, use all variable pairs
        if not queue:
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

    def backtracking_search(self, assignment: Dict[V, D] = {}, performance: Dict = None) -> Optional[Dict[V, D]]:
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

                if self.forward_checking(variable, value, local_assignment):
                    # Apply AC3 dynamically after forward checking
                    if self.ac3():
                        result = self.backtracking_search(local_assignment, performance)
                        if result is not None:
                            return result

                # Restore domains if search fails
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


if __name__ == "__main__":
    equation = "SEND + MORE == MONEY"
    letters = list(set(filter(str.isalpha, equation)))

    print("Original Equation:", equation)

    possible_digits = {letter: list(range(10)) for letter in letters}
    for letter in letters:
        if equation.index(letter) == 0:
            possible_digits[letter] = list(range(1, 10))

    csp = CSP(letters, possible_digits)
    csp.add_constraint(CryptoArithmeticConstraint(equation, letters))

    # Initializing AC3 dynamically as part of the solution search
    performance = {"nodes_explored": 0}
    start_time = time.time()

    solution = csp.backtracking_search(performance=performance)

    end_time = time.time()

    if solution is None:
        print("No solution found!")
    else:
        print("Solution:", solution)

    print(f"Nodes explored: {performance['nodes_explored']}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")


##"DONALD + GERALD == ROBERT"
    ##"BASE + BALL == GAMES"
    ##"CROSS + ROADS == DANGER"
    ##TWELVE + THREE == FIFTEEN ##No solution as 11 Aplahbets ,Pigeonhole
    ##"SEND + MORE == MONEY",
     ## "BASE + BALL == GAMES",
