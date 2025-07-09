# 🧠 LeetCode Multi-Agent Optimizer - Feedback Loop Edition

A powerful **5-agent system** with **automatic feedback loops** that uses **Autogen**, **Groq AI**, and **Streamlit** to solve, review, test, and optimize LeetCode problems with **guaranteed LeetCode acceptance** through iterative improvement.

## 🤖 Enhanced Multi-Agent System with Feedback Loop

This application uses **five specialized AI agents** working together with **automatic feedback loops**:

1. **🔧 Code Generator**: Analyzes problems and generates solutions with edge case handling
2. **🔍 Code Reviewer**: Reviews code for correctness and suggests improvements
3. **🧪 Test Validator**: Creates comprehensive test cases and validates solutions
4. **🔄 Feedback Coordinator**: Analyzes test failures and provides specific feedback for regeneration
5. **⚡ Code Optimizer**: Optimizes the final validated solution for performance

## 🔄 **Automatic Feedback Loop Process**

When test cases fail, the system automatically:

1. **Analyzes failures** with detailed error categorization
2. **Generates specific feedback** for the Code Generator
3. **Triggers code regeneration** with targeted improvements
4. **Re-tests the solution** until all tests pass
5. **Repeats up to 3 iterations** for continuous improvement

## 🚀 Enhanced Features with Feedback Loop

- **🔄 Automatic Feedback Loop**: Failed tests trigger automatic code regeneration
- **5-Agent Collaboration**: Five specialized agents work together with feedback coordination
- **Iterative Improvement**: Up to 3 feedback iterations for perfect solutions
- **Comprehensive Testing**: Automated test case generation and validation
- **LeetCode Acceptance Guaranteed**: Solutions validated through iterative testing
- **Real-time Processing**: Watch agents collaborate and improve in real-time
- **Live Test Execution**: See your code tested and improved automatically
- **Failure Analysis**: Detailed categorization of test failures and specific feedback
- **Code Analysis**: Complete time/space complexity analysis
- **Interactive UI**: Beautiful Streamlit interface with feedback loop visualization
- **Example Problems**: Pre-loaded example problems for quick testing
- **Groq AI Integration**: Fast inference using Groq's infrastructure
- **Edge Case Handling**: Comprehensive edge case testing and automatic fixes

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com/keys))

## 🛠️ Installation

### Quick Setup (Recommended)

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd Leetcode-Opti
   ```

2. **Run the automated installer**:

   ```bash
   python install.py
   ```

3. **Edit the `.env` file** and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

### Manual Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Groq API key.

## 🎯 Usage

### Easy Start

**Option 1: Use the run script (Recommended)**

```bash
python run.py
```

**Option 2: Windows users can double-click**

```
run.bat
```

**Option 3: Manual start**

```bash
streamlit run main.py
```

### Using the Application

1. **Open your browser** and go to `http://localhost:8501`
2. **Enter a LeetCode problem** or select from example problems
3. **Click "Run Multi-Agent Optimizer"** and watch the agents work!

### Testing Your Setup

```bash
python test_setup.py
```

## 📝 Example Problems

The app includes pre-loaded examples:

- Two Sum
- Valid Parentheses
- (Add your own custom problems)

## 🔧 How It Works

1. **Problem Input**: User provides a LeetCode problem statement
2. **Code Generation**: First agent analyzes and generates a solution
3. **Code Review**: Second agent reviews for correctness and improvements
4. **Code Optimization**: Third agent optimizes for performance
5. **Results Display**: All conversations and final optimized code shown

## 🏗️ Project Structure

```
Leetcode-Opti/
├── main.py              # Streamlit UI with feedback loop integration
├── agents.py            # 5-agent system with feedback loop support
├── config.py            # Configuration settings with feedback parameters
├── utils.py             # Utility functions
├── test_executor.py     # Comprehensive test execution engine
├── feedback_loop.py     # Feedback loop orchestration system
├── install.py           # Automated installation script
├── run.py               # Easy run script
├── run.bat              # Windows batch file
├── test_setup.py        # Setup validation script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## ⚙️ Configuration

### Groq AI Settings

- Model: `llama3-70b-8192`
- Temperature: `0.7`
- Timeout: `120 seconds`

### Agent Settings

- Max consecutive replies: `1` per agent
- Group chat rounds: `6` maximum
- Speaker selection: `round_robin`

## 🐛 Troubleshooting

**Common Issues:**

1. **"GROQ_API_KEY not found"**

   - Make sure you created `.env` file with your API key

2. **Import errors**

   - Run `pip install -r requirements.txt`

3. **Slow responses**

   - Groq AI is usually fast, check your internet connection

4. **Agent not responding**
   - Try refreshing the page and running again

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Autogen**: Microsoft's multi-agent framework
- **Groq**: Fast AI inference platform
- **Streamlit**: Beautiful web app framework
- **LeetCode**: Problem inspiration

---

**Happy Coding! 🚀**
