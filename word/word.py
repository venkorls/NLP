import os
import docx
import jieba
import jieba.analyse
import json
from common.mysqlHelper import Zs_extractInfo, DBSession
from common.aipClient import nlpClient
from win32com import client as wc


def findFile(file_path, file_type):
    #递归查找指定文件类型的文件列表
    file_list = []
    if os.path.isfile(file_path):
        file_list.append(file_path)
    else:
        for top, dirs, files in os.walk(file_path):
            for filename in files:
                fileExt = os.path.splitext(filename)[1]
                if filename.endswith(file_type):
                    abspath = os.path.join(top, filename)
                    file_list.append(abspath)
    return file_list


def doc2docx(doc_path):
    wordApp = wc.Dispatch('Word.Application')
    doc = wordApp.Documents.Open(doc_path)
    doc.SaveAs(doc_path + 'x', 16)
    doc.Close()
    wordApp.Quit()
    os.remove(doc_path)


def gci(filepath):
    # 遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    sess = DBSession()
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
                print('当前正在处理：' + fi_d + '......')
                zsinfo = Zs_extractInfo()
                for para in docx.Document(fi_d).paragraphs:
                    text += para.text
                txtName = os.path.splitext(fi_d)[0] + '.txt'
                with open(txtName, mode='w+') as f:
                    try:
                        topic = nlpClient.topic(fi, text)
                        if (topic.keys().__contains__('item')):
                            zsinfo.topic = json.dumps(topic['item'], ensure_ascii=False)
                            f.write('分类： ' + json.dumps(topic['item'], ensure_ascii=False) + '\n')
                    except:
                        f.write('分类：出现异常' + '\n')
                    try:
                        keyword = nlpClient.keyword(fi, text)
                        if (keyword.keys().__contains__('items')):
                            zsinfo.tags = json.dumps(keyword['items'], ensure_ascii=False)
                            f.write('标签： ' + json.dumps(keyword['items'], ensure_ascii=False) + '\n')
                    except:
                        f.write('标签:出现异常' + '\n')
                    try:
                        commentTag = nlpClient.commentTag(text)
                        zsinfo.comments = json.dumps(commentTag, ensure_ascii=False)
                        f.write('观点抽取： ' + json.dumps(commentTag, ensure_ascii=False) + '\n')
                    except:
                        f.write('观点抽取： 出现异常' + '\n')
                    keywords = ','.join(jieba.analyse.extract_tags(text, 25))
                    zsinfo.keywords = json.dumps(keywords, ensure_ascii=False)
                    f.write('关键词: ' + keywords + '\n')
                    sess.add(zsinfo)
                    sess.commit()
    sess.close()
    print('处理成功！')
    # print(text)
    # print(','.join(jieba.analyse.extract_tags(text)))
    # result=nlpClient.keyword(fi, text)
    # print(result['items'][1])
    # print(nlpClient.topic(fi, text))
    # print(nlpClient.commentTag(text))

doclist=findFile('d:\\0.红河州', '.doc')
print(doclist)
for doc in doclist:
    try:
        doc2docx(doc)
    except:
        continue
docxlist=findFile('d:\\0.红河州', '.docx')
print(docxlist)


