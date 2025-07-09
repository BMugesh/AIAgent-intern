"""
Feedback loop system for iterative code improvement
"""

from typing import Dict, List, Any, Tuple
from test_executor import TestExecutor
from config import Config
import re

class FeedbackLoop:
    """Manages the feedback loop between test validation and code generation"""
    
    def __init__(self):
        self.iteration_count = 0
        self.max_iterations = Config.MAX_FEEDBACK_ITERATIONS
        self.test_executor = TestExecutor()
        self.feedback_history = []
        
    def analyze_test_failures(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test failures and create detailed feedback"""
        if test_results['leetcode_ready']:
            return {
                'needs_feedback': False,
                'message': "All tests passed! Solution is ready for optimization.",
                'feedback_type': 'success'
            }
        
        failed_tests = [test for test in test_results['test_results'] if not test['passed'] or test['error']]
        
        if not failed_tests:
            return {
                'needs_feedback': False,
                'message': "No specific test failures found.",
                'feedback_type': 'unclear'
            }
        
        # Categorize failures
        failure_analysis = self.categorize_failures(failed_tests)
        
        # Generate specific feedback
        feedback_message = self.generate_feedback_message(failure_analysis, test_results)
        
        return {
            'needs_feedback': True,
            'message': feedback_message,
            'feedback_type': 'improvement_needed',
            'failed_tests': failed_tests,
            'failure_analysis': failure_analysis,
            'iteration': self.iteration_count + 1
        }
    
    def categorize_failures(self, failed_tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Categorize different types of test failures"""
        categories = {
            'syntax_errors': [],
            'logic_errors': [],
            'edge_case_failures': [],
            'performance_issues': [],
            'type_errors': [],
            'other_errors': []
        }
        
        for test in failed_tests:
            error = test.get('error', '').lower()
            test_id = test.get('test_id', '')
            
            if 'syntax' in error or 'invalid syntax' in error:
                categories['syntax_errors'].append(test)
            elif 'type' in error or 'attribute' in error:
                categories['type_errors'].append(test)
            elif 'edge' in test_id or 'empty' in test_id or 'single' in test_id:
                categories['edge_case_failures'].append(test)
            elif 'timeout' in error or 'time' in error:
                categories['performance_issues'].append(test)
            elif test.get('actual') != test.get('expected'):
                categories['logic_errors'].append(test)
            else:
                categories['other_errors'].append(test)
        
        return categories
    
    def generate_feedback_message(self, failure_analysis: Dict[str, Any], test_results: Dict[str, Any]) -> str:
        """Generate detailed feedback message for the code generator"""
        feedback_parts = []
        
        feedback_parts.append(f"**Feedback Analysis - Iteration {self.iteration_count + 1}/{self.max_iterations}**\n")
        
        # Failed test summary
        failed_count = len([t for t in test_results['test_results'] if not t['passed'] or t['error']])
        total_count = test_results['total_tests']
        feedback_parts.append(f"**Test Results:** {test_results['passed_tests']}/{total_count} passed ({failed_count} failed)\n")
        
        # Detailed failure analysis
        feedback_parts.append("**Failed Test Cases:**")
        for test in test_results['test_results']:
            if not test['passed'] or test['error']:
                feedback_parts.append(f"- **{test['description']}**")
                if test['error']:
                    feedback_parts.append(f"  - Error: {test['error']}")
                else:
                    feedback_parts.append(f"  - Expected: {test['expected']}")
                    feedback_parts.append(f"  - Got: {test['actual']}")
        
        feedback_parts.append("\n**Root Cause Analysis:**")
        
        # Analyze each category
        if failure_analysis['syntax_errors']:
            feedback_parts.append("- **Syntax Issues:** Code has syntax errors that prevent execution")
        
        if failure_analysis['type_errors']:
            feedback_parts.append("- **Type Issues:** Incorrect data types or missing attributes")
        
        if failure_analysis['logic_errors']:
            feedback_parts.append("- **Logic Issues:** Algorithm produces incorrect results")
        
        if failure_analysis['edge_case_failures']:
            feedback_parts.append("- **Edge Case Issues:** Solution doesn't handle edge cases properly")
        
        if failure_analysis['performance_issues']:
            feedback_parts.append("- **Performance Issues:** Solution may be too slow")
        
        # Specific instructions
        feedback_parts.append("\n**Specific Instructions for Code Generator:**")
        instructions = self.generate_specific_instructions(failure_analysis)
        for i, instruction in enumerate(instructions, 1):
            feedback_parts.append(f"{i}. {instruction}")
        
        # Code generation request
        feedback_parts.append("\n**Code Generation Request:**")
        feedback_parts.append("Please regenerate the solution addressing the above issues. Focus on:")
        focus_areas = self.generate_focus_areas(failure_analysis)
        for area in focus_areas:
            feedback_parts.append(f"- {area}")
        
        if self.iteration_count + 1 >= self.max_iterations:
            feedback_parts.append(f"\n⚠️ **Final Iteration:** This is iteration {self.iteration_count + 1} of {self.max_iterations}. Please ensure all issues are addressed.")
        
        return "\n".join(feedback_parts)
    
    def generate_specific_instructions(self, failure_analysis: Dict[str, Any]) -> List[str]:
        """Generate specific instructions based on failure types"""
        instructions = []
        
        if failure_analysis['syntax_errors']:
            instructions.append("Fix all syntax errors and ensure code is valid Python")
        
        if failure_analysis['type_errors']:
            instructions.append("Check data types and ensure proper attribute access")
        
        if failure_analysis['logic_errors']:
            instructions.append("Review the algorithm logic and fix incorrect calculations")
        
        if failure_analysis['edge_case_failures']:
            instructions.append("Add proper handling for edge cases (empty inputs, single elements, etc.)")
        
        if failure_analysis['performance_issues']:
            instructions.append("Optimize the algorithm for better time complexity")
        
        if not any(failure_analysis.values()):
            instructions.append("Review the problem requirements and ensure complete implementation")
        
        return instructions
    
    def generate_focus_areas(self, failure_analysis: Dict[str, Any]) -> List[str]:
        """Generate focus areas for code regeneration"""
        focus_areas = []
        
        if failure_analysis['syntax_errors']:
            focus_areas.append("Code syntax and structure")
        
        if failure_analysis['logic_errors']:
            focus_areas.append("Algorithm correctness and logic flow")
        
        if failure_analysis['edge_case_failures']:
            focus_areas.append("Edge case handling and input validation")
        
        if failure_analysis['type_errors']:
            focus_areas.append("Data type consistency and object handling")
        
        if failure_analysis['performance_issues']:
            focus_areas.append("Algorithm efficiency and optimization")
        
        if not focus_areas:
            focus_areas.append("Overall problem understanding and implementation")
        
        return focus_areas
    
    def should_continue_feedback(self) -> bool:
        """Determine if feedback loop should continue"""
        return self.iteration_count < self.max_iterations
    
    def increment_iteration(self):
        """Increment the iteration counter"""
        self.iteration_count += 1
    
    def reset(self):
        """Reset the feedback loop for a new problem"""
        self.iteration_count = 0
        self.feedback_history = []
    
    def add_to_history(self, feedback_data: Dict[str, Any]):
        """Add feedback data to history"""
        self.feedback_history.append({
            'iteration': self.iteration_count,
            'feedback_data': feedback_data
        })
    
    def get_feedback_summary(self) -> str:
        """Get a summary of all feedback iterations"""
        if not self.feedback_history:
            return "No feedback iterations recorded."
        
        summary = [f"**Feedback Loop Summary - {len(self.feedback_history)} iterations:**\n"]
        
        for entry in self.feedback_history:
            iteration = entry['iteration']
            feedback = entry['feedback_data']
            summary.append(f"**Iteration {iteration}:**")
            summary.append(f"- Feedback Type: {feedback.get('feedback_type', 'unknown')}")
            if 'failed_tests' in feedback:
                summary.append(f"- Failed Tests: {len(feedback['failed_tests'])}")
            summary.append("")
        
        return "\n".join(summary)
