import os
import docx
import jieba
import jieba.analyse
import json
from aipClient import nlpClient
from win32com import client as wc


def gci(filepath):
    # 遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:
            ext = os.path.splitext(fi_d)[1]
            text = ''
            if ext == '.doc':
                wordApp = wc.Dispatch('Word.Application')
                doc = wordApp.Documents.Open(fi_d)
                doc.SaveAs(fi_d + 'x', 16)
                doc.Close()
                wordApp.Quit()
                os.remove(fi_d)
                ext = '.docx'
                fi_d += 'x'
            if (ext == '.docx'):
                for para in docx.Document(fi_d).paragraphs:
                    text += para.text
                print(text)
                txtName = os.path.splitext(fi_d)[0] + '.txt'
                with open(txtName, mode='w+') as f:
                    keyword = nlpClient.keyword(fi, text)
                    topic = nlpClient.topic(fi, text)
                    commentTag = nlpClient.commentTag(text)
                    print(commentTag)
                    if (topic.keys().__contains__('item')):
                        f.write('文件分类： ' + json.dumps(topic['item'], ensure_ascii=False) + '\n')
                    if (keyword.keys().__contains__('items')):
                        f.write('标签： ' + json.dumps(keyword['items'], ensure_ascii=False) + '\n')
                    if commentTag.keys().__contains__('items'):
                        f.write('文件分类： ' + json.dumps(commentTag['items'], ensure_ascii=False) + '\n')
                    f.write('关键词: ' + ','.join(jieba.analyse.extract_tags(text, 10)) + '\n')
        # print(text)
        # print(','.join(jieba.analyse.extract_tags(text)))
        # result=nlpClient.keyword(fi, text)
        # print(result['items'][1])
        # print(nlpClient.topic(fi, text))
        # print(nlpClient.commentTag(text))


gci('D:\\2018work')
# output = pypandoc.convert_file('somefile.md', 'docx', outputfile="somefile.docx")
