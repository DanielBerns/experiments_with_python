# simple_ocr.py
import pytesseract
from PIL import Image

# If you don't have tesseract in your PATH, include the following line
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Example for Windows

try:
    # Open the image file
    # img = Image.open("/home/dberns/Documents/money/IMG_20250905_120634325.jpg")
    img = Image.open("/home/dberns/Documents/money/IMG_20251009_121413989.jpg")
    # Use Tesseract to extract text
    text = pytesseract.image_to_string(img)

    # Print the extracted text
    print("--- Extracted Text ---")
    print(text)

except FileNotFoundError:
    print("Error: The image file 'supermarket_card.jpg' was not found.")
    print("Please make sure the image is in the same directory as the script.")
except Exception as e:
    print(f"An error occurred: {e}")
