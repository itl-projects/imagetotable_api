from PIL import Image
import os
import pyocr
import pyocr.builders
import pandas as pd
from flashtext import KeywordProcessor


class OcrPdf:
    """
    Summary of class:
    Attributes:
        input_dir: input directory of images
    """

    def __init__(self, input_dir, filename):
        self.filename = filename.split('.pdf')[0]
        self.input_dir = input_dir
        self.idDict = None
        self.set_id()

    def set_id(self):
        """
        sets page number as id for images
        """
        idDict = {}
        files = [os.path.join(self.input_dir, f) for f in os.listdir(self.input_dir)]
        for file in files:
            name = file.split('-')[-1].split('.')[0]
            idDict[file] = name
        idDict = {k: v for k, v in sorted(idDict.items(), key=lambda item: item[1])}
        self.idDict = idDict

    def get_category(self):
        """
        Label each image based on keywords
        """
        keyword_dict = {'Lab Report': ['report', 'lab'],
                        'Radiology Report': ['C.T', 'C.A.T', 'Computerized Tomography',
                                             'MRI', 'Magnetic Image Reasoning',
                                             'Magnetic Resonance Angiography',
                                             'Ultrasound', 'USG/US'],
                        'Discharge Note': ['Discharge'],
                        'Procedures': ['Echocardiography', 'EGD', 'Holter', 'Colonoscopy']}

        # pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        tessdata_dir_config = r'--tessdata-dir "tessdata" --oem 1 --psm 3'

        tools = pyocr.get_available_tools()
        tool = tools[0]

        idList = []
        labelList = []

        for image_name in self.idDict.keys():

            id_num = self.idDict.get(image_name)
            idList.append(id_num)

            print("##Processing page {}".format(self.idDict.get(image_name)))
            text = tool.image_to_string(Image.open(image_name), lang='eng', builder=pyocr.builders.TextBuilder())

            processor = KeywordProcessor(case_sensitive=False)
            processor.add_keywords_from_dict(keyword_dict)
            label = processor.extract_keywords(text)

            if label:
                report_type = label[0]
            else:
                report_type = 'Misc'
            print(report_type)
            labelList.append(report_type)

            if os.path.exists('./PdfText'):
                os.chdir('./PdfText')
            else:
                os.mkdir('./PdfText')
                os.chdir('./PdfText')

            if report_type == 'Misc':
                with open(self.filename+'-Page{}_misc.txt'.format(id_num), 'w', encoding='utf-8') as misc_file:
                    misc_file.write(text)
            else:
                with open(self.filename+'-Page{}.txt'.format(id_num), 'w', encoding='utf-8') as misc_file:
                    misc_file.write(text)
            os.chdir('..')
        return idList, labelList, self.idDict


def label_it(filename):
    print("Here")
    obj = OcrPdf('./data/', filename)
    obj.set_id()
    page, label, idDict = obj.get_category()
    print(idDict)
    frame = pd.DataFrame(list(zip(page, label)), columns=['Page Number', 'Report Type'])
    frame.to_csv('label.csv', index=False)
    return page, label, idDict
