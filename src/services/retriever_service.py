# services/retriever_service.py
from transformers import pipeline

class RetrieverService:
    def __init__(self, model_name, concatenated_text):
        self.model_name = model_name
        self.concatenated_text = concatenated_text
        self.retriever = pipeline("question-answering", model=model_name, tokenizer=model_name)

    def query_retriever(self, user_query):
        result = self.retriever({
            "question": user_query,
            "context": self.concatenated_text
        })
        return result["answer"]
