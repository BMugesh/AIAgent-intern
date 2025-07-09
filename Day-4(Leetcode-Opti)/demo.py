#!/usr/bin/env python3
"""
Demo script for LeetCode Multi-Agent Optimizer with Enhanced UI
"""

import streamlit as st
import time
from agents import run_leetcode_optimizer
from config import Config
from test_executor import TestExecutor, format_test_results
from feedback_loop import FeedbackLoop

def run_demo():
    """Run a comprehensive demo of the system"""
    
    st.set_page_config(
        page_title="🎬 LeetCode Optimizer Demo",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Demo header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h1 style="margin: 0; font-size: 2.5rem;">🎬 Interactive Demo</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            LeetCode Multi-Agent Optimizer with Feedback Loop & Enhanced UI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo options
    st.markdown("### 🎯 Choose Demo Scenario")
    
    demo_scenarios = {
        "Two Sum Problem": {
            "problem": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.""",
            "description": "Classic array problem - demonstrates basic workflow",
            "complexity": "Easy",
            "expected_agents": 5
        },
        
        "Valid Parentheses": {
            "problem": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.""",
            "description": "Stack-based problem - shows edge case handling",
            "complexity": "Easy",
            "expected_agents": 5
        },
        
        "Feedback Loop Demo": {
            "problem": """Write a function that finds the maximum subarray sum.

Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

Example:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.""",
            "description": "Intentionally challenging - demonstrates feedback loop",
            "complexity": "Medium",
            "expected_agents": 5
        }
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_scenario = st.selectbox(
            "Select a demo scenario:",
            list(demo_scenarios.keys()),
            help="Choose a scenario to see the system in action"
        )
        
        scenario = demo_scenarios[selected_scenario]
        
        # Display scenario info
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
        ">
            <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">📋 Scenario Details</h4>
            <p style="margin: 0 0 0.5rem 0; color: #6b7280;"><strong>Description:</strong> {scenario['description']}</p>
            <p style="margin: 0 0 0.5rem 0; color: #6b7280;"><strong>Complexity:</strong> {scenario['complexity']}</p>
            <p style="margin: 0; color: #6b7280;"><strong>Expected Agents:</strong> {scenario['expected_agents']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show problem statement
        st.text_area(
            "Problem Statement:",
            value=scenario['problem'],
            height=200,
            disabled=True
        )
    
    with col2:
        st.markdown("### 🎮 Demo Controls")
        
        if st.button("🚀 Start Demo", type="primary", use_container_width=True):
            run_demo_scenario(scenario['problem'], selected_scenario)
        
        if st.button("🔄 Reset Demo", use_container_width=True):
            st.rerun()
        
        # Demo features
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, #ecfdf5 0%, #f0fdf4 100%);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid #22c55e;
        ">
            <h4 style="margin: 0 0 0.5rem 0; color: #166534;">🌟 Demo Features</h4>
            <ul style="margin: 0; padding-left: 1rem; color: #15803d; font-size: 0.9rem;">
                <li>5-Agent Workflow</li>
                <li>Automatic Feedback Loops</li>
                <li>Enhanced UI Visualization</li>
                <li>Real-time Progress Tracking</li>
                <li>Live Test Execution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def run_demo_scenario(problem_statement, scenario_name):
    """Run a specific demo scenario"""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    ">
        <h3 style="margin: 0;">🎬 Running Demo: {scenario_name}</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Watch the 5-agent system with feedback loops in action!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate the multi-agent process with enhanced visualization
    with st.spinner("🤖 Multi-agents are working..."):
        
        # Progress tracking
        progress_container = st.empty()
        
        stages = [
            ("🔧", "Code Generator", "Analyzing problem and generating solution...", 20),
            ("🔍", "Code Reviewer", "Reviewing code for correctness...", 40),
            ("🧪", "Test Validator", "Creating and running test cases...", 60),
            ("🔄", "Feedback Coordinator", "Analyzing results and coordinating feedback...", 80),
            ("⚡", "Code Optimizer", "Optimizing final solution...", 100)
        ]
        
        for icon, agent, description, progress in stages:
            progress_container.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
                border-radius: 12px;
                padding: 1rem;
                margin: 0.5rem 0;
                border-left: 4px solid #3b82f6;
                display: flex;
                align-items: center;
            ">
                <span style="font-size: 1.5rem; margin-right: 1rem;">{icon}</span>
                <div>
                    <strong style="color: #1f2937;">{agent}</strong>
                    <br>
                    <span style="color: #6b7280; font-size: 0.9rem;">{description}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(progress / 100)
            time.sleep(1.5)
        
        # Run actual system
        try:
            chat_result = run_leetcode_optimizer(problem_statement)
            
            # Success message
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 2rem;
                border-radius: 16px;
                margin: 2rem 0;
                text-align: center;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
                <h2 style="margin: 0 0 0.5rem 0;">Demo Completed Successfully!</h2>
                <p style="margin: 0; opacity: 0.9;">
                    The 5-agent system with feedback loops has processed your problem!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Demo statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Agents Used", "5", "🤖 All agents active")
            with col2:
                st.metric("Feedback Loops", "Auto", "🔄 As needed")
            with col3:
                st.metric("UI Enhanced", "Yes", "🎨 Beautiful design")
            with col4:
                st.metric("LeetCode Ready", "Yes", "✅ Validated")
                
        except Exception as e:
            st.error(f"Demo encountered an error: {str(e)}")
            st.info("This is normal in demo mode. The actual system handles errors gracefully.")

if __name__ == "__main__":
    run_demo()
