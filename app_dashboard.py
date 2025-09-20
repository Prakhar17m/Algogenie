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
from file_browser import SolutionBrowser, render_file_browser
from solution_editor import SolutionEditor, render_solution_editor

# Configure Streamlit page
st.set_page_config(
    page_title="AlgoGenie - AI DSA Problem Solver",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with animations and modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* CSS Variables */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #8b5cf6;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --bg-primary: #f8fafc;
        --bg-secondary: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border: #e2e8f0;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Header Styles */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: slideDown 0.6s ease-out;
    }

    .main-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: fadeInUp 0.8s ease-out;
    }

    .main-subtitle {
        font-size: 1.4rem;
        color: var(--text-secondary);
        margin-bottom: 0;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }

    /* Card Styles */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }

    .solution-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }

    .solution-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        font-family: 'Inter', sans-serif;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, var(--primary-dark), var(--secondary));
    }

    .primary-button {
        background: linear-gradient(135deg, var(--success), var(--accent));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }

    .primary-button:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 10px;
    }

    /* Sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 0 20px 20px 0;
    }

    /* Code Blocks */
    .code-block {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 12px;
        font-family: 'Fira Code', 'Monaco', monospace;
        overflow-x: auto;
        border: 1px solid #334155;
        box-shadow: var(--shadow);
    }

    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }

    .pulse {
        animation: pulse 2s infinite;
    }

    /* Status Indicators */
    .status-success {
        color: var(--success);
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .status-error {
        color: var(--error);
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .status-warning {
        color: var(--warning);
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .main-header {
            padding: 2rem;
        }
        .feature-card {
            padding: 1.5rem;
        }
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'solutions' not in st.session_state:
    st.session_state.solutions = []
if 'current_solution' not in st.session_state:
    st.session_state.current_solution = None
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Solve"

def load_solutions():
    """Load all saved solutions"""
    browser = SolutionBrowser()
    return browser.get_solutions()

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
    solutions_dir = Path("solutions")
    solutions_dir.mkdir(exist_ok=True)
    
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
    <div class="main-header">
        <h1 class="main-title">🧠 AlgoGenie</h1>
        <p class="main-subtitle">AI-Powered Data Structures & Algorithms Problem Solver</p>
        <div style="margin-top: 1rem;">
            <span style="background: linear-gradient(135deg, #10b981, #06b6d4); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                ✨ Enhanced with OpenRouter AI
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Solve", "📁 Browse", "✏️ Edit", "📊 Analytics"])

    with tab1:
        render_solve_tab()

    with tab2:
        render_file_browser()

    with tab3:
        render_solution_editor()

    with tab4:
        render_analytics_tab()

def render_solve_tab():
    """Render the problem solving tab"""
    st.markdown("### 💭 Problem Input")
    
    # Problem input with enhanced UI
    col1, col2 = st.columns([3, 1])
    
    with col1:
        problem_input = st.text_area(
            "Describe your DSA problem:",
            value="Write a function to find the maximum element in an array",
            height=120,
            help="Be as specific as possible about your problem requirements",
            key="problem_input"
        )
    
    with col2:
        st.markdown("#### 🎯 Quick Templates")
        templates = [
            "Binary Search",
            "Merge Sort", 
            "Linked List",
            "Tree Traversal",
            "Dynamic Programming",
            "Graph Algorithms"
        ]
        
        for template in templates:
            if st.button(f"📝 {template}", key=f"template_{template}"):
                st.session_state.template_selected = template
                st.rerun()
    
    # Advanced options
    with st.expander("🔧 Advanced Options", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            include_tests = st.checkbox("Include Test Cases", value=True)
            include_docs = st.checkbox("Include Documentation", value=True)
        with col2:
            complexity_analysis = st.checkbox("Complexity Analysis", value=True)
            optimization_tips = st.checkbox("Optimization Tips", value=True)
    
    # Solve button
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
            st.markdown('<div class="status-warning">🔄 Initializing AI agents and Docker container...</div>', unsafe_allow_html=True)
        progress_bar.progress(10)
        
        team, docker = get_dsa_team_and_docker()
        progress_bar.progress(20)
        
        # Step 2: Start Docker
        with status_container:
            st.markdown('<div class="status-warning">🐳 Starting Docker container for code execution...</div>', unsafe_allow_html=True)
        progress_bar.progress(30)
        
        # Step 3: Solve problem
        with status_container:
            st.markdown('<div class="status-warning">🧠 AI agents are analyzing and solving your problem...</div>', unsafe_allow_html=True)
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
                            # Display agent message with enhanced styling
                            agent_name = message.source
                            content = message.content
                            
                            if "DSA_Problem_Solver_Agent" in agent_name:
                                with st.chat_message("assistant", avatar="🧑‍💻"):
                                    st.markdown("""
                                    <div class="solution-card">
                                        <h4>🧑‍💻 Problem Solver Agent</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
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
                                    st.markdown("""
                                    <div class="solution-card">
                                        <h4>🤖 Code Executor Agent</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
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
                                st.markdown("""
                                <div class="status-success">
                                    ✅ Task Completed: """ + message.stop_reason + """
                                </div>
                                """, unsafe_allow_html=True)
                                solution_data['messages'].append({
                                    'agent': 'System',
                                    'content': f"Task completed: {message.stop_reason}",
                                    'timestamp': datetime.now().isoformat()
                                })
                    
                    return solution_data
                    
                except Exception as e:
                    st.markdown(f"""
                    <div class="status-error">
                        ❌ Error during solving: {e}
                    </div>
                    """, unsafe_allow_html=True)
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
                
                # Success message with animation
                st.markdown("""
                <div class="status-success pulse">
                    🎉 Problem solved successfully!
                </div>
                """, unsafe_allow_html=True)
                
                # Display solution summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Problem", problem[:30] + "...")
                with col2:
                    st.metric("Code Lines", len(solution_data['code'].split('\n')))
                with col3:
                    st.metric("Status", "✅ Complete")
                
                # File location info
                st.info(f"📁 Solution saved to: {Path('solutions').absolute()}")
                
                # Auto-refresh to show the solution
                time.sleep(1)
                st.rerun()
            
            else:
                st.markdown("""
                <div class="status-error">
                    ❌ Failed to solve the problem. Please try again.
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.markdown(f"""
        <div class="status-error">
            ❌ Error: {e}
        </div>
        """, unsafe_allow_html=True)
        st.error("Please check your configuration and try again.")

def render_analytics_tab():
    """Render the analytics tab"""
    st.markdown("### 📊 Solution Analytics")
    
    solutions = load_solutions()
    
    if not solutions:
        st.info("No solutions found. Solve some problems first!")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Solutions", len(solutions))
    
    with col2:
        recent_count = len([s for s in solutions if 
                          (datetime.now() - datetime.fromisoformat(s['timestamp'])).days <= 7])
        st.metric("This Week", recent_count)
    
    with col3:
        avg_code_length = sum(len(s['code'].split('\n')) for s in solutions) / len(solutions)
        st.metric("Avg Code Lines", f"{avg_code_length:.1f}")
    
    with col4:
        unique_problems = len(set(s['problem'] for s in solutions))
        st.metric("Unique Problems", unique_problems)
    
    # Problem categories
    st.markdown("#### 🏷️ Problem Categories")
    categories = {}
    for solution in solutions:
        problem = solution['problem'].lower()
        if 'sort' in problem or 'merge' in problem or 'quick' in problem:
            categories['Sorting'] = categories.get('Sorting', 0) + 1
        elif 'search' in problem or 'binary' in problem:
            categories['Searching'] = categories.get('Searching', 0) + 1
        elif 'tree' in problem or 'binary tree' in problem:
            categories['Trees'] = categories.get('Trees', 0) + 1
        elif 'graph' in problem or 'bfs' in problem or 'dfs' in problem:
            categories['Graphs'] = categories.get('Graphs', 0) + 1
        elif 'dynamic' in problem or 'dp' in problem:
            categories['Dynamic Programming'] = categories.get('Dynamic Programming', 0) + 1
        else:
            categories['Other'] = categories.get('Other', 0) + 1
    
    # Display categories as metrics
    if categories:
        cols = st.columns(len(categories))
        for i, (category, count) in enumerate(sorted(categories.items(), key=lambda x: x[1], reverse=True)):
            with cols[i]:
                st.metric(category, count)
    
    # Recent activity
    st.markdown("#### 📈 Recent Activity")
    recent_solutions = sorted(solutions, key=lambda x: x['timestamp'], reverse=True)[:5]
    
    for solution in recent_solutions:
        with st.expander(f"📄 {solution['problem'][:50]}...", expanded=False):
            st.write(f"**Created:** {solution['timestamp'][:19]}")
            st.write("**Code Lines:**", len(solution['code'].split("\n")))

            if solution.get('test_results'):
                st.write(f"**Test Cases:** {len(solution['test_results'])}")

if __name__ == "__main__":
    main()
