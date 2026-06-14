import os
import glob
import re

html_files = glob.glob('*.html')

# Mapping from alt text keywords to local image paths
img_map = {
    'logo': 'images/soor_neogi_logo.png',
    'mild steel': 'images/mild_steel_pipes.png',
    'galvanized': 'images/galvanized_pipes.png',
    'hdpe': 'images/hdpe_pipes.png',
    'pvc': 'images/pvc_pipes.png',
    'steel pipes': 'images/mild_steel_pipes.png',
    'facility': 'images/hero_facility.png',
    'manufacturing': 'images/hero_facility.png',
    'other products': 'images/hero_facility.png',
    'achievement': 'images/achievements_banner.png',
    'welcome': 'images/soor_neogi_logo.png' # for admin.html freelancer.svg
}

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Find all <img> tags
    # We will replace them one by one.
    img_pattern = re.compile(r'<img[^>]*>')
    
    def replace_img(match):
        img_tag = match.group(0)
        
        # Determine which image this is based on alt attribute or src
        matched_path = None
        alt_match = re.search(r'alt="([^"]*)"', img_tag, re.IGNORECASE)
        alt_text = alt_match.group(1).lower() if alt_match else ""
        
        for key, path in img_map.items():
            if key in alt_text:
                matched_path = path
                break
                
        # If no alt matched, try to look at src (e.g., logo)
        if not matched_path and 'aida-public/AB6AXuAF' in img_tag:
            matched_path = 'images/soor_neogi_logo.png'
            
        if not matched_path:
            return img_tag # Leave as is if we can't figure it out
            
        # Does it already have a src?
        if 'src="' in img_tag:
            # Replace the existing src
            new_tag = re.sub(r'src="[^"]*"', f'src="{matched_path}"', img_tag)
            return new_tag
        else:
            # Inject src right after <img
            new_tag = img_tag.replace('<img', f'<img src="{matched_path}"', 1)
            return new_tag

    new_content = img_pattern.sub(replace_img, content)

    # Additionally, achievements.html has javascript that sets src dynamically:
    # <img src="${imgSrc}" alt="Achievement ${i}" ...>
    # The script uses a for loop over images/achive${i}.jpg. We should fix the script in achievements.html
    if file == 'achievements.html':
        new_content = new_content.replace('images/achive${i}.jpg', 'images/achievements_banner.png')

    with open(file, 'w') as f:
        f.write(new_content)
        
    print(f"Updated images in {file}")

