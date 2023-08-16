from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from text_splitter.chinese_text_splitter import ChineseTextSplitterForTableData
from sentence_transformers import SentenceTransformer,util

model_path = '/mnt/workspace/text2vec-large-chinese'
model = SentenceTransformer(model_path)
device = 'cuda'

def get_file_vector_store(source_file):
    loader = TextLoader(source_file, encoding='utf-8')
    documents = loader.load()
    text_splitter = ChineseTextSplitterForTableData()
    docs = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=model_path, model_kwargs={'device': device})
    db = FAISS.from_documents(docs, embeddings)
    return db

def get_texts_vector_store(texts):
    embeddings = HuggingFaceEmbeddings(model_name=model_path, model_kwargs={'device': device})
    db = FAISS.from_texts(texts, embeddings)
    return db

# 最大边际相关算法
def max_marginal_relevance_search_by_words(vectorstore, words):
    print("===================================")
    print(words)
    res = []
    for word in words:
        docs = vectorstore.similarity_search_with_relevance_scores(word)
        # marginal_relevance = vectorstore.max_marginal_relevance_search_with_score_by_vector(word)
        content = docs[0][0].page_content
        score = docs[0][1]
        res.append(content)
    print(res)
    print("===================================")
    return res


# 利用余弦相似度算法啊，计算两个词之间的相似度
def cos_similarity_search_by_words(word, core):
    word_embedding = model.encode(word, convert_to_tensor=True)
    core_embdding = model.encode(core, convert_to_tensor=True)
    sim = util.pytorch_cos_sim(core_embdding, word_embedding)
    return sim
