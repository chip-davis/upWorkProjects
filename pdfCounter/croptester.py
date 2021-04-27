import pdfplumber
import pypdfocr


# pdf = pdfplumber.open(r"C:\Users\Chip\Documents\upWorkProjects\PDFcounter\PDFs\therewerenone.pdf")
# page = pdf.pages[0]


# bottom_left = page.crop((0, 0.08 * float(page.height), page.width, page.height))
# test = bottom_left.extract_text(x_tolerance=3, y_tolerance=3).split("\n")
# im = bottom_left.to_image(resolution=150) 
# im.save('test.png', format="PNG")
# print(test)

from pypdfocr import pypdfocr
from pypdfocr.pypdfocr import PyPDFOCR as pocr

filepath = r'C:\Users\Chip\Documents\upWorkProjects\PDFcounter\PDFs\andThenThereWereNoneReg.pdf'

my_ocr = pocr()

newfile = my_ocr.run_conversion(filepath)