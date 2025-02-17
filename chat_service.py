from model_adapter import ModelAdapter
from session_manager import SessionManager


class ChatService:
    def __init__(self, model_adapter: ModelAdapter, session_manager: SessionManager):
        self.model_adapter = model_adapter
        self.session_manager = session_manager

    def process_message(self, session_id: str, user_message: str) -> str:
        # Добавляем сообщение пользователя в историю сессии
        self.session_manager.add_message(session_id, user_message)
        context = self.session_manager.get_context(session_id)

        # Генерируем ответ с учетом контекста
        response = self.model_adapter.generate_response(user_message, context)

        # Сохраняем ответ в истории диалога
        self.session_manager.add_message(session_id, response)
        return response
