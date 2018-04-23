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