import asyncio
import sys
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult


async def main():
    try:
        print("🚀 Starting AlgoGenie - DSA Problem Solver")
        print("=" * 50)
        
        dsa_team, docker = get_dsa_team_and_docker()
        print("✅ Team and Docker executor initialized")

        await start_docker_container(docker)
        print("✅ Docker container started successfully")
        
        task = 'Write a Python code to add two numbers.'
        print(f"📝 Task: {task}")
        print("=" * 50)

        async for message in dsa_team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print('==' * 20)
                print(f"{message.source}: {message.content}")
            elif isinstance(message, TaskResult):
                print('Stop Reason:', message.stop_reason)
                
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        try:
            await stop_docker_container(docker)
            print("✅ Docker container stopped")
        except Exception as e:
            print(f"⚠️  Warning: Error stopping Docker container: {e}")

if __name__ == "__main__":
    asyncio.run(main())