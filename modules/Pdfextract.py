import os
import pdf2image


def convert(path_name, output_path):

    print("Converting pdf to images. . . Wait")
    result = pdf2image.convert_from_path(pdf_path=path_name, output_folder=output_path,
                                         fmt='jpeg',
                                         jpegopt={"quality": 100, "progressive": True, "optimize": True},
                                         paths_only=True, grayscale=True, dpi=500, thread_count=4)
    return result


def execute(filename):

    path_name = './labreport/api_uploads/'+filename
    output_path = './data'

    if not os.path.exists('./data'):
        os.mkdir('./data')
    convert(path_name, output_path)

