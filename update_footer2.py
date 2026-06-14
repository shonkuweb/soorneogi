import os
import re

directory = '/Users/shonkuweb/soorneogi/SoorNeogiWeb'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    footer_pattern = re.compile(r'(<footer\b[^>]*>)(.*?)(</footer>)', re.DOTALL)
    
    def replacer(match):
        footer_tag = match.group(1)
        inner_content = match.group(2)
        
        # update divider in copyright section
        inner_content = inner_content.replace('border-slate-200/60', 'border-[#2d3748]')
        
        # update badges
        inner_content = inner_content.replace('bg-surface-container-low', 'bg-[#2d3748]')
        inner_content = inner_content.replace('text-secondary text-xs', 'text-slate-300 text-xs')
        
        # In case the text-secondary wasn't replaced where it lacks dark mode classes
        # The badges had: text-secondary text-xs font-bold
        
        return footer_tag + inner_content + '</footer>'

    new_content = footer_pattern.sub(replacer, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Updated footer bottom borders and badges.")
