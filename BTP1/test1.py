from csp import Constraint, CSP
from typing import Dict, List, Optional


class CryptoArithmeticConstraint(Constraint[str, int]):
    def __init__(self, letters: List[str], operands: List[str], result: str) -> None:
        super().__init__(letters)
        self.letters = letters
        self.operands = operands
        self.result = result

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        # Ensure no duplicate digits
        if len(set(assignment.values())) < len(assignment):
            return False

        # If all variables are assigned, check the equation
        if len(assignment) == len(self.letters):
            operand_values = [
                int("".join(str(assignment[letter]) for letter in operand))
                for operand in self.operands
            ]
            result_value = int("".join(str(assignment[letter]) for letter in self.result))

            return sum(operand_values) == result_value

        return True  # Partial assignment is consistent


def solve_crypto_arithmetic(equation: str) -> None:
    # Parse the input equation
    equation = equation.replace(" ", "")
    lhs, rhs = equation.split("=")
    operands = lhs.split("+")
    result = rhs

    # Find all unique letters in the equation
    unique_letters = set("".join(operands) + result)
    letters = list(unique_letters)

    # Assign possible digits to letters
    possible_digits: Dict[str, List[int]] = {}
    for letter in letters:
        possible_digits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Leading letter of the result or operands cannot be 0
    for operand in operands + [result]:
        possible_digits[operand[0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Create CSP
    csp: CSP[str, int] = CSP(letters, possible_digits)
    csp.add_constraint(CryptoArithmeticConstraint(letters, operands, result))

    # Solve using backtracking
    solution: Optional[Dict[str, int]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print("Solution:", solution)
        # Substitute solution into the equation for validation
        operand_values = [
            int("".join(str(solution[letter]) for letter in operand))
            for operand in operands
        ]
        result_value = int("".join(str(solution[letter]) for letter in result))
        print(f"Verification: {' + '.join(map(str, operand_values))} = {result_value}")


if __name__ == "__main__":
    # Example input
    equation = input("Enter a cryptoarithmetic equation (e.g., SEND + MORE = MONEY): ")
    solve_crypto_arithmetic(equation)
