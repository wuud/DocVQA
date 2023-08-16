from abc import abstractmethod


class ChatModel:
    @abstractmethod
    def chat(self, message,context, history):
        pass
