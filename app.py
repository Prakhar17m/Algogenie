import streamlit as st
import asyncio
import sys
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

# Configure Streamlit page
st.set_page_config(
    page_title="AlgoGenie - DSA Problem Solver",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AlgoGenie - DSA Problem Solver")
st.write("Welcome to AlgoGenie, your personal DSA problem solver! Here you can ask solutions to various data structures and algorithms problems.")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Make sure you have set your OpenAI API key in the .env file")
    
    # Display current model
    from config.constant import MODEL
    st.text(f"Model: {MODEL}")

# Main input area
task = st.text_input(
    "Enter your DSA problem or question:", 
    value='Write a function to add two numbers',
    help="Describe the DSA problem you want to solve"
)

async def run(team, docker, task):
    """Run the DSA solving process"""
    try:
        await start_docker_container(docker)
        st.success("🐳 Docker container started successfully")
        
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                msg = f"{message.source}: {message.content}"
                yield msg
            elif isinstance(message, TaskResult):
                msg = f"Stop Reason: {message.stop_reason}"
                yield msg
                
    except Exception as e:
        st.error(f"❌ Error: {e}")
        yield f"Error: {e}"
    finally:
        try:
            await stop_docker_container(docker)
            st.info("🐳 Docker container stopped")
        except Exception as e:
            st.warning(f"⚠️ Warning: Error stopping Docker container: {e}")

if st.button("🚀 Run Solution", type="primary"):
    if not task.strip():
        st.error("Please enter a problem to solve!")
        st.stop()
    
    # Initialize progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔄 Initializing team and Docker executor...")
        progress_bar.progress(10)
        
        team, docker = get_dsa_team_and_docker()
        progress_bar.progress(20)
        
        status_text.text("🚀 Starting problem solving process...")
        progress_bar.progress(30)
        
        # Create a container for messages
        messages_container = st.container()
        
        async def collect_messages():
            message_count = 0
            async for msg in run(team, docker, task):
                message_count += 1
                progress = min(30 + (message_count * 5), 90)
                progress_bar.progress(progress)
                
                if isinstance(msg, str):
                    if msg.startswith("user"):
                        with messages_container.chat_message('user', avatar='👤'):
                            st.markdown(msg)
                    elif msg.startswith('DSA_Problem_Solver_Agent'):
                        with messages_container.chat_message('assistant', avatar='🧑‍💻'):
                            st.markdown(msg)
                    elif msg.startswith('CodeExecutorAgent'):
                        with messages_container.chat_message('assistant', avatar='🤖'):
                            st.markdown(msg)
                    elif msg.startswith("Stop Reason"):
                        with messages_container.chat_message('system', avatar='✅'):
                            st.markdown(f"**{msg}**")
                elif isinstance(msg, TaskResult):
                    with messages_container.chat_message('system', avatar='🚫'):
                        st.markdown(f"**Task Completed: {msg.result}**")
        
        # Run the async function
        asyncio.run(collect_messages())
        
        progress_bar.progress(100)
        status_text.text("✅ Task completed successfully!")
        
    except Exception as e:
        st.error(f"❌ Failed to initialize: {e}")
        st.error("Please check your configuration and try again.")
            
