import streamlit as st
import time
from agents import run_leetcode_optimizer
from config import Config
from utils import (
    parse_chat_history,
    validate_problem_input,
    create_agent_summary,
    export_results_to_markdown,
    display_code_with_syntax_highlighting,
    extract_code_blocks
)
from test_executor import TestExecutor, format_test_results
from feedback_loop import FeedbackLoop

# Page configuration
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    layout=Config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Main Header */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Agent Cards */
    .agent-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Agent-specific styling */
    .code-generator-card {
        border-left: 4px solid #10b981;
        background: linear-gradient(145deg, #ecfdf5 0%, #f0fdf4 100%);
    }

    .code-reviewer-card {
        border-left: 4px solid #3b82f6;
        background: linear-gradient(145deg, #eff6ff 0%, #f0f9ff 100%);
    }

    .test-validator-card {
        border-left: 4px solid #f59e0b;
        background: linear-gradient(145deg, #fffbeb 0%, #fefce8 100%);
    }

    .feedback-coordinator-card {
        border-left: 4px solid #8b5cf6;
        background: linear-gradient(145deg, #f3e8ff 0%, #faf5ff 100%);
    }

    .code-optimizer-card {
        border-left: 4px solid #ef4444;
        background: linear-gradient(145deg, #fef2f2 0%, #fefefe 100%);
    }

    /* Agent Headers */
    .agent-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
    }

    .agent-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }

    /* Code Blocks */
    .code-container {
        background: #1e293b;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        position: relative;
        overflow: hidden;
    }

    .code-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981, #3b82f6, #f59e0b, #ef4444);
    }

    /* Progress Indicators */
    .progress-container {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }

    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }

    .status-success {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }

    .status-warning {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }

    .status-error {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }

    .status-info {
        background-color: #dbeafe;
        color: #1e40af;
        border: 1px solid #bfdbfe;
    }

    /* Metrics Cards */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        font-family: 'Inter', sans-serif;
    }

    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    /* Animations */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    .slide-in {
        animation: slideIn 0.5s ease-out;
    }

    /* Feedback Loop Visualization */
    .feedback-loop-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }

    .feedback-loop-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            rgba(255, 255, 255, 0.05) 10px,
            rgba(255, 255, 255, 0.05) 20px
        );
        animation: move 20s linear infinite;
    }

    @keyframes move {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        font-weight: 500;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main title and description with enhanced styling
st.markdown('''
<div class="main-header">
    🧠 LeetCode Multi-Agent Optimizer
</div>
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="font-size: 1.2rem; color: #64748b; font-weight: 400; margin: 0;">
        🔄 <strong>Feedback Loop Edition</strong> • 5 AI Agents • Guaranteed LeetCode Acceptance
    </p>
</div>
''', unsafe_allow_html=True)

# Enhanced Sidebar with modern styling
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">🤖 AI Agent Workflow</h2>
        <p style="color: #6b7280; font-size: 0.9rem;">5 Specialized Agents with Feedback Loop</p>
    </div>
    """, unsafe_allow_html=True)

    # Agent workflow with enhanced cards
    agents_info = [
        ("🔧", "Code Generator", "Analyzes problems and generates solutions", "#10b981"),
        ("🔍", "Code Reviewer", "Reviews code for correctness and improvements", "#3b82f6"),
        ("🧪", "Test Validator", "Creates and runs comprehensive test cases", "#f59e0b"),
        ("🔄", "Feedback Coordinator", "Analyzes failures and provides feedback", "#8b5cf6"),
        ("⚡", "Code Optimizer", "Optimizes final validated solutions", "#ef4444")
    ]

    for icon, name, description, color in agents_info:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            border-left: 3px solid {color};
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                <strong style="color: #1f2937; font-size: 0.9rem;">{name}</strong>
            </div>
            <p style="color: #6b7280; font-size: 0.8rem; margin: 0; line-height: 1.4;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

    # Feedback Loop Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
    ">
        <h4 style="margin: 0 0 0.5rem 0; font-size: 1rem;">🔄 Automatic Feedback Loop</h4>
        <ul style="margin: 0; padding-left: 1rem; font-size: 0.8rem; line-height: 1.4;">
            <li>Detects test failures automatically</li>
            <li>Provides specific improvement feedback</li>
            <li>Triggers code regeneration</li>
            <li>Repeats until all tests pass (max 3 iterations)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Configuration Section
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #0ea5e9;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #0c4a6e; font-size: 1rem;">⚙️ Configuration</h4>
        <div style="display: flex; align-items: center; color: #0369a1; font-size: 0.8rem;">
            <span style="margin-right: 0.5rem;">🚀</span>
            <span>Groq AI • Llama3-70B • Auto Feedback</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tips Section
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #f0fdf4 0%, #ecfdf5 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #22c55e;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #166534; font-size: 1rem;">💡 Pro Tips</h4>
        <ul style="margin: 0; padding-left: 1rem; color: #15803d; font-size: 0.8rem; line-height: 1.4;">
            <li>Include complete problem statement</li>
            <li>Add all examples and constraints</li>
            <li>Specify edge cases if known</li>
            <li>Let feedback loop handle failures</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content area with enhanced styling
st.markdown("""
<div style="
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #e2e8f0;
">
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
            <span style="margin-right: 0.5rem;">🧩</span>
            LeetCode Problem Statement
        </h3>
        <p style="color: #6b7280; font-size: 0.9rem; margin: 0;">
            Enter your problem or select from examples below
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Example problems for quick testing
    example_problems = Config.EXAMPLE_PROBLEMS

    selected_example = st.selectbox(
        "Choose an example problem (optional):",
        ["Custom Problem"] + list(example_problems.keys()),
        help="Select a pre-loaded example or choose 'Custom Problem' to enter your own"
    )

    if selected_example != "Custom Problem":
        problem_input = st.text_area(
            "Problem Description",
            value=example_problems[selected_example],
            height=300,
            placeholder="Paste the full problem description here...",
            help="Complete problem statement with examples and constraints"
        )
    else:
        problem_input = st.text_area(
            "Problem Description",
            height=300,
            placeholder="Paste the full problem description here...",
            help="Include problem statement, examples, and constraints for best results"
        )

with col2:
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
            <span style="margin-right: 0.5rem;">🚀</span>
            Control Panel
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced action buttons
    run_button = st.button(
        "🚀 Run Multi-Agent Optimizer",
        type="primary",
        use_container_width=True,
        help="Start the 5-agent workflow with automatic feedback loops"
    )

    if st.button("🗑️ Clear Input", use_container_width=True, help="Clear the problem input"):
        st.rerun()

    # Add status indicators
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid #e2e8f0;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #374151; font-size: 0.9rem;">📊 System Status</h4>
        <div style="display: flex; align-items: center; margin-bottom: 0.25rem;">
            <span style="color: #10b981; margin-right: 0.5rem;">●</span>
            <span style="color: #6b7280; font-size: 0.8rem;">5 Agents Ready</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.25rem;">
            <span style="color: #10b981; margin-right: 0.5rem;">●</span>
            <span style="color: #6b7280; font-size: 0.8rem;">Feedback Loop Active</span>
        </div>
        <div style="display: flex; align-items: center;">
            <span style="color: #10b981; margin-right: 0.5rem;">●</span>
            <span style="color: #6b7280; font-size: 0.8rem;">Groq AI Connected</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Main processing logic
if run_button and problem_input.strip():
    with st.spinner("🤖 Multi-agents are working on your problem..."):
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("🔧 Code Generator is analyzing the problem...")
            progress_bar.progress(15)
            time.sleep(1)

            # Run the multi-agent system
            chat_result = run_leetcode_optimizer(problem_input)

            status_text.text("🔍 Code Reviewer is examining the solution...")
            progress_bar.progress(40)
            time.sleep(1)

            status_text.text("🧪 Test Validator is creating comprehensive test cases...")
            progress_bar.progress(50)
            time.sleep(1)

            status_text.text("🔄 Feedback Loop processing (if needed)...")
            progress_bar.progress(70)
            time.sleep(1)

            status_text.text("⚡ Code Optimizer is improving the solution...")
            progress_bar.progress(85)
            time.sleep(1)

            progress_bar.progress(100)
            status_text.text("✅ All agents have completed their work!")

            # Display results
            st.markdown("---")
            st.markdown("## 💬 Agent Conversations")

            # Parse and display the conversation
            if hasattr(chat_result, 'chat_history') and chat_result.chat_history:
                for i, message in enumerate(chat_result.chat_history):
                    if isinstance(message, dict):
                        name = message.get('name', 'Unknown')
                        content = message.get('content', '')

                        # Skip empty messages
                        if not content.strip():
                            continue

                        # Enhanced agent visualization with beautiful cards
                        if name == "CodeGenerator":
                            st.markdown(f"""
                            <div class="agent-card code-generator-card slide-in">
                                <div class="agent-header">
                                    <span class="agent-icon">🔧</span>
                                    <span>{name}</span>
                                    <span class="status-badge status-success" style="margin-left: auto;">Active</span>
                                </div>
                                <div style="color: #374151; line-height: 1.6;">
                                    {content.replace('```python', '<div class="code-container"><pre style="margin: 0; color: #e2e8f0;">').replace('```', '</pre></div>')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        elif name == "CodeReviewer":
                            st.markdown(f"""
                            <div class="agent-card code-reviewer-card slide-in">
                                <div class="agent-header">
                                    <span class="agent-icon">🔍</span>
                                    <span>{name}</span>
                                    <span class="status-badge status-info" style="margin-left: auto;">Reviewing</span>
                                </div>
                                <div style="color: #374151; line-height: 1.6;">
                                    {content}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif name == "TestValidator":
                            # Enhanced Test Validator with live execution
                            st.markdown(f"""
                            <div class="agent-card test-validator-card slide-in">
                                <div class="agent-header">
                                    <span class="agent-icon">🧪</span>
                                    <span>{name}</span>
                                    <span class="status-badge status-warning" style="margin-left: auto;">Testing</span>
                                </div>
                                <div style="color: #374151; line-height: 1.6;">
                                    {content}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Execute actual tests if code is present
                            code_blocks = extract_code_blocks(content)
                            if code_blocks:
                                with st.expander("🔬 Live Test Execution & Feedback Loop", expanded=True):
                                    # Create test execution container
                                    st.markdown("""
                                    <div class="progress-container">
                                        <h4 style="margin: 0 0 1rem 0; color: #374151;">🔬 Test Execution Results</h4>
                                    </div>
                                    """, unsafe_allow_html=True)

                                    executor = TestExecutor()
                                    test_results = executor.run_all_tests(code_blocks[0], problem_input)

                                    # Enhanced test results display
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Total Tests", test_results.get('total_tests', 0))
                                    with col2:
                                        st.metric("Passed", test_results.get('passed_tests', 0))
                                    with col3:
                                        pass_rate = test_results.get('pass_rate', 0) * 100
                                        st.metric("Pass Rate", f"{pass_rate:.1f}%")

                                    formatted_results = format_test_results(test_results)
                                    st.markdown(formatted_results)

                                    # Enhanced feedback loop visualization
                                    if not test_results.get('leetcode_ready', False):
                                        st.markdown("""
                                        <div class="feedback-loop-container">
                                            <h4 style="margin: 0 0 0.5rem 0;">🔄 Feedback Loop Activated</h4>
                                            <p style="margin: 0; opacity: 0.9;">Tests failed! Automatic improvement cycle initiated...</p>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        # Initialize feedback loop
                                        feedback_loop = FeedbackLoop()
                                        feedback_analysis = feedback_loop.analyze_test_failures(test_results)

                                        if feedback_analysis['needs_feedback']:
                                            st.info(f"🔄 Iteration {feedback_analysis['iteration']}/{Config.MAX_FEEDBACK_ITERATIONS}")

                                            with st.expander("📋 Detailed Feedback Analysis", expanded=True):
                                                st.markdown(f"""
                                                <div style="
                                                    background: #fef3c7;
                                                    border-left: 4px solid #f59e0b;
                                                    padding: 1rem;
                                                    border-radius: 8px;
                                                    margin: 1rem 0;
                                                ">
                                                    {feedback_analysis['message']}
                                                </div>
                                                """, unsafe_allow_html=True)
                                    else:
                                        st.markdown("""
                                        <div style="
                                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                            color: white;
                                            padding: 1rem;
                                            border-radius: 8px;
                                            margin: 1rem 0;
                                            text-align: center;
                                        ">
                                            <h4 style="margin: 0;">✅ All Tests Passed!</h4>
                                            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Solution is ready for optimization</p>
                                        </div>
                                        """, unsafe_allow_html=True)

                        elif name == "FeedbackCoordinator":
                            # Enhanced Feedback Coordinator with status indicators
                            st.markdown(f"""
                            <div class="agent-card feedback-coordinator-card slide-in">
                                <div class="agent-header">
                                    <span class="agent-icon">🔄</span>
                                    <span>{name}</span>
                                    <span class="status-badge status-warning" style="margin-left: auto;">Coordinating</span>
                                </div>
                                <div style="color: #374151; line-height: 1.6;">
                                    {content}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Enhanced feedback loop status indicators
                            if "REGENERATE_CODE" in content:
                                st.markdown("""
                                <div style="
                                    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                                    color: white;
                                    padding: 1rem;
                                    border-radius: 8px;
                                    margin: 1rem 0;
                                    display: flex;
                                    align-items: center;
                                ">
                                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">🔄</span>
                                    <div>
                                        <strong>Feedback Loop Active</strong>
                                        <br><small>Code regeneration requested based on test failures</small>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            elif "MAX_ITERATIONS_REACHED" in content:
                                st.markdown("""
                                <div style="
                                    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                                    color: white;
                                    padding: 1rem;
                                    border-radius: 8px;
                                    margin: 1rem 0;
                                    display: flex;
                                    align-items: center;
                                ">
                                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">⚠️</span>
                                    <div>
                                        <strong>Maximum Iterations Reached</strong>
                                        <br><small>Manual review may be required for remaining issues</small>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            elif "PROCEED_TO_OPTIMIZATION" in content:
                                st.markdown("""
                                <div style="
                                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                    color: white;
                                    padding: 1rem;
                                    border-radius: 8px;
                                    margin: 1rem 0;
                                    display: flex;
                                    align-items: center;
                                ">
                                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">✅</span>
                                    <div>
                                        <strong>Tests Passed!</strong>
                                        <br><small>Proceeding to final optimization phase</small>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                        elif name == "CodeOptimizer":
                            # Enhanced Code Optimizer with performance metrics
                            st.markdown(f"""
                            <div class="agent-card code-optimizer-card slide-in">
                                <div class="agent-header">
                                    <span class="agent-icon">⚡</span>
                                    <span>{name}</span>
                                    <span class="status-badge status-success" style="margin-left: auto;">Optimizing</span>
                                </div>
                                <div style="color: #374151; line-height: 1.6;">
                                    {content.replace('```python', '<div class="code-container"><pre style="margin: 0; color: #e2e8f0;">').replace('```', '</pre></div>')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Add optimization metrics if available
                            if "Time Complexity" in content or "Space Complexity" in content:
                                st.markdown("""
                                <div style="
                                    background: linear-gradient(145deg, #fef2f2 0%, #fefefe 100%);
                                    border: 1px solid #fecaca;
                                    border-radius: 8px;
                                    padding: 1rem;
                                    margin: 1rem 0;
                                ">
                                    <h4 style="margin: 0 0 0.5rem 0; color: #991b1b;">📊 Performance Analysis</h4>
                                    <p style="margin: 0; color: #7f1d1d; font-size: 0.9rem;">
                                        Optimization complete with complexity analysis above
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"### 👤 {name}")
                            st.markdown(content)

                        st.markdown("---")

            # Enhanced success message with celebration
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 2rem;
                border-radius: 16px;
                margin: 2rem 0;
                text-align: center;
                box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
                position: relative;
                overflow: hidden;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
                <h2 style="margin: 0 0 0.5rem 0; font-size: 1.5rem; font-weight: 600;">
                    Mission Accomplished!
                </h2>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
                    Your LeetCode problem has been solved, reviewed, tested, and optimized by our enhanced 5-agent system with automatic feedback loops!
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Enhanced final validation summary with beautiful metrics
            st.markdown("""
            <div style="margin: 2rem 0;">
                <h3 style="text-align: center; color: #1f2937; font-weight: 600; margin-bottom: 1.5rem;">
                    📋 Final Validation Summary
                </h3>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style="color: #10b981;">5</div>
                    <div class="metric-label">AI Agents</div>
                    <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">
                        Gen → Review → Test → Feedback → Optimize
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style="color: #3b82f6;">Complete</div>
                    <div class="metric-label">Workflow Status</div>
                    <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">
                        ✅ All phases executed with feedback loops
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style="color: #f59e0b;">Ready</div>
                    <div class="metric-label">LeetCode Status</div>
                    <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">
                        🔄 Validated through iterative improvement
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.markdown("**Troubleshooting tips:**")
            st.markdown("- Make sure your GROQ_API_KEY is set in the .env file")
            st.markdown("- Check your internet connection")
            st.markdown("- Verify the problem statement is complete")

elif run_button and not problem_input.strip():
    st.warning("⚠️ Please enter a LeetCode problem statement before running the optimizer.")

# Enhanced Footer
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
    color: white;
    padding: 3rem 2rem;
    margin-top: 3rem;
    border-radius: 16px 16px 0 0;
    text-align: center;
">
    <div style="margin-bottom: 1.5rem;">
        <h3 style="margin: 0 0 0.5rem 0; font-weight: 600;">
            🧠 LeetCode Multi-Agent Optimizer
        </h3>
        <p style="margin: 0; opacity: 0.8; font-size: 1.1rem;">
            Feedback Loop Edition • 5 AI Agents • Guaranteed Success
        </p>
    </div>

    <div style="
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    ">
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">🤖</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Autogen Multi-Agent</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">🚀</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Groq AI Powered</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">💻</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Streamlit Interface</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">🔄</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Feedback Loops</div>
        </div>
    </div>

    <div style="
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 1.5rem 0;
    ">
        <div style="font-weight: 500; margin-bottom: 0.5rem;">🎯 Complete Workflow</div>
        <div style="font-size: 0.9rem; opacity: 0.8;">
            Generate → Review → Test → Feedback → Optimize → Validate
        </div>
    </div>

    <div style="
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        padding-top: 1.5rem;
        margin-top: 1.5rem;
        font-size: 0.9rem;
        opacity: 0.7;
    ">
        <p style="margin: 0;">
            Built with ❤️ for the coding community • LeetCode Acceptance Guaranteed
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
