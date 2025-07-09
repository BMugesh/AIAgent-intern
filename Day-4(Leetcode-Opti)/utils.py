"""
Utility functions for LeetCode Multi-Agent Optimizer
"""

import re
import streamlit as st
from typing import List, Dict, Any
import time

def extract_code_blocks(text: str) -> List[str]:
    """Extract Python code blocks from text"""
    pattern = r'```python\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def extract_complexity_analysis(text: str) -> Dict[str, str]:
    """Extract time and space complexity from text"""
    time_pattern = r'Time Complexity:\s*O\(([^)]+)\)'
    space_pattern = r'Space Complexity:\s*O\(([^)]+)\)'
    
    time_match = re.search(time_pattern, text, re.IGNORECASE)
    space_match = re.search(space_pattern, text, re.IGNORECASE)
    
    return {
        'time': f"O({time_match.group(1)})" if time_match else "Not specified",
        'space': f"O({space_match.group(1)})" if space_match else "Not specified"
    }

def format_agent_response(agent_name: str, content: str) -> str:
    """Format agent response for better display"""
    agent_icons = {
        'CodeGenerator': '🔧',
        'CodeReviewer': '🔍',
        'CodeOptimizer': '⚡',
        'UserProxy': '👤'
    }
    
    icon = agent_icons.get(agent_name, '🤖')
    return f"### {icon} {agent_name}\n\n{content}"

def display_progress_steps():
    """Display progress steps for the multi-agent process"""
    steps = [
        ("🔧 Code Generator", "Analyzing problem and generating solution..."),
        ("🔍 Code Reviewer", "Reviewing code for correctness and improvements..."),
        ("⚡ Code Optimizer", "Optimizing code for better performance..."),
        ("✅ Complete", "All agents have finished their work!")
    ]
    
    return steps

def create_download_link(content: str, filename: str, link_text: str) -> str:
    """Create a download link for content"""
    import base64
    
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def validate_problem_input(problem_text: str) -> tuple[bool, str]:
    """Validate the problem input"""
    if not problem_text.strip():
        return False, "Problem statement cannot be empty"
    
    if len(problem_text.strip()) < 50:
        return False, "Problem statement seems too short. Please provide a complete problem description."
    
    # Check for common LeetCode problem elements
    required_elements = ['example', 'input', 'output']
    has_elements = any(element.lower() in problem_text.lower() for element in required_elements)
    
    if not has_elements:
        return False, "Problem statement should include examples with input/output"
    
    return True, "Valid problem statement"

def parse_chat_history(chat_result) -> List[Dict[str, Any]]:
    """Parse chat history from autogen result"""
    messages = []
    
    if hasattr(chat_result, 'chat_history') and chat_result.chat_history:
        for message in chat_result.chat_history:
            if isinstance(message, dict):
                name = message.get('name', 'Unknown')
                content = message.get('content', '')
                
                # Skip empty messages or system messages
                if not content.strip() or name == 'UserProxy':
                    continue
                
                messages.append({
                    'agent': name,
                    'content': content,
                    'code_blocks': extract_code_blocks(content),
                    'complexity': extract_complexity_analysis(content)
                })
    
    return messages

def display_code_with_syntax_highlighting(code: str, language: str = "python"):
    """Display code with syntax highlighting"""
    st.code(code, language=language)

def create_agent_summary(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a summary of agent contributions"""
    summary = {
        'total_messages': len(messages),
        'agents_participated': set(),
        'code_blocks_generated': 0,
        'optimizations_made': 0
    }
    
    for message in messages:
        summary['agents_participated'].add(message['agent'])
        summary['code_blocks_generated'] += len(message['code_blocks'])
        
        if 'optimization' in message['content'].lower():
            summary['optimizations_made'] += 1
    
    summary['agents_participated'] = list(summary['agents_participated'])
    return summary

def export_results_to_markdown(messages: List[Dict[str, Any]], problem_statement: str) -> str:
    """Export results to markdown format"""
    markdown_content = f"""# LeetCode Problem Solution

## Problem Statement
{problem_statement}

## Agent Solutions

"""
    
    for message in messages:
        markdown_content += f"### {message['agent']}\n\n"
        markdown_content += f"{message['content']}\n\n"
        
        if message['code_blocks']:
            for i, code in enumerate(message['code_blocks']):
                markdown_content += f"```python\n{code}\n```\n\n"
        
        markdown_content += "---\n\n"
    
    return markdown_content

def get_agent_color(agent_name: str) -> str:
    """Get color for agent based on name"""
    colors = {
        'CodeGenerator': '#FF6B6B',
        'CodeReviewer': '#4ECDC4',
        'CodeOptimizer': '#45B7D1',
        'UserProxy': '#96CEB4'
    }
    return colors.get(agent_name, '#95A5A6')

def animate_typing_effect(text: str, delay: float = 0.05):
    """Create a typing animation effect"""
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)
    
    return placeholder

def check_code_quality(code: str) -> Dict[str, Any]:
    """Basic code quality checks"""
    quality_metrics = {
        'has_comments': '#' in code,
        'has_docstring': '"""' in code or "'''" in code,
        'line_count': len(code.split('\n')),
        'has_error_handling': 'try' in code and 'except' in code,
        'follows_pep8': True  # Simplified check
    }
    
    # Calculate quality score
    score = sum([
        quality_metrics['has_comments'],
        quality_metrics['has_docstring'],
        quality_metrics['line_count'] > 5,
        quality_metrics['has_error_handling']
    ]) / 4 * 100
    
    quality_metrics['quality_score'] = score
    return quality_metrics
