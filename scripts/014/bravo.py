# robust_ocr.py
import pytesseract
import re
from PIL import Image

# If you don't have tesseract in your PATH, include the following line
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Example for Windows

def extract_price(text):
    """
    Finds a price in the text using a regular expression.
    Looks for currency symbols like $, €, £ followed by numbers.
    """
    # Regex to find prices (e.g., $19.99, € 20, 19.99€)
    price_patterns = [
        r'[\$€£]\s*\d+\.?\d*',  # $19.99 or € 20
        r'\d+\.?\d*\s*[\$€£]',  # 19.99$ or 20 €
        r'\d+,\d+\s*[\$€£]',    # 19,99€ (common in Europe)
    ]

    for pattern in price_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()
    return "Price not found"

def extract_description(text, price):
    """
    Tries to extract the product description.
    This is a heuristic: it assumes the description is the main block of text,
    often before the price.
    """
    # Remove the price from the text to avoid confusion
    if price != "Price not found":
        text = text.replace(price, '')

    # Split text into lines and clean them up
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Heuristic: The description is often the longest line or the first few lines.
    # Let's try to find the longest line that isn't just a number or a single word.
    description_lines = []
    for line in lines:
        # Filter out lines that are likely not the description
        if not re.fullmatch(r'[\d\.\,\/\-\s]+', line) and len(line.split()) > 1:
            description_lines.append(line)

    if description_lines:
        # Return the most substantial line found
        return max(description_lines, key=len)

    # Fallback: if no good lines are found, return the first line
    return lines[0] if lines else "Description not found"


def main():
    image_path = "/home/dberns/Documents/money/1760052973030-310090b1-4618-410e-8302-e17ad43a2943_.jpg"
    try:
        # Open the image file
        img = Image.open(image_path)

        # Use Tesseract to extract text
        # Using German and English language packs can improve accuracy for some products
        # e.g., pytesseract.image_to_string(img, lang='eng+deu')
        extracted_text = pytesseract.image_to_string(img, lang="spa")

        print("--- Raw Extracted Text ---")
        print(extracted_text)
        print("-" * 25)

        # Find the price and description
        price = extract_price(extracted_text)
        description = extract_description(extracted_text, price)

        print("--- Structured Data ---")
        print(f"Description: {description}")
        print(f"Price:       {price}")

    except FileNotFoundError:
        print(f"Error: The image file '{image_path}' was not found.")
        print("Please make sure the image is in the same directory as the script.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
