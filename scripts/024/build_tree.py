import argparse
import re
from pathlib import Path
import sys

def create_structure_from_tree(input_file: str, output_dir: str):
    base_path = Path(output_dir)
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Regex to capture the structural prefix (lines, spaces) and the actual name.
    # \u00A0 handles non-breaking spaces often created when copying/pasting from the web.
    line_pattern = re.compile(r'^([│├└─\| \t\u00A0]*)(.*)$')
    
    # The stack stores tuples of (indentation_length, directory_path).
    # We initialize with -1 so the root output directory is never popped off the stack.
    path_stack = [(-1, base_path)]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Strip trailing whitespace and newlines, but preserve leading characters
                line = line.rstrip()
                if not line:
                    continue
                    
                match = line_pattern.match(line)
                if not match:
                    continue
                    
                prefix, name = match.groups()
                name = name.strip()
                
                # Skip if there's no valid name after the structural prefix
                if not name:
                    continue
                    
                indent_length = len(prefix)
                
                # Pop directories from the stack until we find the parent.
                # The parent's indentation MUST be strictly less than the current line's.
                while path_stack and path_stack[-1][0] >= indent_length:
                    path_stack.pop()
                    
                parent_path = path_stack[-1][1]
                
                # Check if the current item is a directory (indicated by a trailing '/')
                is_dir = name.endswith('/')
                clean_name = name.rstrip('/')
                
                current_path = parent_path / clean_name
                
                if is_dir:
                    current_path.mkdir(parents=True, exist_ok=True)
                    path_stack.append((indent_length, current_path))
                    print(f"📁 Created directory: {current_path}")
                else:
                    # Create parent directories just in case the tree format implies them
                    current_path.parent.mkdir(parents=True, exist_ok=True)
                    current_path.touch()
                    print(f"📄 Created file:      {current_path}")
                    
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a directory tree from a text file.")
    parser.add_argument("input_file", help="Text file containing the tree structure")
    parser.add_argument("output_dir", help="Destination directory to build the tree in")
    
    args = parser.parse_args()
    
    print(f"Building tree from '{args.input_file}' into '{args.output_dir}'...\n")
    create_structure_from_tree(args.input_file, args.output_dir)
    print("\nDone!")