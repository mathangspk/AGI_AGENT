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
        self.conversations = {}
        
        @self.bot.event
        async def on_ready():
            print(f"DevMate is online! Logged in as {self.bot.user}")
            
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
            await message.reply("Hey! I'm DevMate, your AI coding assistant.")
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
    
    async def run(self):
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            raise ValueError("DISCORD_BOT_TOKEN not set!")
        await self.bot.start(token)
