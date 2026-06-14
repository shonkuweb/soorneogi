import os
import re
import glob

html_files = glob.glob('*.html')

MOBILE_MENU_HTML = """
        <!-- Mobile Menu Overlay -->
        <div id="mobile-menu" class="fixed inset-0 bg-white z-[60] transform translate-x-full transition-transform duration-300 md:hidden flex flex-col">
            <div class="flex justify-between items-center p-6 border-b border-slate-100">
                <span class="font-headline-sm font-bold text-primary">Menu</span>
                <button id="close-mobile-menu" class="text-primary">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <nav class="flex flex-col p-6 gap-6 overflow-y-auto">
                <a href="index.html" class="font-label-bold text-lg text-secondary">Home</a>
                <a href="gallery.html" class="font-label-bold text-lg text-secondary">Gallery</a>
                <a href="achievements.html" class="font-label-bold text-lg text-secondary">Achievements</a>
                <a href="products.html" class="font-label-bold text-lg text-secondary">Products</a>
                <a href="about.html" class="font-label-bold text-lg text-secondary">About Us</a>
                <a href="clientele.html" class="font-label-bold text-lg text-secondary">Clientele</a>
                <a href="enquiry.html" class="bg-gradient-to-r from-amber-500 to-orange-600 text-white px-6 py-3 rounded text-center font-label-bold mt-4 shadow-lg shadow-orange-500/30">Enquiry Now</a>
            </nav>
        </div>
    </header>
"""

MOBILE_MENU_SCRIPT = """
    <script>
        // Mobile Menu Logic
        document.addEventListener('DOMContentLoaded', () => {
            const mobileMenuBtn = document.getElementById('mobile-menu-toggle');
            const closeMobileMenuBtn = document.getElementById('close-mobile-menu');
            const mobileMenu = document.getElementById('mobile-menu');
            
            if (mobileMenuBtn && closeMobileMenuBtn && mobileMenu) {
                mobileMenuBtn.addEventListener('click', () => {
                    mobileMenu.classList.remove('translate-x-full');
                });
                closeMobileMenuBtn.addEventListener('click', () => {
                    mobileMenu.classList.add('translate-x-full');
                });
            }
        });
    </script>
</body>
"""

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Add id to mobile toggle button
    content = content.replace('<button class="md:hidden text-primary">', '<button class="md:hidden text-primary" id="mobile-menu-toggle">')

    # Add mobile menu inside header (just before </header>)
    if 'id="mobile-menu"' not in content:
        content = content.replace('</header>', MOBILE_MENU_HTML)
    
    # Add script before </body>
    if 'mobile-menu-toggle' in content and '// Mobile Menu Logic' not in content:
        content = content.replace('</body>', MOBILE_MENU_SCRIPT)

    # Fix header padding
    content = content.replace('px-margin-desktop flex justify-between', 'px-6 md:px-margin-desktop flex justify-between')

    # Fix footer layout (making it responsive)
    # The current footer has `<div class="max-w-container-max mx-auto px-margin-desktop grid grid-cols-1 md:grid-cols-4 gap-gutter">`
    content = content.replace('px-margin-desktop grid grid-cols-1 md:grid-cols-4', 'px-6 md:px-margin-desktop grid grid-cols-1 md:grid-cols-4 gap-8 md:gap-gutter')
    
    # Also fix footer copyright row padding
    content = content.replace('px-margin-desktop mt-12 pt-8', 'px-6 md:px-margin-desktop mt-8 md:mt-12 pt-8')

    with open(file, 'w') as f:
        f.write(content)

print("Updated HTML files with mobile menu.")
