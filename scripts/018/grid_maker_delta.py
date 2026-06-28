import sys
import os
from PIL import Image, ImageDraw, ImageFont

def get_font(grid_size):
    """
    Attempts to load a standard system font (Arial) scaled to the grid size.
    Falls back to the default PIL font if Arial is missing.
    """
    # Estimate font size based on grid square size (approx 30% of grid box)
    font_size = int(grid_size * 0.3)
    if font_size < 10: font_size = 10

    try:
        # Try loading Arial (Windows/macOS standard)
        return ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        try:
            # Try DejaVuSans (Linux standard)
            return ImageFont.truetype("DejaVuSans.ttf", font_size)
        except IOError:
            # Fallback to default (tiny, but works everywhere)
            return ImageFont.load_default()

def draw_text_with_bg(draw, position, text, font, text_color='white', bg_color='black'):
    """Draws text with a small background box for better visibility."""
    left, top, right, bottom = draw.textbbox(position, text, font=font)
    # Add padding corresponding to the line width relative scale, or fixed 2px
    draw.rectangle((left-2, top-2, right+2, bottom+2), fill=bg_color)
    draw.text(position, text, fill=text_color, font=font)

def draw_grid_with_labels(image_path, grid_size=100, line_thickness=2, color='red'):
    try:
        # 1. Setup paths
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_with_grid{ext}"

        # 2. Load Image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # 3. Setup Font
        font = get_font(grid_size)

        # 4. Draw Vertical Lines & Column Numbers (1, 2, 3...)
        col_count = 1
        for x in range(0, width, grid_size):
            # Draw Line
            draw.line([(x, 0), (x, height)], fill=color, width=line_thickness)

            # Draw Label
            if x + 5 < width:
                label = str(col_count)
                # Position: Top edge, slightly offset inside the square
                draw_text_with_bg(draw, (x + 5, 5), label, font, text_color='white', bg_color=color)
                col_count += 1

        # 5. Draw Horizontal Lines & Row Letters (A, B, C...)
        row_count = 0
        for y in range(0, height, grid_size):
            # Draw Line
            draw.line([(0, y), (width, y)], fill=color, width=line_thickness)

            # Draw Label
            if y + 5 < height:
                # Convert 0 -> A, 1 -> B, etc.
                label = chr(65 + row_count)
                # Position: Left edge, slightly offset down
                draw_text_with_bg(draw, (5, y + 5), label, font, text_color='white', bg_color=color)
                row_count += 1

        # 6. Save
        image.save(output_path)
        print(f"Success!")
        print(f"Grid Size: {grid_size}px | Line Width: {line_thickness}px")
        print(f"Saved to:  {output_path}")

    except FileNotFoundError:
        print(f"Error: Could not find file '{image_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # --- Argument Parsing ---
    args = sys.argv
    argc = len(args)

    if argc < 2:
        print("Usage: python grid_maker.py <filename> [grid_size] [line_width]")
        print("Example: python grid_maker.py photo.jpg 150 5")
    else:
        input_file = args[1]

        # Default values
        g_size = 100
        l_width = 2

        # Parse Grid Size (2nd argument)
        if argc > 2:
            try:
                g_size = int(args[2])
            except ValueError:
                print("Warning: Invalid grid size. Using default (100).")

        # Parse Line Width (3rd argument)
        if argc > 3:
            try:
                l_width = int(args[3])
            except ValueError:
                print("Warning: Invalid line width. Using default (2).")

        draw_grid_with_labels(input_file, g_size, l_width, 'red')
