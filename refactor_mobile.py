import os
import glob
import re

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # 1. Update the toggle button to use inline onclick
    # It might be: <button class="md:hidden text-primary" id="mobile-menu-toggle">
    toggle_pattern = re.compile(r'<button class="md:hidden text-primary" id="mobile-menu-toggle">')
    toggle_replacement = '<button class="md:hidden text-primary" id="mobile-menu-toggle" onclick="document.getElementById(\\\'mobile-menu\\\').classList.remove(\\\'translate-x-full\\\'); document.body.classList.add(\\\'overflow-hidden\\\');">'
    content = toggle_pattern.sub(toggle_replacement, content)

    # 2. Update the close button to use inline onclick
    # It might be: <button id="close-mobile-menu" class="text-primary">
    close_pattern = re.compile(r'<button id="close-mobile-menu" class="text-primary">')
    close_replacement = '<button id="close-mobile-menu" class="text-primary" onclick="document.getElementById(\\\'mobile-menu\\\').classList.add(\\\'translate-x-full\\\'); document.body.classList.remove(\\\'overflow-hidden\\\');">'
    content = close_pattern.sub(close_replacement, content)

    # 3. Remove the entire <script> block for Mobile Menu Logic
    script_pattern = re.compile(r'\s*<script>\s*// Mobile Menu Logic.*?</script>', re.DOTALL)
    content = script_pattern.sub('', content)

    with open(file, 'w') as f:
        f.write(content)
        
    print(f"Refactored mobile menu in {file} to use inline onclick handlers.")
