# DocVQA

## main.py
执行 main.py 内的main函数即可启动项目。

## model
model包下的每个类都是对大模型的封装，要注意模型的加载路径。最好将模型下载到本地再加载本地路径。

## text_splitter
分词用的，现在没有用到。如果要对pdf文档中的飞表格数据进行操作，可能会用到。

## 构建词向量库预训练模型
### 下载预训练模型到本地：
https://huggingface.co/hfl/chinese-roberta-wwm-ext
并将DocVQA/vectorstore/faiss.py第七行的文件路径修改为本地模型

## 微调部分
### 代码链接：
https://github.com/hiyouga/ChatGLM-Efficient-Tuning
### 最终模型的数据集位置：
DocVQA/utils/train_data/train_data1.json
用生成的数据集训练之后需要导出模型再由系统进行调用
### 导出命令：
python src/export_model.py \
    --model_name_or_path path_to_your_chatglm_model \
    --finetuning_type lora \
    --checkpoint_dir path_to_checkpoint \
    --output_dir path_to_export

## 生成训练数据
python DocVQA/utils/train_data.py