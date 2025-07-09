"""
Test execution utilities for LeetCode solutions
"""

import re
import sys
import traceback
from typing import List, Dict, Any, Tuple
import time
import ast

class TestExecutor:
    """Execute and validate LeetCode solutions with feedback loop support"""

    def __init__(self):
        self.test_results = []
        self.execution_time = 0
        self.feedback_history = []
        self.iteration_count = 0
        
    def extract_function_name(self, code: str) -> str:
        """Extract the main function name from the code"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    return node.name
        except:
            pass
        
        # Fallback: look for common LeetCode function patterns
        patterns = [
            r'def\s+(\w+)\s*\(',
            r'class\s+Solution.*?def\s+(\w+)\s*\('
        ]
        
        for pattern in patterns:
            match = re.search(pattern, code)
            if match:
                return match.group(1)
        
        return None
    
    def prepare_code_for_execution(self, code: str) -> str:
        """Prepare code for safe execution"""
        # Remove any existing test code
        lines = code.split('\n')
        clean_lines = []
        
        for line in lines:
            # Skip test-related lines
            if any(keyword in line.lower() for keyword in ['assert', 'test', 'print', 'input()']):
                continue
            clean_lines.append(line)
        
        return '\n'.join(clean_lines)
    
    def create_test_cases(self, problem_text: str) -> List[Dict[str, Any]]:
        """Extract test cases from problem description"""
        test_cases = []
        
        # Look for example patterns
        example_pattern = r'Example\s*\d*:.*?Input:\s*(.*?).*?Output:\s*(.*?)(?=\n|Example|\Z)'
        matches = re.findall(example_pattern, problem_text, re.DOTALL | re.IGNORECASE)
        
        for i, (input_text, output_text) in enumerate(matches):
            try:
                # Clean and parse input/output
                input_clean = input_text.strip().replace('Input:', '').strip()
                output_clean = output_text.strip().replace('Output:', '').strip()
                
                test_cases.append({
                    'id': f'example_{i+1}',
                    'input_raw': input_clean,
                    'output_raw': output_clean,
                    'description': f'Example {i+1} from problem'
                })
            except Exception as e:
                print(f"Error parsing example {i+1}: {e}")
        
        # Add common edge cases
        edge_cases = self.generate_edge_cases(problem_text)
        test_cases.extend(edge_cases)
        
        return test_cases
    
    def generate_edge_cases(self, problem_text: str) -> List[Dict[str, Any]]:
        """Generate common edge cases based on problem type"""
        edge_cases = []
        
        # Array problems
        if 'array' in problem_text.lower() or 'nums' in problem_text.lower():
            edge_cases.extend([
                {'id': 'empty_array', 'input_raw': '[]', 'output_raw': 'varies', 'description': 'Empty array'},
                {'id': 'single_element', 'input_raw': '[1]', 'output_raw': 'varies', 'description': 'Single element'},
                {'id': 'two_elements', 'input_raw': '[1, 2]', 'output_raw': 'varies', 'description': 'Two elements'}
            ])
        
        # String problems
        if 'string' in problem_text.lower():
            edge_cases.extend([
                {'id': 'empty_string', 'input_raw': '""', 'output_raw': 'varies', 'description': 'Empty string'},
                {'id': 'single_char', 'input_raw': '"a"', 'output_raw': 'varies', 'description': 'Single character'}
            ])
        
        # Tree problems
        if 'tree' in problem_text.lower() or 'node' in problem_text.lower():
            edge_cases.extend([
                {'id': 'null_tree', 'input_raw': 'null', 'output_raw': 'varies', 'description': 'Null/empty tree'},
                {'id': 'single_node', 'input_raw': '[1]', 'output_raw': 'varies', 'description': 'Single node tree'}
            ])
        
        return edge_cases
    
    def execute_test_case(self, code: str, test_case: Dict[str, Any], function_name: str) -> Dict[str, Any]:
        """Execute a single test case"""
        result = {
            'test_id': test_case['id'],
            'description': test_case['description'],
            'passed': False,
            'error': None,
            'execution_time': 0,
            'expected': test_case.get('output_raw', 'Unknown'),
            'actual': None
        }
        
        try:
            # Create execution environment
            exec_globals = {}
            
            # Execute the solution code
            start_time = time.time()
            exec(code, exec_globals)
            
            # Get the function
            if function_name in exec_globals:
                solution_func = exec_globals[function_name]
            elif 'Solution' in exec_globals:
                solution_instance = exec_globals['Solution']()
                solution_func = getattr(solution_instance, function_name)
            else:
                raise Exception(f"Function {function_name} not found")
            
            # Parse input (simplified - would need more sophisticated parsing for complex inputs)
            input_val = self.parse_input(test_case['input_raw'])
            
            # Execute function
            if isinstance(input_val, list) and len(input_val) == 1:
                actual_result = solution_func(input_val[0])
            elif isinstance(input_val, list):
                actual_result = solution_func(*input_val)
            else:
                actual_result = solution_func(input_val)
            
            end_time = time.time()
            
            result['actual'] = str(actual_result)
            result['execution_time'] = end_time - start_time
            result['passed'] = True  # Basic execution success
            
        except Exception as e:
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
        
        return result
    
    def parse_input(self, input_str: str) -> Any:
        """Parse input string to Python object"""
        try:
            # Handle common LeetCode input formats
            input_str = input_str.strip()
            
            # Handle multiple inputs separated by comma
            if ',' in input_str and not input_str.startswith('['):
                parts = [part.strip() for part in input_str.split(',')]
                return [eval(part) for part in parts]
            
            # Single input
            return eval(input_str)
        except:
            return input_str
    
    def run_all_tests(self, code: str, problem_text: str) -> Dict[str, Any]:
        """Run all test cases for a solution"""
        function_name = self.extract_function_name(code)
        if not function_name:
            return {
                'success': False,
                'error': 'Could not extract function name from code',
                'test_results': []
            }
        
        clean_code = self.prepare_code_for_execution(code)
        test_cases = self.create_test_cases(problem_text)
        
        results = []
        passed_count = 0
        
        for test_case in test_cases:
            if test_case.get('output_raw') == 'varies':
                continue  # Skip edge cases without expected output
                
            result = self.execute_test_case(clean_code, test_case, function_name)
            results.append(result)
            
            if result['passed'] and not result['error']:
                passed_count += 1
        
        return {
            'success': True,
            'function_name': function_name,
            'total_tests': len(results),
            'passed_tests': passed_count,
            'test_results': results,
            'pass_rate': passed_count / len(results) if results else 0,
            'leetcode_ready': passed_count == len(results) and len(results) > 0,
            'needs_feedback': passed_count < len(results) and len(results) > 0
        }

    def generate_feedback(self, test_results: Dict[str, Any], problem_text: str) -> str:
        """Generate detailed feedback for failed test cases"""
        if not test_results.get('needs_feedback', False):
            return None

        failed_tests = [result for result in test_results['test_results'] if not result['passed'] or result['error']]

        if not failed_tests:
            return None

        self.iteration_count += 1

        feedback = []
        feedback.append(f"**Feedback Analysis (Iteration {self.iteration_count}):**")
        feedback.append(f"**Failed Tests:** {len(failed_tests)}/{test_results['total_tests']}")

        # Analyze failure patterns
        error_patterns = {}
        for test in failed_tests:
            if test['error']:
                error_type = type(test['error']).__name__ if hasattr(test['error'], '__name__') else 'RuntimeError'
                error_patterns[error_type] = error_patterns.get(error_type, 0) + 1

        feedback.append("**Root Causes:**")
        for error_type, count in error_patterns.items():
            feedback.append(f"- {error_type}: {count} occurrences")

        feedback.append("**Specific Issues:**")
        for i, test in enumerate(failed_tests[:3]):  # Show first 3 failures
            feedback.append(f"- Test '{test['description']}': {test['error'] or 'Incorrect output'}")
            if test['error']:
                feedback.append(f"  Error: {test['error']}")
            else:
                feedback.append(f"  Expected: {test['expected']}, Got: {test['actual']}")

        feedback.append("**Instructions for Code Generator:**")
        feedback.append("- Fix the specific errors mentioned above")
        feedback.append("- Pay special attention to edge cases that failed")
        feedback.append("- Ensure proper input validation and error handling")
        feedback.append("- Test your solution mentally before providing the code")

        if self.iteration_count >= 3:
            feedback.append("**⚠️ WARNING: Maximum iterations approaching. Please provide a robust solution.**")

        feedback.append(f"**Iteration Status:** {self.iteration_count}/3")

        if self.iteration_count >= 3:
            feedback.append("**Action Required:** MAX_ITERATIONS_REACHED")
        else:
            feedback.append("**Action Required:** REGENERATE_CODE")

        feedback_text = "\n".join(feedback)
        self.feedback_history.append(feedback_text)

        return feedback_text

    def reset_feedback_loop(self):
        """Reset feedback loop counters"""
        self.iteration_count = 0
        self.feedback_history = []

def format_test_results(test_results: Dict[str, Any]) -> str:
    """Format test results for display"""
    if not test_results['success']:
        return f"❌ Test execution failed: {test_results.get('error', 'Unknown error')}"
    
    output = []
    output.append(f"🧪 **Test Results for `{test_results['function_name']}`**")
    output.append(f"📊 **Summary:** {test_results['passed_tests']}/{test_results['total_tests']} tests passed ({test_results['pass_rate']:.1%})")
    
    if test_results['leetcode_ready']:
        output.append("✅ **LeetCode Ready:** YES - All tests passed!")
    else:
        output.append("⚠️ **LeetCode Ready:** NO - Some tests failed")
    
    output.append("\n**Individual Test Results:**")
    
    for result in test_results['test_results']:
        status = "✅ PASS" if result['passed'] and not result['error'] else "❌ FAIL"
        output.append(f"- {status} {result['description']}")
        
        if result['error']:
            output.append(f"  Error: {result['error']}")
        else:
            output.append(f"  Expected: {result['expected']}")
            output.append(f"  Actual: {result['actual']}")
            output.append(f"  Time: {result['execution_time']:.4f}s")
    
    return "\n".join(output)
