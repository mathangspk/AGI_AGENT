import os
import json
from pathlib import Path
from typing import Optional

class ProjectManager:
    def __init__(self, config: dict):
        self.config = config
        self.projects_dir = Path("/app/projects")
        self.current_projects = {}
        
        self._ensure_projects_dir()
    
    def _ensure_projects_dir(self):
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def list_projects(self) -> list:
        if not self.projects_dir.exists():
            return []
        return [p.name for p in self.projects_dir.iterdir() if p.is_dir()]
    
    def get_project_path(self, project_name: str) -> str:
        project_path = self.projects_dir / project_name
        return str(project_path)
    
    def get_current_project(self, user_id: int) -> Optional[str]:
        return self.current_projects.get(user_id) or os.getenv("DEFAULT_PROJECT", "default")
    
    def set_current_project(self, user_id: int, project_name: str):
        self.current_projects[user_id] = project_name
    
    def get_test_command(self, project_name: str) -> str:
        project_config = self.config.get("projects", {}).get(project_name, {})
        return project_config.get("test_command", "pytest")
    
    def get_build_command(self, project_name: str) -> str:
        project_config = self.config.get("projects", {}).get(project_name, {})
        return project_config.get("build_command", "npm run build")
