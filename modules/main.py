from .OCR import *
from .Pdfextract import *


def main(filename):
    execute(filename)
    page, label, idDict = label_it(filename)
    return page, label, idDict


if __name__ == '__main__':
    main()