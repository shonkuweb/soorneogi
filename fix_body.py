import os
import glob
import re

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Find <body class="...">
    # We want to insert overflow-x-hidden if it's not already there.
    
    body_pattern = re.compile(r'(<body[^>]*class=")([^"]*)(")')
    
    def replace_body(match):
        classes = match.group(2)
        if 'overflow-x-hidden' not in classes:
            classes = 'overflow-x-hidden ' + classes
        return match.group(1) + classes + match.group(3)

    content = body_pattern.sub(replace_body, content)

    with open(file, 'w') as f:
        f.write(content)
        
    print(f"Added overflow-x-hidden to {file}")
