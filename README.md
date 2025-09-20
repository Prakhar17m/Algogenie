# AlgoGenie - DSA Problem Solver

A powerful AI-powered Data Structures and Algorithms problem solver built with AutoGen agents. This application uses multiple AI agents working together to solve DSA problems, write code, execute it in a Docker container, and provide comprehensive explanations.

## Features

- 🤖 **AI-Powered Problem Solving**: Uses GPT-4 to understand and solve DSA problems
- 🐳 **Docker Code Execution**: Safely executes code in isolated Docker containers
- 👥 **Multi-Agent System**: Problem solver and code executor agents work together
- 🌐 **Web Interface**: Beautiful Streamlit-based web interface
- 💻 **CLI Interface**: Command-line interface for quick problem solving
- 📝 **Code Saving**: Automatically saves solutions to files
- 🧪 **Test Cases**: Generates and runs multiple test cases

## Prerequisites

- Python 3.8 or higher
- Docker Desktop (for code execution)
- OpenRouter API key (or OpenAI API key)

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Algogenie
```

### 2. Run Setup Script

```bash
python setup.py
```

This will:
- Install all required dependencies
- Check Docker installation
- Verify configuration

### 3. Configure Environment

Edit the `.env` file and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_actual_openrouter_api_key_here
```

**Get your OpenRouter API key from:** https://openrouter.ai/keys

**Available Models:**
- `meta-llama/llama-3.1-8b-instruct:free` (Free)
- `microsoft/phi-3-medium-128k-instruct:free` (Free)
- `google/gemini-flash-1.5` (Paid)
- `anthropic/claude-3.5-sonnet` (Paid)

### 4. Run the Application

**Easy Launcher (Recommended):**
```bash
python launch.py
```

**Direct Launch Options:**
```bash
# Enhanced Dashboard (Best Experience)
python -m streamlit run app_dashboard.py

# Enhanced Web Interface
python -m streamlit run app_enhanced.py

# Original Web Interface
python -m streamlit run app.py

# CLI Interface
python main.py

# Demo Mode (No API required)
python demo_mode.py
```

## Project Structure

```
Algogenie/
├── 📁 agents/                    # AI Agent implementations
│   ├── code_executor_agent.py   # Code execution agent
│   └── problem_solver.py        # Problem solving agent
├── 📁 config/                    # Configuration files
│   ├── constant.py              # Constants and settings
│   ├── docker_executor.py       # Docker configuration
│   ├── docker_utils.py          # Docker utilities
│   └── settings.py              # Model and API settings
├── 📁 team/                      # Team orchestration
│   └── dsa_team.py              # Team setup and coordination
├── 📁 solutions/                 # Generated solutions (auto-created)
├── 📁 temp/                      # Temporary files (auto-created)
├── 🚀 Core Applications
│   ├── app_dashboard.py         # Enhanced dashboard (RECOMMENDED)
│   ├── app_enhanced.py          # Enhanced web interface
│   ├── app.py                   # Original web interface
│   └── main.py                  # CLI interface
├── 🎮 Demo & Testing
│   ├── demo_mode.py             # Demo mode (no API required)
│   ├── test_openrouter.py       # OpenRouter API testing
│   └── test_setup.py            # Setup validation
├── 🛠️ Utilities
│   ├── file_browser.py          # File management component
│   ├── solution_editor.py       # Solution editing component
│   └── launch.py                # Application launcher
├── 📚 Documentation
│   ├── README.md                # Main documentation
│   ├── QUICKSTART.md            # Quick start guide
│   ├── OPENROUTER_SETUP.md      # OpenRouter setup guide
│   └── ENHANCED_FEATURES.md     # Enhanced features guide
└── ⚙️ Configuration
    ├── requirements.txt         # Python dependencies
    ├── setup.py                 # Setup script
    └── .gitignore               # Git ignore rules
```

## How It Works

1. **Problem Input**: User provides a DSA problem or question
2. **Problem Analysis**: The Problem Solver Agent analyzes the problem and creates a solution plan
3. **Code Generation**: The agent generates Python code with test cases
4. **Code Execution**: The Code Executor Agent runs the code in a Docker container
5. **Result Analysis**: Results are analyzed and explained
6. **Code Saving**: The solution is saved to a file
7. **Completion**: The process completes with a "STOP" signal

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
DOCKER_IMAGE=python:3.11
DOCKER_TIMEOUT=120
```

### Model Configuration

You can modify the model in `config/constant.py`:

```python
MODEL = 'gpt-4o'  # or 'gpt-3.5-turbo' for faster/cheaper responses
```

## Usage Examples

### Web Interface

1. Start the web app: `streamlit run app.py`
2. Open your browser to `http://localhost:8501`
3. Enter your DSA problem in the text input
4. Click "Run" to start solving
5. Watch the agents work together in real-time

### CLI Interface

1. Run: `python main.py`
2. The app will solve a default problem: "Write a Python code to add two numbers"
3. Modify the task in `main.py` to solve different problems

## Troubleshooting

### Docker Issues

- **Docker not running**: Start Docker Desktop
- **Permission denied**: Make sure Docker is running and you have proper permissions
- **Container fails**: Check Docker logs and ensure the image is available

### API Issues

- **OpenAI API errors**: Verify your API key is correct and has sufficient credits
- **Rate limiting**: The app includes retry logic, but you may need to wait

### Import Errors

- **Missing packages**: Run `pip install -r requirements.txt`
- **Version conflicts**: Use a virtual environment: `python -m venv venv && source venv/bin/activate`

## Development

### Adding New Agents

1. Create a new agent file in `agents/`
2. Import and add to the team in `team/dsa_team.py`
3. Update the termination conditions if needed

### Customizing Behavior

- **System messages**: Edit agent system messages in `agents/`
- **Team configuration**: Modify `team/dsa_team.py`
- **Docker settings**: Update `config/docker_executor.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in the console
3. Open an issue on GitHub

---

**Happy Coding! 🚀**
