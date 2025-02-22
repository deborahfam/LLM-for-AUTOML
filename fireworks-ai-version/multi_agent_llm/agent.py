import uuid
import datetime
from typing import List, Dict, Any
from .agent_message import AgentMessage

class Agent:
    def __init__(self, name: str, model_name: str, role: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.model_name = model_name
        self.role = role
        # Nuevo: estado para almacenar parámetros específicos (incluyendo RAG strategy)
        self.state: Dict[str, Any] = {}
        # Historial de mensajes enviados/recibidos
        self.history: List[AgentMessage] = []
        # Se espera que cada agente tenga, si es aplicable, un 'retriever' y un 'chunk_selector'
        self.retriever = None
        self.chunk_selector = None

    def send_message(self, content: str) -> AgentMessage:
        message = AgentMessage(self.id, self.role, content)
        self.history.append(message)
        return message

    def get_last_messages(self, k: int) -> List[Dict[str, str]]:
        return [{"sender_id": m.sender_id, "role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()}
                for m in self.history[-k:]]
    
    def process_message(self, message: AgentMessage):
        # Método genérico que se puede sobrescribir en agentes especializados
        print(f"{self.name} recibió: {message.content}")