import os
import json
from datetime import datetime
from typing import Optional
from bot.tools.command_exec import CommandExecutor
from bot.tools.file_manager import FileManager

WORKSPACE_PATH = "/app/workspace/devmate"

class LLMRouter:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.nvidia_api_key = os.getenv("MOONSHOT_API_KEY")
        self.message_history = {}
        self.command_exec = CommandExecutor()
        self.file_manager = FileManager()
        self.workspace_loaded = False
        
        if self.nvidia_api_key:
            self.current_provider = "NVIDIA (DeepSeek V3.1)"
        elif self.groq_api_key:
            self.current_provider = "Groq (Llama 3.3 70B)"
        else:
            self.current_provider = "None"
        
        self._load_workspace_context()
    
    def _load_workspace_context(self):
        context_files = ["identity.md", "goals.md", "USER.md", "MEMORY.md", "AGENTS.md"]
        context = {}
        
        for filename in context_files:
            filepath = os.path.join(WORKSPACE_PATH, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        context[filename] = f.read()
                except:
                    pass
        
        self.workspace_context = context
        self.workspace_loaded = True
    
    def _get_today_memory_path(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(WORKSPACE_PATH, "memory", f"{today}.md")
    
    def _ensure_today_memory(self):
        mem_path = self._get_today_memory_path()
        if not os.path.exists(mem_path):
            os.makedirs(os.path.dirname(mem_path), exist_ok=True)
            with open(mem_path, 'w') as f:
                f.write(f"# {datetime.now().strftime('%Y-%m-%d')} - Daily Log\n\n")
        return mem_path
    
    def append_to_memory(self, content: str):
        try:
            mem_path = self._ensure_today_memory()
            with open(mem_path, 'a') as f:
                f.write(content + "\n")
        except Exception as e:
            print(f"Error writing to memory: {e}")
    
    def list_skills(self):
        skills_dir = os.path.join(WORKSPACE_PATH, "skills")
        if not os.path.exists(skills_dir):
            return []
        return [f.replace(".md", "") for f in os.listdir(skills_dir) if f.endswith(".md")]
    
    def get_skill_content(self, skill_name: str):
        skill_path = os.path.join(WORKSPACE_PATH, "skills", f"{skill_name}.md")
        if os.path.exists(skill_path):
            with open(skill_path, 'r') as f:
                return f.read()
        return None
    
    async def chat(self, message: str, user_id: int, project_manager, project_name: Optional[str] = None) -> str:
        if user_id not in self.message_history:
            self.message_history[user_id] = []
        
        messages = self.message_history[user_id]
        
        system_prompt = self._build_system_prompt(project_manager, project_name)
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        self.append_to_memory(f"User: {message}")
        
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
        self.append_to_memory(f"Assistant: {response[:200]}...\n")
        
        if len(messages) > 20:
            self.message_history[user_id] = messages[-20:]
        
        return response
    
    def _build_system_prompt(self, project_manager, project_name: Optional[str] = None) -> str:
        prompt_parts = []
        
        if "identity.md" in self.workspace_context:
            prompt_parts.append(self.workspace_context["identity.md"])
        
        if "goals.md" in self.workspace_context:
            prompt_parts.append("\n" + self.workspace_context["goals.md"])
        
        if "AGENTS.md" in self.workspace_context:
            prompt_parts.append("\n" + self.workspace_context["AGENTS.md"])
        
        skills = self.list_skills()
        if skills:
            prompt_parts.append(f"\n## Available Skills\n{', '.join(skills)}")
        
        prompt_parts.append(f"\n## Current LLM: {self.current_provider}")
        
        if project_name:
            project_path = project_manager.get_project_path(project_name)
            prompt_parts.append(f"\n## Current Project\nName: {project_name}\nPath: {project_path}")
        
        prompt_parts.append("\n## Workspace Location\n- Workspace: /app/workspace/devmate/\n- Projects: /app/projects/")
        
        return "\n\n".join(prompt_parts)
    
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
