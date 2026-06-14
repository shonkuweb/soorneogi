import os
import glob

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Find the old script block
    old_script_part1 = "mobileMenu.classList.remove('translate-x-full');"
    old_script_part2 = "mobileMenu.classList.add('translate-x-full');"
    
    new_script_part1 = "mobileMenu.classList.remove('translate-x-full'); mobileMenu.classList.add('translate-x-0');"
    new_script_part2 = "mobileMenu.classList.remove('translate-x-0'); mobileMenu.classList.add('translate-x-full');"
    
    if old_script_part1 in content and new_script_part1 not in content:
        content = content.replace(old_script_part1, new_script_part1)
        content = content.replace(old_script_part2, new_script_part2)
        
        # Make the logic run immediately if DOM is already loaded
        content = content.replace("document.addEventListener('DOMContentLoaded', () => {", "const initMenu = () => {")
        content = content.replace("});\n    </script>\n</body>", "};\n        if(document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', initMenu); } else { initMenu(); }\n    </script>\n</body>")
        # Handle cases where </body> is not immediately after
        content = content.replace("});\n    </script>\n    <script src=\"cms.js\">", "};\n        if(document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', initMenu); } else { initMenu(); }\n    </script>\n    <script src=\"cms.js\">")

        with open(file, 'w') as f:
            f.write(content)
        print(f"Fixed {file}")
