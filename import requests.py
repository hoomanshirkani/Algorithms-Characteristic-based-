import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import pytesseract
import cv2
import numpy as np
from selenium import webdriver

# Start a browser session
browser = webdriver.Firefox()

# Navigate to the page
browser.get('https://www.ninisite.com/imen/mobileregister')

# Find the CAPTCHA image element
captcha_element = browser.find_element_by_css_selector('.imen-box .center-box-item .captcha-addon img')

# Get the image as bytes
captcha_bytes = captcha_element.screenshot_as_png

# Convert the bytes to a numpy array for OpenCV processing
img_np = np.frombuffer(captcha_bytes, np.uint8)
img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

# Convert to grayscale
grayscale = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresholded = cv2.threshold(grayscale, 128, 255, cv2.THRESH_BINARY)

# Convert the OpenCV image back to PIL format
img_pil = Image.fromarray(cv2.cvtColor(thresholded, cv2.COLOR_GRAY2RGB))

# Use pytesseract to extract text with a configuration for recognizing numbers only
captcha_text = pytesseract.image_to_string(img_pil, config='--psm 6 outputbase digits').strip()

# Ensure that the result is exactly four digits (this could also help in filtering out false results)
if len(captcha_text) == 4 and captcha_text.isdigit():
    print(captcha_text)
else:
    print("Failed to recognize the CAPTCHA")
