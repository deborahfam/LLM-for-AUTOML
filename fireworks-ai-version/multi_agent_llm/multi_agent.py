from typing import List, Dict, Any
from .agent import Agent
from .tasks import Task
from .rag_strategies import BaseRAGStrategy  # Se asume que existe un módulo con estrategias de RAG

class MultiAgentSystem:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.global_state: Dict[str, Any] = {}
        self.messages: List[Dict[str, Any]] = []  # Historial global de mensajes

    def add_agent(self, name: str, model_name: str, role: str, rag_strategy: BaseRAGStrategy = None):
        if name not in self.agents:
            # Se crea el agente con un rol y se almacena su estrategia RAG en su estado
            agent = Agent(name, model_name, role=role)
            agent.state['rag_strategy'] = rag_strategy
            self.agents[name] = agent

    def add_task(self, task_id: str, description: str, assigned_agent: str):
        if assigned_agent in self.agents:
            self.tasks[task_id] = Task(task_id, description, assigned_agent)
        else:
            raise ValueError(f"Agent {assigned_agent} not found.")

    def send_message_to_agent(self, agent_name: str, content: str) -> Any:
        if agent_name in self.agents:
            message = self.agents[agent_name].send_message(content)
            self.messages.append(message)
            return message
        else:
            raise ValueError(f"Agent {agent_name} not found.")

    def get_agent_messages(self, agent_name: str, k: int) -> List[Dict[str, str]]:
        if agent_name in self.agents:
            return self.agents[agent_name].get_last_messages(k)
        else:
            raise ValueError(f"Agent {agent_name} not found.")

    def broadcast_message(self, content: str) -> Dict[str, Any]:
        responses = {}
        for agent_name, agent in self.agents.items():
            message = agent.send_message(content)
            self.messages.append(message)
            responses[agent_name] = message
        return responses

    def execute_task(self, task_id: str):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            agent = self.agents[task.assigned_agent]
            response = agent.send_message(task.description)
            task.mark_completed(response)
            self.messages.append(response)
            return response
        else:
            raise ValueError(f"Task {task_id} not found.")

    def execute_rag_strategy(self, prompt: str, query_embedding: List[float], top_k: int = 3) -> str:
        if not self.agents:
            raise ValueError("No agents available in the system.")

        # Enviar el prompt a todos los agentes y recopilar respuestas iniciales
        responses = self.broadcast_message(prompt)
        processed_responses = {}

        for agent_name, agent in self.agents.items():
            rag_strategy: BaseRAGStrategy = agent.state.get('rag_strategy')
            if rag_strategy:
                # Se espera que cada estrategia disponga de un método generate_context que reciba:
                # (prompt, query_embedding, retriever, chunk_selector, top_k)
                # Aquí se asume que cada agente tiene los atributos retriever y chunk_selector configurados.
                processed_context = rag_strategy.generate_context(
                    prompt, query_embedding, agent.retriever, agent.chunk_selector, top_k
                )
                processed_responses[agent_name] = processed_context
            else:
                # Si no se define una estrategia, se usa el contenido del mensaje original.
                processed_responses[agent_name] = responses[agent_name].content

        # La estrategia final de agregación: concatenar las respuestas de los agentes
        final_response = "\n\n---\n\n".join(
            [f"{name}: {content}" for name, content in processed_responses.items()]
        )
        return final_response
