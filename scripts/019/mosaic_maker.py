from PIL import Image

def create_pixel_mosaic(input_image: Image.Image) -> Image.Image:
    """
    Creates a mosaic where the top-left is the original image, and the
    other three quadrants are solid blocks of the color found at
    pixel (3, 3) of the original image.

    Args:
        input_image (PIL.Image): The source image.

    Returns:
        PIL.Image: The resulting mosaic image (2x width, 2x height).

    Raises:
        ValueError: If the input image is too small (less than 4x4 pixels).
    """
    # Ensure image is large enough to have a pixel at index (3,3)
    width, height = input_image.size
    if width <= 3 or height <= 3:
        raise ValueError(f"Image is too small ({width}x{height}). Must be at least 4x4 pixels.")

    # Get the color at position (3, 3).
    # Note: (3, 3) implies the 4th column and 4th row in 0-indexed systems.
    target_color = input_image.getpixel((3, 3))

    # Calculate new dimensions
    new_width = width * 2
    new_height = height * 2

    # Create the new canvas initialized entirely with the target color.
    # This automatically handles the Top-Right, Bottom-Left, and Bottom-Right quadrants.
    mosaic_image = Image.new(input_image.mode, (new_width, new_height), target_color)

    # Paste the original image into the Top-Left quadrant (0, 0)
    mosaic_image.paste(input_image, (0, 0))

    return mosaic_image

# --- Example Usage ---
if __name__ == "__main__":
    try:
        # Load an example image
        # Replace 'input.jpg' with your actual file path
        original = Image.open("input.jpg")

        # Process the image
        result = create_pixel_mosaic(original)

        # Save the output
        result.save("output_mosaic.jpg")
        print("Mosaic created successfully.")

    except FileNotFoundError:
        print("Error: The input file was not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
