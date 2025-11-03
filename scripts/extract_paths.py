import re
from pathlib import Path

# Read the HTML file
html_content = Path('/home/rudycosta3/claude-code-docs/temp.html').read_text()

# Find all paths containing /en/
# This regex matches /en/ followed by any non-whitespace, non-quote characters
pattern = r'/en/[^\s"\'<>&]+?(?=["\s<>&]|$)'
matches = re.findall(pattern, html_content)

# Get unique paths and sort them
unique_paths = sorted(set(matches))

# Print results
print(f"Found {len(unique_paths)} unique paths containing '/en/':\n")
for path in unique_paths:
    print(path)

# Also save to a file
output_file = Path('/home/rudycosta3/claude-code-docs/extracted_paths.txt')
output_file.write_text('\n'.join(unique_paths))
print(f"\n\nPaths saved to: {output_file}")
