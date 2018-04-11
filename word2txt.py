from win32com import client as wc
import os
import fnmatch

all_FileNum = 0
debug = 0


def Translate(path):
    '''
    ��һ��Ŀ¼������doc��docx�ļ�ת��txt
    ��Ŀ¼�´���һ����Ŀ¼newdir
    ��Ŀ¼��fileNames.txt����һ���ı��������е�word�ļ���
    ���汾����һ�����ݴ��ԣ��������ͬһ�ļ��ж�β�������������ͻ
    '''
    global debug, all_FileNum
    if debug:
        print
        path
    # ��Ŀ¼�������ļ�������
    files = os.listdir(path)
    # ��Ŀ�´���һ����Ŀ¼newdir��������ת�����txt�ı�
    New_dir = os.path.abspath(os.path.join(path, 'newdir'))
    if not os.path.exists(New_dir):
        os.mkdir(New_dir)
    if debug:
        print
        New_dir
    # ����һ���ı��������е�word�ļ���
    fileNameSet = os.path.abspath(os.path.join(New_dir, 'fileNames.txt'))
    o = open(fileNameSet, "w")
    try:
        for filename in files:
            if debug:
                print
                filename
            # �������word�ļ�������
            if not fnmatch.fnmatch(filename, '*.doc') and not fnmatch.fnmatch(filename, '*.docx'):
                continue;
            # �����word��ʱ�ļ�������
            if fnmatch.fnmatch(filename, '~$*'):
                continue;
            if debug:
                print
                filename
            docpath = os.path.abspath(os.path.join(path, filename))

            # �õ�һ���µ��ļ���,��ԭ�ļ����ĺ�׺�ĳ�txt
            new_txt_name = ''
            if fnmatch.fnmatch(filename, '*.doc'):
                new_txt_name = filename[:-4] + '.txt'
            else:
                new_txt_name = filename[:-5] + '.txt'
            if debug:
                print
                new_txt_name
            word_to_txt = os.path.join(os.path.join(path, 'newdir'), new_txt_name)
            print
            word_to_txt
            wordapp = wc.Dispatch('Word.Application')
            doc = wordapp.Documents.Open(docpath)
            # Ϊ����python�����ں���������r��ʽ��ȡtxt�Ͳ��������룬����Ϊ4
            doc.SaveAs(word_to_txt, 4)
            doc.Close()
            o.write(word_to_txt + '\n')
            all_FileNum += 1
    finally:
        wordapp.Quit()


if __name__ == '__main__':
    print
    '''
        ��һ��Ŀ¼������doc��docx�ļ�ת��txt
        ��Ŀ�´���һ����Ŀ¼newdir
        ��Ŀ¼��fileNames.txt����һ���ı��������е�word�ļ���
        ���������һ�����ݴ���
    '''
    print('Enter your Director\'s path:')
    print("·����\��\\��ʾ����")
    mypath = raw_input()
    print('���ɵ��ļ���:')
    Translate(mypath)
    print
    'The Total Files Numbers = ', all_FileNum
    raw_input()



