from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from transformers.generation import GenerationConfig
from model.base import ChatModel
# from base import ChatModel
import json


class Qwen(ChatModel):
    
    def __init__(self):
        # 请注意：分词器默认行为已更改为默认关闭特殊token攻击防护。相关使用指引，请见examples/tokenizer_showcase.ipynb
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True)

        # 打开bf16精度，A100、H100、RTX3060、RTX3070等显卡建议启用以节省显存
        # model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True, bf16=True).eval()
        # 打开fp16精度，V100、P100、T4等显卡建议启用以节省显存
        # model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True, fp16=True).eval()
        # 使用CPU进行推理，需要约32GB内存
        # model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="cpu", trust_remote_code=True).eval()
        # 默认使用自动模式，根据设备自动选择精度
        # model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()
        # 使用8bit量化模型
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        self.model = AutoModelForCausalLM.from_pretrained(
            'Qwen/Qwen-7B-Chat',
            device_map="cuda:0",
            quantization_config=quantization_config,
            trust_remote_code=True,
        ).eval()
        # 可指定不同的生成长度、top_p等相关超参
        self.model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True)

    def chat(self, message, context, history):
        prompt = """
        请根据上下文信息回答问题：
        目前已知以下信息：
        {}
        问：{}
        """.format(context, message)
        # prompt = gen_tools_prompt(message)
        print("=" * 50)
        print("question: ", prompt)
        print("=" * 50)
        response, history = self.model.chat(self.tokenizer, prompt, history=[])
        print("response: ", response)
        print("=" * 50)
        return response, history

def gen_tools_prompt(query):
    TOOLS = [
        {
            'name_for_human':
            '计算器',
            'name_for_model':
            'calculator',
            'description_for_model':
            '计算器是计算数据用的，可以快速计算并保证不出误差，可以计算整形和浮点类型等各种数据的加减乘除结果。涉及到计算的地方都应交给计算器计算！',
            'parameters': [{
                'name': 'search_query',
                'description': '要计算的数据公式',
                'required': True,
                'schema': {
                    'type': 'string'
                },
            }],
        },
    ]
    TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""

    REACT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

                    {tool_descs}

                    Use the following format:

                    Question: the input question you must answer
                    Thought: you should always think about what to do
                    Action: the action to take, should be one of [{tool_names}]
                    Action Input: the input to the action
                    Observation: the result of the action
                    ... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
                    Thought: I now know the final answer
                    Final Answer: the final answer to the original input question

                    Begin!

                    Question: {query}"""

    tool_descs = []
    tool_names = []
    for info in TOOLS:
        tool_descs.append(
            TOOL_DESC.format(
                name_for_model=info['name_for_model'],
                name_for_human=info['name_for_human'],
                description_for_model=info['description_for_model'],
                parameters=json.dumps(
                    info['parameters'], ensure_ascii=False),
            )
        )
        tool_names.append(info['name_for_model'])
    tool_descs = '\n\n'.join(tool_descs)
    tool_names = ','.join(tool_names)

    prompt = REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names, query=query)
    return prompt

if __name__ == "__main__":
    chat_model = Qwen()
    question = '2022年06月30日的流动资产合计是65776909579.15元。2021年12月31日的流动资产合计是70233588960.32元。问：流动资产合计同比增长率是多少？'
    chat_model.chat(gen_tools_prompt(question), "", [])
