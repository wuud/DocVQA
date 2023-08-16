from transformers import AutoTokenizer, AutoModel
from model.base import ChatModel


class ChatGLM(ChatModel):

    def __init__(self):
        model_name_or_path = 'THUDM/chatglm-6b'

        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True).half().cuda()

    def chat(self, message, context, history):
        prompt = """
        请根据上下文信息回答问题。注意：问题不涉及到任何计算，禁止加减计算，请直接检索并回答。
        目前已知以下信息：
        {}
        问：{}。禁止加减计算！
        """.format(context, message)
        print("=" * 50)
        print("question: ", prompt)
        print("=" * 50)
        # response, history = model.chat(tokenizer, prompt, history=history)
        response, history = self.model.chat(self.tokenizer, prompt, history=[])
        print("response: ", response)
        print("=" * 50)
        return response, history


if __name__ == "__main__":
    message = '你是谁'
    # chat(message, '', [])
