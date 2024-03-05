# importing required libraries
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path

# loading pdf file to convert it into an image
# returns PpmImageFile object that is PIL image (Python Imaging Library now called Pillow)
pdf_image = convert_from_path('samplepdf.pdf')

# convert PIL to OpenCV format (numpy array)
# image = cv2.cvtColor(np.array(pdf_image[0]), cv2.COLOR_RGB2BGR)


# Image preprocessing : making sure if the image is in correct position / angle
# read README file for detailed explanation for this function
def deskew(image):
    # convert to black & white image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # inverting the pixels using bitwise_not
    gray = cv2.bitwise_not(gray)

    # Threshold the grayscale image to obtain a binary image
    binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # fetching coordinates of white pixels
    coords = np.column_stack(np.where(binary_img > 0)).astype(np.float32)

    # finding angle of the image
    angle = cv2.minAreaRect(coords)[-1]

    # adjusting image angle
    if angle > 45:
        adjust_angle = (90 - angle)
    else:
        adjust_angle = -angle

    # shape returns 3 values; (height, width, depth). Here we just need height and width
    (h, w) = gray.shape[:2]

    # finding center point of the image. // : operator is used as floor division, which means returns nearest whole number of the output
    center = (w // 2, h // 2)

    # getting the rotation matrix M
    M = cv2.getRotationMatrix2D(center=center, angle=adjust_angle, scale=1.0)

    # rotating the image
    fixed_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return fixed_image


def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text


# storing the extracted data in list
extracted_text = []

for page in pdf_image:
    # preprocess the image
    preprocessed_image = deskew(np.array(page))

    # extract text using OCR
    text = extract_text_from_image(preprocessed_image)
    extracted_text.append(text)

print(extracted_text)

