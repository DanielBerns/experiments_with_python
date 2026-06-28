import sys
import os
from PIL import Image, ImageDraw

def draw_grid(image_path, grid_size=100, line_color='red', line_thickness=2):
    try:
        # Generate output filename dynamically
        # internal_photo.jpg -> internal_photo_with_grid.jpg
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_with_grid{ext}"

        # Load image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # Draw vertical lines
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=line_color, width=line_thickness)

        # Draw horizontal lines
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=line_color, width=line_thickness)

        image.save(output_path)
        print(f"Success! Grid saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check if user provided a filename
    if len(sys.argv) < 2:
        print("Usage: python grid_maker.py <image_file>")
    else:
        # Get filename from command line argument
        input_file = sys.argv[1]

        # You can still change grid settings here
        GRID_PIXELS = 150
        COLOR = 'red'

        draw_grid(input_file, GRID_PIXELS, COLOR)
