import jieba
import jieba.posseg as pseg
import paddle


# 创建停用词列表 使用哈工大的停用词表
def stopwordslist():
    stopwords = [line.strip() for line in open('/mnt/workspace/DocVQA/src/ner/hit_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


# 对句子进行中文分词
def seg_depart(sentence):
    # 对句子进行中文分词
    sentence_depart = jieba.cut(sentence.strip())
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
    return outstr

def NER2(sentence):

    outstr = seg_depart(sentence)
    print("删除停用词和分词成功！！！")
    print(outstr)

    # 开启静态图模式
    paddle.enable_static()
    # # 引入paddle包，开启paddle模式
    jieba.enable_paddle()
    # 使用paddle分词，设置use_paddle=True
    texts = pseg.cut(outstr, use_paddle=True)
    print(texts)
    # 存放地名
    Location = []
    # 存放机构名
    Organization = []
    # 存放时间
    Time = []
    for text, flag in texts:
        if flag == 'LOC':
            Location.append(text)
        if flag == 'ORG':
            Organization.append(text)
            outstr = outstr.replace(text, "")
        if flag == 'TIME':
            Time.append(text)
            outstr = outstr.replace(text, "")
        print('%s %s' % (text, flag))
    print("===========")
    print("Location" + str(Location))
    print("Organization" + str(Organization))
    print("Time" + str(Time))
    print(outstr)

    return outstr

if __name__ == '__main__':
    sentence = "都城伟业公司2021年12月30日的资产总计是多少"

    x = NER2(sentence)
    print(x)
