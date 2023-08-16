from transformers import AutoTokenizer, AutoModel
from model.base import ChatModel


class ChatGLM2(ChatModel):

    def __init__(self):
        model_name_or_path = '/root/.cache/huggingface/chatglm2'

        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True).half().cuda()
        self.model = self.model.eval()

    def chat(self, message, context, history):
        prompt = """
        请根据上下文信息回答问题。
        目前已知以下信息：
        {}
        问：{}。
        """.format(context, message)
        print("=" * 50)
        print("question: ", prompt)
        print("=" * 50)
        response, history = self.model.chat(self.tokenizer, prompt, history=[])
        print("response: ", response)
        print("=" * 50)
        return response, history
