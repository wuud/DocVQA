import gradio as gr
import random
import time
import utils
from model.chatglm2 import ChatGLM2
from model.qwen import Qwen
from vectorstore import faiss
from utils import utils
from ner import ner, ner_2
from string_match import Fuzzy
from OCRTest import process
import os

chat_model = ChatGLM2()
#chat_model = Qwen()
#to do ocr
indicators = utils.FinancialIndicators()
vectorstore = None
key_words_vectorsore = None
content = None
ctx = None

# 系统的初始方法，提交文件时执行这个方法
def file_prcoessor(file, start, end):
    if file is None:
        return [(None, """<p align="center">文件不能为空！</p>""")]
    if start == "" or end == "":
        return [(None, """<p align="center">起止页码不能为空</p>""")]
    '''处理文件,生成向量库并赋值给vectorstore'''
    global indicators, vectorstore, key_words_vectorsore, content, ctx
    # TODO ocr
    content = process.main_process(file, page_start = start, page_end = end)
    ctx = utils.Context(content)
    print('--------------------ocr提取到的数据------------------')
    for line in ctx.data_.data_:
        print(line)
    model_keys = ctx.modelsMap_.keys()
    key_words_vectorsore = faiss.get_texts_vector_store(model_keys)
    print("---------------","成功生成词向量库","-------------------")
    print(model_keys)
    name = os.path.basename(file.name)
    return [(None, "文件[{}]提交成功！可以开始提问了。".format(name))] # 返回文件目录


# 跟据问题中的关键字匹配上下文
def search_context(question):
    global ctx
    model_keys = ctx.modelsMap_.keys()
    print(model_keys)
    # 文本匹配
    new_sentence = ner.NER(question, model_keys)

    words = []
    words.append(new_sentence)

    
    res_words = Fuzzy.string_match(new_sentence, model_keys)
    # res_words = faiss.max_marginal_relevance_search_by_words(key_words_vectorsore, words)
    print("---------------", "匹配到关键词", res_words, "--------------------")
    context = ""
    if res_words != None:
        for word in res_words:
            context += ctx.data_.getSentenceByKey(ctx.get(word).rawKey)
            context += "\n"
        print("---------------", "成功匹配到上下文", context, "-------------------")
        return context
    else:
        return None

# 对问题给出回答
def respond(question, chat_history):
    context = search_context(question)
    if context is None:
        bot_message = '抱歉，未在文档中匹配到相关上下文信息！'
    else:
        bot_message, _ = chat_model.chat(
        question, context, chat_history)
    chat_history.append((question, bot_message))
    return "", chat_history

block = gr.Blocks(theme='default', title="财务报表智能问答系统").queue(concurrency_count=1)
with block as demo:
    gr.HTML("""<h1 align="center">财务报表智能问答系统</h1>""")
    with gr.Tab("对话"):
        with gr.Row():  # 并行显示，可开多列
            with gr.Column(scale=3):
                init_msg = [(None, "请先在右侧提交相关文档，再提出问题！")]
                chatbot = gr.Chatbot(init_msg)
                msg = gr.Textbox(label='输入问题', placeholder='在此输入问题开始提问')
                submit = gr.Button("Submit", variant='primary')
            with gr.Column(scale=1):
                file_input = gr.File(label="输入文件")
                start = gr.Textbox(label='起始页码', placeholder='起始页码')
                end = gr.Textbox(label='终止页码', placeholder='终止页码')
                file_submit = gr.Button("Submit")
    file_submit.click(file_prcoessor, inputs=[file_input, start, end], outputs=[chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(share=True)
