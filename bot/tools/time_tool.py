from datetime import datetime
from typing import Dict, Any

class TimeTool:
    def get_current_time(self) -> str:
        """Get the current date and time"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_current_date(self) -> str:
        """Get the current date"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d")
    
    def get_current_timezone(self) -> str:
        """Get current timezone info"""
        import time
        now = datetime.now()
        tz_name = time.tzname[0]
        return f"Current timezone: {tz_name}"

time_tool = TimeTool()
