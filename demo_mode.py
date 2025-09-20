#!/usr/bin/env python3
"""
Demo mode for AlgoGenie - Works without OpenAI API
This demonstrates the application structure without requiring API calls
"""

import asyncio
import sys
from config.docker_utils import start_docker_container, stop_docker_container

class MockDockerExecutor:
    """Mock Docker executor for demo purposes"""
    def __init__(self):
        self.work_dir = 'temp'
        self.timeout = 120
    
    async def start(self):
        print("🐳 Mock Docker container started")
        return True
    
    async def stop(self):
        print("🐳 Mock Docker container stopped")
        return True
    
    async def execute_code(self, code):
        """Mock code execution"""
        print(f"📝 Executing code:\n{code}")
        print("✅ Mock execution completed successfully")
        return "Mock execution result: Code ran successfully!"

class MockProblemSolver:
    """Mock problem solver agent"""
    def __init__(self):
        self.name = "DSA_Problem_Solver_Agent"
    
    async def solve_problem(self, problem):
        """Mock problem solving"""
        print(f"🧠 {self.name}: Analyzing problem: {problem}")
        
        # Mock solution
        solution = '''
def add_two_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int): First number
        b (int): Second number
    
    Returns:
        int: Sum of a and b
    """
    return a + b

# Test cases
def test_add_two_numbers():
    # Test case 1: Positive numbers
    assert add_two_numbers(2, 3) == 5
    print("✅ Test 1 passed: 2 + 3 = 5")
    
    # Test case 2: Negative numbers
    assert add_two_numbers(-1, -2) == -3
    print("✅ Test 2 passed: -1 + (-2) = -3")
    
    # Test case 3: Mixed numbers
    assert add_two_numbers(5, -3) == 2
    print("✅ Test 3 passed: 5 + (-3) = 2")
    
    print("🎉 All tests passed!")

if __name__ == "__main__":
    test_add_two_numbers()
    print(f"Result: {add_two_numbers(10, 20)}")
'''
        
        print(f"🧠 {self.name}: Generated solution with test cases")
        return solution

class MockCodeExecutor:
    """Mock code executor agent"""
    def __init__(self, docker_executor):
        self.name = "CodeExecutorAgent"
        self.docker = docker_executor
    
    async def execute_solution(self, code):
        """Mock code execution"""
        print(f"🤖 {self.name}: Executing the solution...")
        
        # Mock execution
        result = await self.docker.execute_code(code)
        
        print(f"🤖 {self.name}: Code executed successfully!")
        print(f"🤖 {self.name}: Saving code to solution.py...")
        
        # Save code to file
        with open('temp/solution.py', 'w', encoding='utf-8') as f:
            f.write(code)
        
        print("✅ Code saved successfully in solution.py")
        return result

async def demo_main():
    """Demo main function"""
    try:
        print("🚀 Starting AlgoGenie Demo Mode")
        print("=" * 50)
        print("ℹ️  This is a demo version that works without OpenAI API")
        print("=" * 50)
        
        # Initialize mock components
        docker_executor = MockDockerExecutor()
        problem_solver = MockProblemSolver()
        code_executor = MockCodeExecutor(docker_executor)
        
        # Start Docker container
        await docker_executor.start()
        print("✅ Mock Docker container started successfully")
        
        # Define problem
        task = 'Write a Python code to add two numbers.'
        print(f"📝 Task: {task}")
        print("=" * 50)
        
        # Solve problem
        print("🔄 Starting problem solving process...")
        print("=" * 20)
        
        # Step 1: Problem analysis
        solution = await problem_solver.solve_problem(task)
        
        print("=" * 20)
        
        # Step 2: Code execution
        result = await code_executor.execute_solution(solution)
        
        print("=" * 20)
        
        # Step 3: Final result
        print("🎉 Problem solved successfully!")
        print("📁 Solution saved to: temp/solution.py")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        sys.exit(1)
    finally:
        try:
            await docker_executor.stop()
            print("✅ Mock Docker container stopped")
        except Exception as e:
            print(f"⚠️  Warning: Error stopping mock Docker container: {e}")

if __name__ == "__main__":
    asyncio.run(demo_main())
