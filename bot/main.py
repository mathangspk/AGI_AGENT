import os
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from bot.discord_client import DiscordClient
from bot.llm.router import LLMRouter
from bot.tools.project_manager import ProjectManager

async def main():
    config = load_config()
    
    project_manager = ProjectManager(config)
    llm_router = LLMRouter()
    
    discord_client = DiscordClient(
        llm_router=llm_router,
        project_manager=project_manager
    )
    
    await discord_client.run()

def load_config():
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}

if __name__ == "__main__":
    asyncio.run(main())
