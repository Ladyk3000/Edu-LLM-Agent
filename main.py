from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from chat_service import ChatService
from model_adapter import RemoteAPIAdapter, LocalModelAdapter, ModelAdapter
from session_manager import SessionManager
from config_manager import ConfigManager

app = FastAPI()

# Загружаем конфигурацию
config = ConfigManager("config.json")
adapter_type = config.get("adapter_type", "remote")

# Инициализируем нужный адаптер
if adapter_type == "remote":
    model_adapter: ModelAdapter = RemoteAPIAdapter(api_key=config.get("api_key"))
else:
    model_adapter: ModelAdapter = LocalModelAdapter(model_name=config.get("local_model_name"))

# Инициализируем менеджер сессий и чат-сервис
session_manager = SessionManager()
chat_service = ChatService(model_adapter, session_manager)


class ChatRequest(BaseModel):
    session_id: str
    user_message: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = chat_service.process_message(request.session_id, request.user_message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
