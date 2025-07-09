from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from config import Config

def groq_llm_config():
    """Configuration for Groq LLM to work with Autogen"""
    # Validate configuration first
    Config.validate_config()

    return {
        "config_list": [
            {
                "model": Config.GROQ_MODEL,
                "api_key": Config.GROQ_API_KEY,
                "base_url": Config.GROQ_BASE_URL,
                "api_type": "openai"
            }
        ],
        "temperature": Config.AGENT_TEMPERATURE,
        "timeout": Config.AGENT_TIMEOUT,
    }

def get_agents():
    """Create and return the five specialized agents with feedback loop support"""

    # Code Generator Agent (Enhanced for feedback)
    code_generator = AssistantAgent(
        name="CodeGenerator",
        llm_config=groq_llm_config(),
        system_message=Config.CODE_GENERATOR_PROMPT + """

**FEEDBACK LOOP INSTRUCTIONS:**
When you receive feedback about failed test cases:
1. Carefully analyze the specific failures mentioned
2. Identify the root cause of each failure
3. Generate an improved solution that addresses ALL the issues
4. Pay special attention to edge cases that previously failed
5. Ensure your new solution handles the specific scenarios mentioned in the feedback
""",
        max_consecutive_auto_reply=Config.MAX_CONSECUTIVE_AUTO_REPLY,
    )

    # Code Reviewer Agent
    code_reviewer = AssistantAgent(
        name="CodeReviewer",
        llm_config=groq_llm_config(),
        system_message=Config.CODE_REVIEWER_PROMPT,
        max_consecutive_auto_reply=Config.MAX_CONSECUTIVE_AUTO_REPLY,
    )

    # Test Validator Agent
    test_validator = AssistantAgent(
        name="TestValidator",
        llm_config=groq_llm_config(),
        system_message=Config.TEST_VALIDATOR_PROMPT,
        max_consecutive_auto_reply=Config.MAX_CONSECUTIVE_AUTO_REPLY,
    )

    # Feedback Coordinator Agent
    feedback_coordinator = AssistantAgent(
        name="FeedbackCoordinator",
        llm_config=groq_llm_config(),
        system_message=Config.FEEDBACK_COORDINATOR_PROMPT,
        max_consecutive_auto_reply=Config.MAX_CONSECUTIVE_AUTO_REPLY,
    )

    # Code Optimizer Agent
    code_optimizer = AssistantAgent(
        name="CodeOptimizer",
        llm_config=groq_llm_config(),
        system_message=Config.CODE_OPTIMIZER_PROMPT,
        max_consecutive_auto_reply=Config.MAX_CONSECUTIVE_AUTO_REPLY,
    )

    return code_generator, code_reviewer, test_validator, feedback_coordinator, code_optimizer

def create_group_chat(agents):
    """Create a group chat with the agents including feedback loop support"""
    code_generator, code_reviewer, test_validator, feedback_coordinator, code_optimizer = agents

    # Create a user proxy to manage the conversation
    user_proxy = UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )

    # Create group chat with enhanced workflow and feedback loop
    groupchat = GroupChat(
        agents=[user_proxy, code_generator, code_reviewer, test_validator, feedback_coordinator, code_optimizer],
        messages=[],
        max_round=Config.MAX_GROUP_CHAT_ROUNDS,
        speaker_selection_method="auto",  # Changed to auto for better feedback loop control
    )

    # Create group chat manager
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=groq_llm_config(),
    )

    return user_proxy, manager

