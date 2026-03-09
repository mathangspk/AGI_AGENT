import asyncio

class CommandExecutor:
    def __init__(self, allowed_commands: list = None, max_timeout: int = 60):
        self.allowed_commands = allowed_commands or []
        self.max_timeout = max_timeout
    
    async def run(self, command: str, cwd: str = None) -> tuple:
        if not self._is_command_allowed(command):
            return ("", f"Command not allowed: {command}", 1)
        
        try:
            result = await asyncio.wait_for(
                asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd
                ),
                timeout=self.max_timeout
            )
            
            stdout, stderr = await result.communicate()
            
            return (
                stdout.decode() if stdout else "",
                stderr.decode() if stderr else "",
                result.returncode
            )
            
        except asyncio.TimeoutError:
            return ("", "Command timed out", 1)
        except Exception as e:
            return ("", str(e), 1)
    
    def _is_command_allowed(self, command: str) -> bool:
        if not self.allowed_commands:
            return True
        
        for allowed in self.allowed_commands:
            if command.strip().startswith(allowed.split()[0]):
                return True
        
        return False
