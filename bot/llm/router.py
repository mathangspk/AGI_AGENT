import os
import json
from typing import Optional, List, Dict, Any
from bot.tools.command_exec import CommandExecutor
from bot.tools.file_manager import FileManager
from bot.tools.web_tools import web_tools
from bot.tools.time_tool import time_tool

FUNCTION_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the internet for information. Use this when you need to find current information, news, or facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_content",
            "description": "Fetch and parse content from a URL. Returns up to 5000 characters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to fetch"},
                    "max_length": {"type": "integer", "description": "Max characters to return (default 5000)", "default": 5000}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell_command",
            "description": "Execute a shell command on the server. USE WITH CAUTION.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute"},
                    "timeout": {"type": "integer", "description": "Timeout in seconds (default 60)", "default": 60}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from the filesystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Full path to the file"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Creates new file or overwrites existing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Full path to the file"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to list"}
                },
                "required": ["path"]
            }
        }
    }
]

class LLMRouter:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.nvidia_api_key = os.getenv("MOONSHOT_API_KEY")
        self.message_history = {}
        self.command_exec = CommandExecutor()
        self.file_manager = FileManager()
        self.user_providers = {}  # Per-user provider override
        self.workspace_context = {}
        
        # Determine default provider
        if self.nvidia_api_key:
            self.default_provider = "nvidia"
            self.current_provider = "NVIDIA (DeepSeek V3.1)"
        elif self.groq_api_key:
            self.default_provider = "groq"
            self.current_provider = "Groq (Llama 3.3 70B)"
        else:
            self.default_provider = None
            self.current_provider = "None"
    
    def get_provider_for_user(self, user_id: int) -> str:
        """Get provider for specific user (allows per-user override)"""
        return self.user_providers.get(user_id, self.default_provider)
    
    def set_user_provider(self, user_id: int, provider: str):
        """Set provider for specific user"""
        if provider in ["groq", "nvidia"]:
            self.user_providers[user_id] = provider
            return True
        return False
    
    def list_providers(self) -> str:
        providers = []
        if self.groq_api_key:
            providers.append("groq - Groq (Llama 3.3 70B) - Fast responses")
        if self.nvidia_api_key:
            providers.append("nvidia - NVIDIA DeepSeek V3.1 - High accuracy")
        return "\n".join(providers) if providers else "No providers configured"
    
    async def chat(self, message: str, user_id: int, project_manager, project_name: Optional[str] = None) -> str:
        # Check for time-related queries FIRST (before calling LLM)
        time_result = self._detect_and_execute_time_query(message)
        if time_result:
            return time_result
        
        if user_id not in self.message_history:
            self.message_history[user_id] = []
        
        messages = self.message_history[user_id]
        
        system_prompt = self._build_system_prompt(project_manager, project_name)
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})
        
        try:
            # Get provider for this user
            provider = self.get_provider_for_user(user_id)
            if provider == "nvidia" and self.nvidia_api_key:
                response = await self._call_nvidia(messages)
            elif provider == "groq" and self.groq_api_key:
                response = await self._call_groq(messages)
            elif self.default_provider == "nvidia" and self.nvidia_api_key:
                response = await self._call_nvidia(messages)
            elif self.default_provider == "groq" and self.groq_api_key:
                response = await self._call_groq(messages)
            else:
                return "No LLM provider configured."
        except Exception as e:
            response = f"Error: {str(e)}"
        
        messages.append({"role": "assistant", "content": response})
        if len(messages) > 20:
            self.message_history[user_id] = messages[-20:]
        
        return response
    
    def _detect_and_execute_time_query(self, message: str) -> str:
        """Detect time-related queries and execute directly without LLM"""
        msg_lower = message.lower()
        
        time_keywords = [
            "mấy giờ", "giờ nào", "giờ rồi", "bao giờ", 
            "time is it", "what time", "current time", "now",
            "bây giờ", "hiện tại", "giờ hiện tại"
        ]
        
        if any(kw in msg_lower for kw in time_keywords):
            return f"Giờ hiện tại là: {time_tool.get_current_time()}"
        
        return ""
    
    def _build_system_prompt(self, project_manager, project_name: Optional[str] = None) -> str:
        prompt = f"""You are DevMate, an AI coding assistant.

AVAILABLE PROVIDER:
- Current LLM: {self.current_provider}
- NVIDIA DeepSeek V3.1: High performance model
- Groq: Fast inference with Llama 3.3 70B, Mixtral models

YOUR CAPABILITIES:
- Answer questions about time (just ask!)
- Read/write files in the project directory
- Run commands (tests, builds, git operations)
- Search for information
- List directory contents

Be concise and practical."""
        
        if project_name:
            project_path = project_manager.get_project_path(project_name)
            prompt += f"\n\nCurrent project: {project_name}\nProject path: {project_path}"
        
        return prompt
    
    async def _execute_function(self, func_name: str, args: Dict[str, Any]) -> str:
        try:
            if func_name == "search_web":
                return await web_tools.search_web(args.get("query", ""))
            elif func_name == "fetch_content":
                return await web_tools.fetch_content(args.get("url", ""), args.get("max_length", 5000))
            elif func_name == "get_current_time":
                return time_tool.get_current_time()
            elif func_name == "run_shell_command":
                import asyncio
                stdout, stderr, code = await self.command_exec.run(args.get("command", ""), cwd="")
                return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}\nExit code: {code}"
            elif func_name == "read_file":
                path = args.get("path", "")
                try:
                    with open(path, 'r') as f:
                        return f.read()
                except Exception as e:
                    return f"Error reading {path}: {str(e)}"
            elif func_name == "write_file":
                path = args.get("path", "")
                content = args.get("content", "")
                try:
                    with open(path, 'w') as f:
                        f.write(content)
                    return f"Written to {path}"
                except Exception as e:
                    return f"Error writing to {path}: {str(e)}"
            elif func_name == "list_directory":
                import os
                path = args.get("path", "")
                try:
                    files = os.listdir(path)
                    return "\n".join(files)
                except Exception as e:
                    return f"Error listing {path}: {str(e)}"
            else:
                return f"Unknown function: {func_name}"
        except Exception as e:
            return f"Error executing {func_name}: {str(e)}"
    
    async def _call_nvidia(self, messages: list):
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
        
        return response.choices[0].message
    
    async def _call_groq(self, messages: list):
        from groq import Groq
        
        client = Groq(api_key=self.groq_api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=4096
        )
        
        return response.choices[0].message
