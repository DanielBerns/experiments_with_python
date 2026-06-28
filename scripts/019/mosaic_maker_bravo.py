import argparse
import sys
from PIL import Image

def create_pixel_mosaic(input_image: Image.Image) -> Image.Image:
    """
    Creates a mosaic where the top-left is the original image, and the
    other three quadrants are solid blocks of the color found at
    pixel (3, 3) of the original image.
    """
    # Ensure image is large enough to have a pixel at index (3,3)
    width, height = input_image.size
    if width <= 3 or height <= 3:
        raise ValueError(f"Image is too small ({width}x{height}). Must be at least 4x4 pixels.")

    # Get the color at position (3, 3)
    target_color = input_image.getpixel((3, 3))

    # Calculate new dimensions (2x original)
    new_width = width * 2
    new_height = height * 2

    # Create canvas with the solid background color
    mosaic_image = Image.new(input_image.mode, (new_width, new_height), target_color)

    # Paste original image in top-left
    mosaic_image.paste(input_image, (0, 0))

    return mosaic_image

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(
        description="Generate a mosaic image based on pixel (3,3) color."
    )

    # Add arguments
    parser.add_argument("input_file", type=str, help="Path to the input image file")
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="mosaic_output.jpg",
        help="Path to save the output image (default: mosaic_output.jpg)"
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        with Image.open(args.input_file) as original:
            # Force load image data so it persists after file close (optional depending on PIL version)
            original.load()

            print(f"Processing '{args.input_file}'...")
            result = create_pixel_mosaic(original)

            result.save(args.output)
            print(f"Success! Mosaic saved to '{args.output}'")

    except FileNotFoundError:
        print(f"Error: The file '{args.input_file}' was not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error processing image: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
