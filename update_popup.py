import os
import re

directory = '/Users/shonkuweb/soorneogi/SoorNeogiWeb'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

target_content = """            // Trigger after 2.5 seconds
            setTimeout(openModal, 2500);"""

replacement_content = """            // Trigger after 2.5 seconds if not shown before
            if (!localStorage.getItem('popupShown')) {
                setTimeout(() => {
                    openModal();
                    localStorage.setItem('popupShown', 'true');
                }, 2500);
            }"""

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if target_content in content:
        new_content = content.replace(target_content, replacement_content)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"Target content not found in {filename}")
