from typing import List, Dict


class SessionManager:
    def __init__(self):
        # Используем словарь для хранения истории диалогов: {session_id: [сообщения]}
        self.sessions: Dict[str, List[str]] = {}

    def create_session(self, session_id: str):
        self.sessions[session_id] = []

    def add_message(self, session_id: str, message: str):
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id].append(message)

    def get_context(self, session_id: str) -> List[str]:
        return self.sessions.get(session_id, [])
