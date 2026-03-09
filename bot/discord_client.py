import os
import asyncio
import discord
from discord.ext import commands

class DiscordClient:
    def __init__(self, llm_router, project_manager):
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.llm_router = llm_router
        self.project_manager = project_manager
        
        @self.bot.event
        async def on_ready():
            print(f"DevMate is online! Logged in as {self.bot.user}")
            print(f"Workspace loaded: {self.llm_router.workspace_loaded}")
            print(f"Provider: {self.llm_router.current_provider}")
            print(f"Skills: {self.llm_router.list_skills()}")
            
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            
            if self.bot.user in message.mentions:
                await self.handle_mention(message)
            else:
                await self.bot.process_commands(message)
    
    async def handle_mention(self, message):
        user_id = message.author.id
        content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
        content = content.replace(f"<@!{self.bot.user.id}>", "").strip()
        
        if not content:
            skills = self.llm_router.list_skills()
            await message.reply(f"Hey! I am DevMate.\nProvider: {self.llm_router.current_provider}\nSkills: {', '.join(skills) if skills else 'None'}\n\nHow can I help you?")
            return
        
        if content.lower().startswith("tao skill") or content.lower().startswith("create skill"):
            await self.handle_create_skill(message, content)
            return
        
        if content.lower().startswith("list skills") or content.lower().startswith("liet ke skills"):
            skills = self.llm_router.list_skills()
            await message.reply(f"Available skills:\n" + "\n".join([f"- {s}" for s in skills]) if skills else "No skills yet.")
            return
        
        if content.lower().startswith("ban la ai") or content.lower().startswith("who are you"):
            identity = self.llm_router.workspace_context.get("identity.md", "I am DevMate, an AI coding assistant.")
            await message.reply(identity[:1500])
            return
        
        async with message.channel.typing():
            try:
                project_name = self.project_manager.get_current_project(user_id)
                
                response = await self.llm_router.chat(
                    message=content,
                    user_id=user_id,
                    project_manager=self.project_manager,
                    project_name=project_name
                )
                
                await message.reply(response[:2000])
                
            except Exception as e:
                await message.reply(f"Error: {str(e)}")
    
    async def handle_create_skill(self, message, content):
        parts = content.split()
        if len(parts) < 2:
            await message.reply("Usage: @DevMate create skill <name>\nThen describe what the skill does.")
            return
        
        skill_name = parts[1].lower()
        skill_path = os.path.join("/app/workspace/devmate/skills", f"{skill_name}.md")
        
        if os.path.exists(skill_path):
            await message.reply(f"Skill '{skill_name}' already exists!")
            return
        
        try:
            os.makedirs(os.path.dirname(skill_path), exist_ok=True)
            with open(skill_path, 'w') as f:
                f.write(f"# Skill: {skill_name}\n\n## Description\nAdd description here.\n\n## Usage\nHow to use this skill.\n")
            
            await message.reply(f"Created skill '{skill_name}'!\nEdit it at: /app/workspace/devmate/skills/{skill_name}.md")
        except Exception as e:
            await message.reply(f"Error creating skill: {e}")
    
    async def run(self):
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            raise ValueError("DISCORD_BOT_TOKEN not set!")
        await self.bot.start(token)
