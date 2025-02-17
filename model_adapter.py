from abc import ABC, abstractmethod
from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer
import openai


class ModelAdapter(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: List[str]) -> str:
        """
        Принимает основной запрос и историю диалога (context) и возвращает ответ модели.
        """
        pass


class RemoteAPIAdapter(ModelAdapter):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_response(self, prompt: str, context: List[str]) -> str:
        openai.api_key = self.api_key

        # Формируем историю сообщений для API (начальный системный промпт + история диалога)
        messages = [{"role": "system", "content": "Ты образовательный чат-бот."}]
        for msg in context:
            messages.append({"role": "user", "content": msg})
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content


class LocalModelAdapter(ModelAdapter):
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response(self, prompt: str, context: List[str]) -> str:
        # Объединяем контекст диалога и новый запрос
        full_prompt = "\n".join(context + [prompt])
        input_ids = self.tokenizer.encode(full_prompt, return_tensors="pt")
        outputs = self.model.generate(input_ids, max_length=512, do_sample=True)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
