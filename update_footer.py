import os
import re

directory = '/Users/shonkuweb/soorneogi/SoorNeogiWeb'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use regex to find the footer block
    footer_pattern = re.compile(r'(<footer\b[^>]*>)(.*?)(</footer>)', re.DOTALL)
    
    def replacer(match):
        footer_tag = match.group(1)
        inner_content = match.group(2)
        
        # update footer classes
        footer_tag = footer_tag.replace('bg-slate-50 dark:bg-surface-dim', 'bg-[#1c2434] text-slate-300')
        footer_tag = footer_tag.replace('border-slate-200/60', 'border-[#1c2434]')
        
        # update inner content classes
        inner_content = inner_content.replace('text-primary dark:text-primary-fixed', 'text-white')
        inner_content = inner_content.replace('text-on-surface dark:text-on-surface-variant', 'text-slate-300')
        inner_content = inner_content.replace('text-secondary dark:text-on-secondary-fixed-variant', 'text-slate-400')
        inner_content = inner_content.replace('hover:text-on-tertiary-container', 'hover:text-white')
        
        # icon classes update
        inner_content = inner_content.replace('text-secondary hover:text-amber-500', 'text-slate-400 hover:text-amber-500')
        
        return footer_tag + inner_content + '</footer>'

    new_content = footer_pattern.sub(replacer, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Updated all footers.")
