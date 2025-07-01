"""
Reminders service for Prism AI Voice Assistant
Provides reminder management capabilities
"""

import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

@dataclass
class Reminder:
    """Reminder data structure"""
    id: str
    title: str
    datetime: datetime
    completed: bool = False

class ReminderService:
    """Service for reminder management"""
    
    def __init__(self):
        self.reminders: List[Reminder] = []
    
    def add_reminder(self, title: str, time_str: str) -> Reminder:
        """Add a new reminder"""
        reminder_time = self._parse_time_string(time_str)
        reminder = Reminder(
            id=str(uuid.uuid4()),
            title=title,
            datetime=reminder_time
        )
        self.reminders.append(reminder)
        return reminder
    
    def get_reminders(self, include_completed: bool = False) -> List[Reminder]:
        """Get all reminders"""
        if include_completed:
            return self.reminders
        return [r for r in self.reminders if not r.completed]
    
    def complete_reminder(self, reminder_id: str) -> bool:
        """Mark a reminder as completed"""
        for reminder in self.reminders:
            if reminder.id == reminder_id:
                reminder.completed = True
                return True
        return False
    
    def delete_reminder(self, reminder_id: str) -> bool:
        """Delete a reminder"""
        for i, reminder in enumerate(self.reminders):
            if reminder.id == reminder_id:
                del self.reminders[i]
                return True
        return False
    
    def _parse_time_string(self, time_str: str) -> datetime:
        """Parse natural language time strings into datetime objects"""
        now = datetime.now()
        time_str = time_str.lower().strip()
        
        # Handle "tomorrow"
        if "tomorrow" in time_str:
            target_date = now + timedelta(days=1)
            time_str = time_str.replace("tomorrow", "").strip()
        else:
            target_date = now
        
        # Handle specific times
        time_patterns = [
            (r"(\d{1,2}):(\d{2})\s*(am|pm)?", r"\1:\2"),
            (r"(\d{1,2})\s*(am|pm)", r"\1:00"),
            (r"noon", "12:00"),
            (r"midnight", "00:00"),
        ]
        
        time_part = "12:00"  # Default to noon
        for pattern, replacement in time_patterns:
            match = re.search(pattern, time_str)
            if match:
                time_part = match.expand(replacement)
                break
        
        # Parse time
        try:
            if "pm" in time_str and not time_part.endswith("pm"):
                hour, minute = map(int, time_part.split(":"))
                if hour != 12:
                    hour += 12
                time_part = f"{hour:02d}:{minute:02d}"
            elif "am" in time_str and time_part.endswith("12"):
                time_part = time_part.replace("12", "00")
            
            hour, minute = map(int, time_part.split(":"))
            return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        except:
            return now + timedelta(hours=1)  # Default to 1 hour from now

# Global instance
reminder_service = ReminderService() 