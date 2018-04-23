import json
import os  
from wand.image import Image
import PyPDF2
from aip import AipOcr

APP_ID = '11078570'
API_KEY = 'x5Z8zdUaLX8ESome8geb2kbB'
SECRET_KEY = 'V7GZ8pMAF4WVZ5HmAyT441SfL1X6ILRY'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def convert_pdf_to_jpg(filename):
    with Image(filename=filename) as img :
        print('pages = ', len(img.sequence))

        with img.convert('png') as converted:
            converted.save(filename='./projects/ocr/img/page.png')

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def traverse(f):  
    fs = os.listdir(f)  
    for f1 in fs:  
        tmp_path = os.path.join(f,f1)  
        if not os.path.isdir(tmp_path):  
            print('file : %s'%tmp_path)  
        else:  
            print('folder ：%s'%tmp_path)  
            traverse(tmp_path)


convert_pdf_to_jpg('./projects/ocr/bad.pdf')
folder = './projects/ocr/img'
fs = os.listdir(folder)
for f1 in fs:
     tmp_path = os.path.join(folder,f1)
     if not os.path.isdir(tmp_path): 
         if not 'DS_Store' in tmp_path:
             image = get_file_content(tmp_path)
             dict_code = client.basicAccurate(image)
             json_code = json.dumps(dict_code)
             text_code = json.loads(json_code)
             for item in text_code['words_result']:
                    print(item.get('words'))


