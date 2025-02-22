import datetime

class AgentMessage:
    def __init__(self, sender_id: str, role: str, content: str, timestamp=None):
        self.sender_id = sender_id
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.datetime.now()