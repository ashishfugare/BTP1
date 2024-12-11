import time
import tracemalloc
import time
import tracemalloc
from re import sub

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

class CSP_crypt:
    
    def __init__(self, problem_str):
        p = problem_str.split()
        
        self.p1 = p[0]
        self.p2 = p[2]
        self.p3 = p[4]
        self.opr = p[1]
        
        self.state = []
        self.solved = False
        
        # Populate unique letters in state
        for q in self.p1 + self.p2 + self.p3:
            if q not in self.state:
                self.state.append(q)
        
        # Fill the remaining state with 'x' placeholders
        for _ in range(10 - len(self.state)):
            self.state.append('x')
    
    def display(self):
        print("Operand 1 : ", self.p1)
        print("Operand 2 : ", self.p2)
        print("Result : ", self.p3)
        print("Operation : ", self.opr)
        print("State (letter mappings) : ", self.state)
        print("Solved : ", self.solved)
    
    def display_ans(self):
        print("Solutions:")
        for i in self.state:
            if i != 'x':
                print(f"{i} - {self.state.index(i)}")
    
    def apply_constraints(self, depth):
        # Apply constraints based on leading zeros, length constraints, etc.
        if len(self.p3) > len(self.p1) and len(self.p3) > len(self.p2):
            if self.state[0] == self.p3[0] or self.state[1] == self.p3[0]:
                return True
            elif depth < 2:
                return True
        else:
            return True
        
        return False
    
    def get_number(self, p):
        # Convert string of letters to a number based on current state mappings
        num = 0
        for q in p:
            num = num * 10 + self.state.index(q)
        return num
    
    def solve(self):
        # Get the integer values of operands and result based on current state
        num1 = self.get_number(self.p1)
        num2 = self.get_number(self.p2)
        num3 = self.get_number(self.p3)
        
        # Evaluate based on the operator
        if self.opr == '+':
            ans = num1 + num2
        elif self.opr == '-':
            ans = num1 - num2
        elif self.opr == '*':
            ans = num1 * num2
        elif self.opr == '/':
            if num2 != 0 and num1 % num2 == 0:  # Ensure integer division
                ans = num1 // num2
            else:
                return  # Avoid invalid division
        
        # Check if the evaluated answer matches the target
        if ans == num3:
            print("Solution Found!")
            print("num1 =", num1)
            print("num2 =", num2)
            print("num3 =", num3)
            self.solved = True
    
    def expand(self, l, r, depth):
        self.solve()
        
        if self.solved:
            return
        elif l == r:
            return
        else:
            for i in range(l, r + 1):
                self.state[l], self.state[i] = self.state[i], self.state[l]
                
                if self.apply_constraints(depth):
                    depth += 1
                    self.expand(l + 1, r, depth)
                    depth -= 1
                
                if self.solved:
                    return
                
                self.state[i], self.state[l] = self.state[l], self.state[i]

if __name__ == "__main__":
    # Input problem
    problem_str = input("Enter the problem (e.g., 'SEND + MORE == MONEY'): ")
    c_csp = CSP_crypt(problem_str)
    
    # Display initial setup
    c_csp.display()
    
    # Start time and memory tracking
    tracemalloc.start()
    start_time = time.time()

    # Try solving the problem
    c_csp.expand(0, 9, 0)

    # End time and memory tracking
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Display final state
    c_csp.display()
    
    # Show solution if found
    if c_csp.solved:
        c_csp.display_ans()
    else:
        print("No solution found.")

    # Output time and space complexity
    print(f"\nExecution Time: {end_time - start_time:.4f} seconds")
    print(f"Current Memory Usage: {current / 10**6:.4f} MB")
    print(f"Peak Memory Usage: {peak / 10**6:.4f} MB")

  
  # Print time and memory usage
print(f"Execution Time: {end_time - start_time:.4f} seconds")
print(f"Current Memory Usage: {current / 10**6:.4f} MB")
print(f"Peak Memory Usage: {peak / 10**6:.4f} MB")
