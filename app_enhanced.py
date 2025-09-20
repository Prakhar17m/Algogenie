import streamlit as st
import asyncio
import sys
import os
import time
from datetime import datetime
from pathlib import Path
import json
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

# Configure Streamlit page
st.set_page_config(
    page_title="AlgoGenie - AI DSA Problem Solver",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --bg-color: #f8fafc;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
    }

    /* Global styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Header styling */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .main-subtitle {
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin-bottom: 0;
    }

    /* Card styling */
    .solution-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .agent-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid var(--primary-color);
    }

    .code-card {
        background: #1e293b;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
    }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }

    /* File browser styling */
    .file-item {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .file-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
    }

    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .slide-in {
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }

    /* Status indicators */
    .status-success {
        color: var(--success-color);
        font-weight: 600;
    }

    .status-error {
        color: var(--error-color);
        font-weight: 600;
    }

    .status-warning {
        color: var(--warning-color);
        font-weight: 600;
    }

    /* Code syntax highlighting */
    .code-block {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Fira Code', monospace;
        overflow-x: auto;
        border: 1px solid #334155;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .solution-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'solutions' not in st.session_state:
    st.session_state.solutions = []
if 'current_solution' not in st.session_state:
    st.session_state.current_solution = None

# Create solutions directory
solutions_dir = Path("solutions")
solutions_dir.mkdir(exist_ok=True)

def load_solutions():
    """Load all saved solutions"""
    solutions = []
    for solution_file in solutions_dir.glob("*.json"):
        try:
            with open(solution_file, 'r', encoding='utf-8') as f:
                solution_data = json.load(f)
                solutions.append(solution_data)
        except Exception as e:
            st.error(f"Error loading solution {solution_file}: {e}")
    return sorted(solutions, key=lambda x: x['timestamp'], reverse=True)

def save_solution(problem, code, explanation, test_results=None):
    """Save solution to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    solution_data = {
        'id': f"solution_{timestamp}",
        'timestamp': datetime.now().isoformat(),
        'problem': problem,
        'code': code,
        'explanation': explanation,
        'test_results': test_results or []
    }
    
    # Save as JSON
    json_file = solutions_dir / f"solution_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(solution_data, f, indent=2, ensure_ascii=False)
    
    # Save as Python file
    py_file = solutions_dir / f"solution_{timestamp}.py"
    with open(py_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    return solution_data

def main():
    # Header
    st.markdown("""
    <div class="main-header fade-in">
        <h1 class="main-title">🧠 AlgoGenie</h1>
        <p class="main-subtitle">AI-Powered Data Structures & Algorithms Problem Solver</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Model selection
        st.markdown("### 🤖 AI Model")
        model_options = {
            "Llama 3.1 8B (Free)": "meta-llama/llama-3.1-8b-instruct",
            "Phi-3 Medium (Free)": "microsoft/phi-3-medium-128k-instruct",
            "Gemini Flash 1.5": "google/gemini-flash-1.5",
            "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet"
        }
        
        selected_model = st.selectbox(
            "Choose AI Model:",
            options=list(model_options.keys()),
            index=0
        )
        
        # Update model in config
        from config.constant import MODEL
        st.info(f"Current: {MODEL}")
        
        st.markdown("---")
        
        # Solution browser
        st.markdown("### 📁 Saved Solutions")
        solutions = load_solutions()
        
        if solutions:
            for solution in solutions[:5]:  # Show last 5
                with st.expander(f"📄 {solution['problem'][:50]}..."):
                    st.write(f"**Created:** {solution['timestamp'][:19]}")
                    st.write(f"**Problem:** {solution['problem']}")
                    if st.button(f"View Solution", key=f"view_{solution['id']}"):
                        st.session_state.current_solution = solution
        else:
            st.info("No solutions saved yet")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        if st.button("📁 Open Solutions Folder"):
            os.startfile(str(solutions_dir.absolute()))
        
        if st.button("🧹 Clear All Solutions"):
            if st.session_state.get('confirm_clear', False):
                for file in solutions_dir.glob("*"):
                    file.unlink()
                st.success("All solutions cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm")

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Problem input
        st.markdown("### 💭 Problem Input")
        problem_input = st.text_area(
            "Describe your DSA problem:",
            value="Write a function to find the maximum element in an array",
            height=100,
            help="Be as specific as possible about your problem requirements"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            col_a, col_b = st.columns(2)
            with col_a:
                include_tests = st.checkbox("Include Test Cases", value=True)
                include_docs = st.checkbox("Include Documentation", value=True)
            with col_b:
                complexity_analysis = st.checkbox("Complexity Analysis", value=True)
                optimization_tips = st.checkbox("Optimization Tips", value=True)

    with col2:
        # Quick problem templates
        st.markdown("### 🎯 Quick Templates")
        templates = [
            "Binary Search Algorithm",
            "Merge Sort Implementation", 
            "Linked List Operations",
            "Tree Traversal Methods",
            "Dynamic Programming Problem",
            "Graph Algorithms",
            "Hash Table Operations",
            "Stack and Queue Problems"
        ]
        
        for template in templates:
            if st.button(f"📝 {template}", key=f"template_{template}"):
                st.session_state.template_selected = template
                st.rerun()
        
        if hasattr(st.session_state, 'template_selected'):
            problem_input = st.session_state.template_selected
            delattr(st.session_state, 'template_selected')

    # Solution display area
    if st.session_state.current_solution:
        st.markdown("---")
        st.markdown("### 📋 Current Solution")
        solution = st.session_state.current_solution
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Problem", solution['problem'][:30] + "...")
        with col2:
            st.metric("Created", solution['timestamp'][:10])
        with col3:
            st.metric("Status", "✅ Complete")
        
        # Display solution details
        with st.expander("📖 View Full Solution", expanded=True):
            st.markdown("**Problem:**")
            st.write(solution['problem'])
            
            st.markdown("**Code:**")
            st.code(solution['code'], language='python')
            
            st.markdown("**Explanation:**")
            st.write(solution['explanation'])

    # Main solve button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Solve Problem", type="primary", use_container_width=True):
            if not problem_input.strip():
                st.error("Please enter a problem to solve!")
            else:
                solve_problem(problem_input, include_tests, include_docs, complexity_analysis, optimization_tips)

def solve_problem(problem, include_tests=True, include_docs=True, complexity_analysis=True, optimization_tips=True):
    """Solve the DSA problem using AI agents"""
    
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_container = st.container()
    messages_container = st.container()
    
    try:
        # Step 1: Initialize
        with status_container:
            st.info("🔄 Initializing AI agents and Docker container...")
        progress_bar.progress(10)
        
        team, docker = get_dsa_team_and_docker()
        progress_bar.progress(20)
        
        # Step 2: Start Docker
        with status_container:
            st.info("🐳 Starting Docker container for code execution...")
        progress_bar.progress(30)
        
        # Step 3: Solve problem
        with status_container:
            st.info("🧠 AI agents are analyzing and solving your problem...")
        progress_bar.progress(40)
        
        # Create message containers
        with messages_container:
            st.markdown("### 🤖 AI Agent Conversation")
            
            # Run the solving process
            async def run_solving_process():
                try:
                    await start_docker_container(docker)
                    
                    solution_data = {
                        'problem': problem,
                        'code': '',
                        'explanation': '',
                        'test_results': [],
                        'messages': []
                    }
                    
                    message_count = 0
                    async for message in team.run_stream(task=problem):
                        message_count += 1
                        progress = min(40 + (message_count * 3), 90)
                        progress_bar.progress(progress)
                        
                        if isinstance(message, TextMessage):
                            # Display agent message
                            agent_name = message.source
                            content = message.content
                            
                            if "DSA_Problem_Solver_Agent" in agent_name:
                                with st.chat_message("assistant", avatar="🧑‍💻"):
                                    st.markdown(f"**Problem Solver Agent:**")
                                    st.markdown(content)
                                    
                                    # Extract code if present
                                    if "```python" in content:
                                        code_start = content.find("```python") + 9
                                        code_end = content.find("```", code_start)
                                        if code_end > code_start:
                                            solution_data['code'] = content[code_start:code_end].strip()
                                    
                                    solution_data['messages'].append({
                                        'agent': 'Problem Solver',
                                        'content': content,
                                        'timestamp': datetime.now().isoformat()
                                    })
                            
                            elif "CodeExecutorAgent" in agent_name:
                                with st.chat_message("assistant", avatar="🤖"):
                                    st.markdown(f"**Code Executor Agent:**")
                                    st.markdown(content)
                                    
                                    solution_data['messages'].append({
                                        'agent': 'Code Executor',
                                        'content': content,
                                        'timestamp': datetime.now().isoformat()
                                    })
                            
                            elif "user" in agent_name.lower():
                                with st.chat_message("user", avatar="👤"):
                                    st.markdown(content)
                        
                        elif isinstance(message, TaskResult):
                            with st.chat_message("system", avatar="✅"):
                                st.success(f"**Task Completed:** {message.stop_reason}")
                                solution_data['messages'].append({
                                    'agent': 'System',
                                    'content': f"Task completed: {message.stop_reason}",
                                    'timestamp': datetime.now().isoformat()
                                })
                    
                    return solution_data
                    
                except Exception as e:
                    st.error(f"Error during solving: {e}")
                    return None
                finally:
                    try:
                        await stop_docker_container(docker)
                    except:
                        pass
            
            # Run the async process
            solution_data = asyncio.run(run_solving_process())
            
            if solution_data and solution_data['code']:
                progress_bar.progress(95)
                
                # Save solution
                saved_solution = save_solution(
                    problem=solution_data['problem'],
                    code=solution_data['code'],
                    explanation=solution_data.get('explanation', ''),
                    test_results=solution_data.get('test_results', [])
                )
                
                st.session_state.solutions.append(saved_solution)
                st.session_state.current_solution = saved_solution
                
                progress_bar.progress(100)
                
                # Success message
                st.success("🎉 Problem solved successfully!")
                
                # Display solution summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Problem", problem[:30] + "...")
                with col2:
                    st.metric("Code Lines", len(solution_data['code'].split('\n')))
                with col3:
                    st.metric("Status", "✅ Complete")
                
                # File location info
                st.info(f"📁 Solution saved to: {solutions_dir.absolute()}")
                
                # Auto-refresh to show the solution
                time.sleep(1)
                st.rerun()
            
            else:
                st.error("❌ Failed to solve the problem. Please try again.")
    
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.error("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
