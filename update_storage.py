import os

directory = '/Users/shonkuweb/soorneogi/SoorNeogiWeb'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    
    if 'sessionStorage.getItem("enquiryModalShown")' in content:
        content = content.replace('sessionStorage.getItem("enquiryModalShown")', 'localStorage.getItem("popupShown")')
        modified = True
        
    if 'sessionStorage.setItem("enquiryModalShown"' in content:
        content = content.replace('sessionStorage.setItem("enquiryModalShown"', 'localStorage.setItem("popupShown"')
        modified = True
        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {filename}")
