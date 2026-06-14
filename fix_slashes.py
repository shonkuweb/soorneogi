import glob

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Replace \' with '
    content = content.replace("\\'", "'")

    with open(file, 'w') as f:
        f.write(content)
        
    print(f"Fixed slashes in {file}")
