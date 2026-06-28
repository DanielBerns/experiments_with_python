from PIL import Image, ImageDraw
import sys

def draw_grid(image_path, output_path, grid_size=100, line_color='red', line_thickness=2):
    """
    Draws a grid over an image.

    :param image_path: Path to the source image.
    :param output_path: Where to save the modified image.
    :param grid_size: The size of the grid squares in pixels.
    :param line_color: Color of the grid lines (name or hex code).
    :param line_thickness: Thickness of the grid lines in pixels.
    """
    try:
        # Load the image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        width, height = image.size

        # Draw vertical lines
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=line_color, width=line_thickness)

        # Draw horizontal lines
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=line_color, width=line_thickness)

        # Save the result
        image.save(output_path)
        print(f"Success! Grid image saved to: {output_path}")

    except FileNotFoundError:
        print("Error: The file was not found. Check your path.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Configuration ---
if __name__ == "__main__":
    # CHANGE THESE VALUES
    INPUT_FILE = "reference_photo.jpg"  # Replace with your image name
    OUTPUT_FILE = "reference_with_grid.jpg"
    SQUARE_SIZE = 150                   # Size of the grid box in pixels
    COLOR = (255, 0, 0)                 # Red in RGB, or use string 'cyan', 'yellow'

    draw_grid(INPUT_FILE, OUTPUT_FILE, SQUARE_SIZE, COLOR, 2)
