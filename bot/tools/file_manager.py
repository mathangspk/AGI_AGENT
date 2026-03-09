import aiofiles
from pathlib import Path
from typing import Optional, List

class FileManager:
    def __init__(self, base_path: str = "/app/projects"):
        self.base_path = Path(base_path)
    
    async def read_file(self, project_name: str, file_path: str) -> Optional[str]:
        try:
            full_path = self.base_path / project_name / file_path
            async with aiofiles.open(full_path, 'r') as f:
                return await f.read()
        except Exception as e:
            return None
    
    async def write_file(self, project_name: str, file_path: str, content: str) -> bool:
        try:
            full_path = self.base_path / project_name / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(full_path, 'w') as f:
                await f.write(content)
            return True
        except Exception as e:
            return False
    
    async def list_files(self, project_name: str, path: str = "") -> List[str]:
        try:
            full_path = self.base_path / project_name / path
            if not full_path.exists():
                return []
            return [p.name for p in full_path.iterdir()]
        except Exception:
            return []
    
    async def file_exists(self, project_name: str, file_path: str) -> bool:
        full_path = self.base_path / project_name / file_path
        return full_path.exists()
