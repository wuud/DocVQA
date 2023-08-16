import hanlp
import jieba

# 创建停用词列表 使用哈工大的停用词表
def stopwordslist():
    stopwords = [line.strip() for line in open('/mnt/workspace/DocVQA/src/ner/hit_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords

def seg_depart(sentence, key_list):
    # 对文档中的每一行进行中文分词
    x = key_list
    for i in range(len(x)):
        jieba.add_word(x[i])

    sentence_depart = jieba.cut(sentence, cut_all=False)
    # print('/'.join(sentence_depart))
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += ""
    print(outstr)
    return outstr

def NER(sentence, key_list):
    sentence = seg_depart(sentence, list(key_list))
    # 分词结果
    tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
    sen_tok = tok(sentence)

    # 加载预训练模型进行命名实体识别任务
    ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_ELECTRA_SMALL_ZH)

    out_put = ner([sen_tok], tasks='ner*')
    # 命名实体识别结果
    print(ner([sen_tok], tasks='ner*'))

    out_list = out_put[0]
    # dic = {'ORGANIZATION': None, 'DATE': None}
    # for i in range(len(out_list)):
    #     if out_list[i][1] == 'ORGANIZATION':
    #         dic['ORGANIZATION'] = out_list[i][0]
    #     if out_list[i][1] == 'DATE':
    #         dic['DATE'] = out_list[i][0]

    # if dic['ORGANIZATION'] is not None:
    #     sentence = sentence.replace(dic['ORGANIZATION'], "")

    # if dic['DATE'] is not None:
    #     new_str = sentence.replace(dic['DATE'], "")
    # print(new_str)

    for i in range(len(out_list)):
        if out_list[i][1] == 'ORGANIZATION' or out_list[i][1] == 'DATE':
            sentence = sentence.replace(out_list[i][0], "")
    print(sentence)

    return sentence

