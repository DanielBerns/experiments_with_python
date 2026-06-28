# tesseract_extractor.py

import pytesseract
from PIL import Image
import cv2
import numpy as np

# If Tesseract is not in your PATH, include the following line
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Example for Windows

# --- 1. SETUP ---
# Path to your supermarket ticket image
image_path = '/home/dberns/Documents/money/1760052973030-310090b1-4618-410e-8302-e17ad43a2943_.jpg'

try:
    # --- 2. IMAGE PROCESSING ---
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Error: The image at '{image_path}' could not be found or opened.")

    # Add this code after loading the image and before the OCR call

    # 1. Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Noise Reduction (e.g., using a median blur)
    # This helps remove small "salt and pepper" noise.
    denoised = cv2.medianBlur(gray, 3)

    # 3. Thresholding / Binarization
    # This converts the image to pure black and white, which makes text stand out.
    # Otsu's method automatically finds the best threshold value.
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Now, pass 'thresh' instead of the original image to the OCR function

    # --- 3. OCR EXTRACTION ---
    print(f"Extracting text from '{image_path}' using Tesseract...")

    # For Tesseract:
    text_data = pytesseract.image_to_string(thresh)
    detailed_data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)

    print("Extraction complete.")

    # --- 4. DISPLAY RESULTS ---
    print("\n--- Extracted Text (as a single block) ---")
    print(text_data)

    print("\n--- Detailed Word-by-Word Extraction ---")
    n_boxes = len(detailed_data['level'])
    for i in range(n_boxes):
        text = detailed_data['text'][i].strip()
        confidence = int(detailed_data['conf'][i])

        # We only care about actual words with a decent confidence score
        if text and confidence > 30:
            (x, y, w, h) = (detailed_data['left'][i], detailed_data['top'][i], detailed_data['width'][i], detailed_data['height'][i])
            print(f"Text: '{text}' (Confidence: {confidence}%)")

            # Draw bounding box on the original image
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Display the image with bounding boxes
    print("\nDisplaying image with detected text boxes. Close the window to exit.")
    cv2.imshow('Tesseract Results', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure Tesseract is installed and in your system's PATH.")
