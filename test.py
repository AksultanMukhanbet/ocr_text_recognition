from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import pytesseract
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
    help="path to input image to be OCR'd")
ap.add_argument("-o", "--output", required=True,
    help="path to output image")
args = vars(ap.parse_args())

def ocr_core(img):
    text = pytesseract.image_to_string(img)
    return text

img = cv2.imread(args["input"])

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(img, 5)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

img = get_grayscale(img)
img = thresholding(img)
img = remove_noise(img)

lines = ocr_core(img)

with open(args["output"], 'w') as f:
    for line in lines:
        f.write(line)




#PDF
PDF_file = "images/2003.00744v1_image_pdf.pdf"

pages = convert_from_path(PDF_file, 500)
image_counter = 1

for page in pages:
    filename = "page_"+str(image_counter)+".jpg"
    page.save(filename, 'JPEG')
    image_counter = image_counter + 1

filelimit = image_counter - 1

f = open(args["output"], "a")

for i in range(1, filelimit + 1):
    filename = "page_"+str(i)+".jpg"

    text = str(((pytesseract.image_to_string(Image.open(filename)))))
    text = text.replace('-\n', '')

    f.write(text)

f.close()