def run_leetcode_optimizer(problem_statement):
    """Run the complete LeetCode optimization pipeline with feedback loop"""

    # Get agents
    agents = get_agents()
    user_proxy, manager = create_group_chat(agents)

    # Enhanced problem statement with clear instructions
    enhanced_prompt = f"""
LeetCode Problem to Solve:
{problem_statement}

Please follow this enhanced workflow with AUTOMATIC FEEDBACK LOOP for LeetCode acceptance:

**INITIAL WORKFLOW:**
1. CodeGenerator: Generate a working solution with proper edge case handling
2. CodeReviewer: Review the code for correctness and improvements
3. TestValidator: Create comprehensive test cases and validate the solution

**AUTOMATIC FEEDBACK LOOP (if tests fail):**
4. FeedbackCoordinator: Analyze failed tests and provide specific feedback to CodeGenerator
5. CodeGenerator: Regenerate solution based on detailed feedback
6. CodeReviewer: Re-review the improved solution
7. TestValidator: Re-test the improved solution
8. Repeat steps 4-7 until all tests pass (maximum 3 feedback iterations)

**FINAL STEP:**
9. CodeOptimizer: Optimize the fully validated solution

**IMPORTANT RULES:**
- If tests fail, AUTOMATICALLY trigger feedback loop
- CodeGenerator must address ALL specific issues mentioned in feedback
- Continue until ALL test cases pass or max iterations reached
- Only proceed to optimization after successful test validation

The goal is to ensure the solution will be ACCEPTED by LeetCode through iterative improvement.

Let's start with the CodeGenerator.
"""

    # Start the conversation with feedback loop support
    chat_result = user_proxy.initiate_chat(
        manager,
        message=enhanced_prompt,
        clear_history=True,
    )

    return chat_result

def run_leetcode_optimizer_with_feedback_loop(problem_statement, max_iterations=3):
    """Enhanced version with explicit feedback loop management"""
    from test_executor import TestExecutor
    from feedback_loop import FeedbackLoop
    from utils import extract_code_blocks

    # Initialize feedback loop components
    feedback_loop = FeedbackLoop()
    test_executor = TestExecutor()

    # Get agents
    agents = get_agents()
    user_proxy, manager = create_group_chat(agents)

    iteration_results = []

    for iteration in range(max_iterations + 1):  # +1 for initial attempt
        # Run the agent conversation
        if iteration == 0:
            # Initial run
            prompt = f"""
LeetCode Problem to Solve:
{problem_statement}

Generate a working solution, review it, and test it comprehensively.
"""
        else:
            # Feedback iteration
            last_feedback = iteration_results[-1]['feedback']
            prompt = f"""
FEEDBACK ITERATION {iteration}/{max_iterations}

Previous solution failed tests. Here's the detailed feedback:

{last_feedback}

Please regenerate the solution addressing ALL the issues mentioned above.
"""

        # Run agents
        chat_result = user_proxy.initiate_chat(
            manager,
            message=prompt,
            clear_history=iteration == 0,  # Clear history only on first iteration
        )

        # Extract code from the latest generator response
        latest_code = None
        if hasattr(chat_result, 'chat_history'):
            for message in reversed(chat_result.chat_history):
                if message.get('name') == 'CodeGenerator':
                    code_blocks = extract_code_blocks(message.get('content', ''))
                    if code_blocks:
                        latest_code = code_blocks[0]
                        break

        if not latest_code:
            break

        # Test the code
        test_results = test_executor.run_all_tests(latest_code, problem_statement)

        # Check if we need feedback
        if test_results.get('leetcode_ready', False):
            # Success! All tests passed
            iteration_results.append({
                'iteration': iteration,
                'chat_result': chat_result,
                'test_results': test_results,
                'success': True,
                'feedback': None
            })
            break

        # Generate feedback for next iteration
        feedback_analysis = feedback_loop.analyze_test_failures(test_results)

        iteration_results.append({
            'iteration': iteration,
            'chat_result': chat_result,
            'test_results': test_results,
            'success': False,
            'feedback': feedback_analysis.get('message', '')
        })

        # Check if we should continue
        if iteration >= max_iterations or not feedback_analysis.get('needs_feedback', False):
            break

        feedback_loop.increment_iteration()

    # Return the final result with all iteration data
    final_result = iteration_results[-1]['chat_result'] if iteration_results else None

    # Add feedback loop metadata
    if final_result and hasattr(final_result, '__dict__'):
        final_result.feedback_loop_data = {
            'total_iterations': len(iteration_results),
            'max_iterations': max_iterations,
            'final_success': iteration_results[-1]['success'] if iteration_results else False,
            'iteration_results': iteration_results
        }

    return final_result
