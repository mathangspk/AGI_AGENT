import os
from typing import Optional
from bot.tools.command_exec import CommandExecutor
from bot.tools.file_manager import FileManager

class LLMRouter:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.nvidia_api_key = os.getenv("MOONSHOT_API_KEY")
        self.message_history = {}
        self.command_exec = CommandExecutor()
        self.file_manager = FileManager()
        
        if self.nvidia_api_key:
            self.current_provider = "NVIDIA (DeepSeek V3.1)"
        elif self.groq_api_key:
            self.current_provider = "Groq (Llama 3.3 70B)"
        else:
            self.current_provider = "None"
    
    async def chat(self, message: str, user_id: int, project_manager, project_name: Optional[str] = None) -> str:
        if user_id not in self.message_history:
            self.message_history[user_id] = []
        
        messages = self.message_history[user_id]
        
        system_prompt = self._build_system_prompt(project_manager, project_name)
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            if self.nvidia_api_key:
                response = await self._call_nvidia(messages)
            elif self.groq_api_key:
                response = await self._call_groq(messages)
            else:
                return "No LLM provider configured. Set GROQ_API_KEY or MOONSHOT_API_KEY"
        except Exception as e:
            response = f"Error: {str(e)}"
        
        messages.append({"role": "assistant", "content": response})
        if len(messages) > 20:
            self.message_history[user_id] = messages[-20:]
        
        return response
    
    def _build_system_prompt(self, project_manager, project_name: Optional[str] = None) -> str:
        prompt = f"""You are DevMate, an AI coding assistant.

AVAILABLE PROVIDER:
- Current LLM: {self.current_provider}
- NVIDIA DeepSeek V3.1: High performance model
- Groq: Fast inference with Llama 3.3 70B, Mixtral models

YOUR CAPABILITIES:
- Read/write files in the project directory
- Run commands (tests, builds, git operations)
- List directory contents
- Search for code patterns

Be concise and practical."""
        
        if project_name:
            project_path = project_manager.get_project_path(project_name)
            prompt += f"\n\nCurrent project: {project_name}\nProject path: {project_path}"
        
        return prompt
    
    async def _call_nvidia(self, messages: list) -> str:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=self.nvidia_api_key,
            base_url="https://integrate.api.nvidia.com/v1"
        )
        
        response = client.chat.completions.create(
            model="deepseek-ai/deepseek-v3.1",
            messages=messages,
            temperature=0.7,
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    async def _call_groq(self, messages: list) -> str:
        from groq import Groq
        
        client = Groq(api_key=self.groq_api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=4096
        )
        
        return response.choices[0].message.content
