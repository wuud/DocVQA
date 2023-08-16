import gradio as gr

def file_prcoessor(file):
    return file.name

def respond(question, chat_history):
    bot_message = "hello!"
    chat_history.append((question, bot_message))
    return "", chat_history


with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">财务报表智能问答系统</h1>""")
    with gr.Tab("对话"):
        with gr.Row():  # 并行显示，可开多列
            with gr.Column(scale=3):
                chatbot = gr.Chatbot()
                msg = gr.Textbox()
                clear = gr.ClearButton([msg, chatbot])
            with gr.Column(scale=1):
                file_input = gr.File(label="输入文件")
                file_submit = gr.Button("Submit")
    file_submit.click(file_prcoessor, inputs=[file_input], outputs = [msg])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(share=True)