import os


def findFile(file_path, file_type):
    """递归查找指定文件类型的文件列表"""
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


def sougou_to_dict(input_file_path, out_dict_path):
    """将搜狗导出的词汇txt文件转为结巴分词的格式"""
    inputlines = open(input_file_path, mode='r').readlines()
    outlines = open(out_dict_path, mode='a+', encoding='utf-8')
    for line in inputlines:
        outlines.write(line.split(' ')[-1])
    outlines.close()

